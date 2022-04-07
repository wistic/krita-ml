import cv2
import os
import numpy as np
from krita import *
from PIL import Image
from ..util import launch_loader, Worker


def apply_recolor():

    doc = Krita.instance().activeDocument()
    if doc is not None:
        worker = RecolorWorker(doc)
        launch_loader(worker)
        worker.apply_changes()


class RecolorWorker(Worker):

    def run(self):
        krita_cwd = os.path.dirname(os.path.realpath(__file__))
        prototxt_path = os.path.join(
            krita_cwd, "recolor-colorization_deploy_v2.prototxt")
        model_path = os.path.join(
            krita_cwd, "recolor-colorization_release_v2.caffemodel")
        kernel_path = os.path.join(krita_cwd, "recolor-pts_in_hull.npy")
        net = cv2.dnn.readNetFromCaffe(prototxt_path, model_path)
        points = np.load(kernel_path)

        mode = "RGBA"
        size = (self.width, self.height)
        pil_image = Image.frombytes(mode, size, self.pixel_data)
        alpha_composite = pil_image.convert('RGB')
        bw_image = np.array(alpha_composite, dtype=np.float32) / 255.0

        points = points.transpose().reshape(2, 313, 1, 1)
        net.getLayer(net.getLayerId("class8_ab")).blobs = [
            points.astype(np.float32)]
        net.getLayer(net.getLayerId("conv8_313_rh")).blobs = [
            np.full([1, 313], 2.606, dtype="float32")]

        lab = cv2.cvtColor(bw_image, cv2.COLOR_BGR2LAB)

        resized = cv2.resize(lab, (224, 224))
        L = cv2.split(resized)[0]
        L -= 50

        net.setInput(cv2.dnn.blobFromImage(L))
        ab = net.forward()[0, :, :, :].transpose((1, 2, 0))

        ab = cv2.resize(ab, (bw_image.shape[1], bw_image.shape[0]))
        L = cv2.split(lab)[0]

        recolor = np.concatenate((L[:, :, np.newaxis], ab), axis=2)
        recolor = cv2.cvtColor(recolor, cv2.COLOR_LAB2BGR)
        recolor = (255.0 * recolor).astype("uint8")

        magic_image = Image.fromarray(recolor, "RGB")
        magic_image.putalpha(255)
        self.result = magic_image.tobytes()
