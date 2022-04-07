import os
from cv2 import dnn_superres
from krita import *
from PIL import Image
import numpy as np
from ..util import launch_loader, Worker


def apply_super_resolution():
    doc = Krita.instance().activeDocument()
    if doc is not None:
        worker = SuperResolutionWorker(doc)
        launch_loader(worker)
        worker.apply_changes()


class SuperResolutionWorker(Worker):

    def apply_changes(self):
        new_width = 3*self.width
        new_height = 3*self.height
        self.doc.resizeImage(0, 0, new_width, new_height)
        self.layer.setPixelData(self.result, 0, 0, new_width, new_height)
        self.doc.refreshProjection()

    def run(self):
        mode = "RGBA"
        size = (self.width, self.height)
        pil_image = Image.frombytes(mode, size, self.pixel_data)
        alpha_composite = pil_image.convert('RGB')

        image = np.array(alpha_composite, dtype=np.uint8)

        # Create an SR object
        sr = dnn_superres.DnnSuperResImpl_create()

        # Read the desired model
        krita_cwd = os.path.dirname(os.path.realpath(__file__))
        path = os.path.join(krita_cwd, "superresolution-EDSR_x3.pb")
        sr.readModel(path)

        # Set the desired model and scale to get correct pre- and post-processing
        sr.setModel("edsr", 3)

        # Upscale the image
        result = sr.upsample(image)
        result = (result).astype(np.uint8)

        # Save the image
        magic_image = Image.fromarray(result, "RGB")
        magic_image.putalpha(255)
        self.result = magic_image.tobytes()
