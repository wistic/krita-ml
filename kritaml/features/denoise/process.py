from PyQt5.QtWidgets import *
from krita import *
import cv2
import numpy as np
from PIL import Image
from ...ui import DenoiseDialog


def run_denoise(h=10, tSize=7, sSize=21):
    doc = Krita.instance().activeDocument()

    if doc is not None:
        layer = doc.activeNode()
        width = doc.width()
        height = doc.height()
        pixel_data = layer.pixelData(0, 0, width, height)
        mode = "RGBA"
        size = (width, height)
        pil_image = Image.frombytes(mode, size, pixel_data)
        numpy_image = np.array(pil_image, dtype=np.uint8)
        processed_numpy_image = cv2.fastNlMeansDenoisingColored(numpy_image, None, h, h, tSize, sSize)
        processed_image = Image.fromarray(processed_numpy_image, mode)
        processed_pixel_data = processed_image.tobytes()
        layer.setPixelData(processed_pixel_data, 0, 0, width, height)
        doc.refreshProjection()


def apply_denoise():
    dialog = DenoiseDialog()
    if dialog.exec():
        h = int(dialog.get_h())
        tSize = int(dialog.get_template_half_size()) * 2 + 1
        sSize = int(dialog.get_search_half_size()) * 2 + 1
        run_denoise(h, tSize, sSize)
