import sys
from krita import *
import cv2
import numpy as np
from PIL import Image
from ..util import launch_loader, Worker


# Reading the Image
def apply_sketch():
    doc = Krita.instance().activeDocument()
    if doc is not None:
        worker = SketchWorker(doc)
        launch_loader(worker)
        worker.apply_changes()


class SketchWorker(Worker):

    def run(self):
        mode = "RGBA"
        size = (self.width, self.height)
        pil_image = Image.frombytes(mode, size, self.pixel_data)
        alpha_composite = pil_image.convert('RGB')
        image = np.array(alpha_composite, dtype=np.uint8)

        k_size = 111
        grey_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Invert Image
        invert_img = cv2.bitwise_not(grey_img)

        # Blur image
        blur_img = cv2.GaussianBlur(invert_img, (k_size, k_size), 0)

        # Invert Blurred Image
        invblur_img = cv2.bitwise_not(blur_img)
        # invblur_img=255-blur_img

        # Sketch Image
        sketch_img = cv2.divide(grey_img, invblur_img, scale=256.0)
        stacked_img = np.stack((sketch_img,)*3, axis=-1)
        magic_image = Image.fromarray(
            stacked_img.astype("uint8"), "RGB")
        magic_image.putalpha(255)
        self.result = magic_image.tobytes()
