from PyQt5.QtWidgets import *
from krita import *
import cv2
import numpy as np
from PIL import Image
from ...ui import DenoiseDialog
from ..util import launch_loader, Worker


def run_denoise(h, tSize, sSize):

    doc = Krita.instance().activeDocument()
    if doc is not None:
        worker = DenoiseWorker(doc, h, tSize, sSize)
        launch_loader(worker)
        worker.apply_changes()


def apply_denoise():
    dialog = DenoiseDialog()
    if dialog.exec():
        h = int(dialog.get_h())
        tSize = int(dialog.get_template_half_size()) * 2 + 1
        sSize = int(dialog.get_search_half_size()) * 2 + 1
        run_denoise(h, tSize, sSize)


class DenoiseWorker(Worker):

    def __init__(self, doc, h, tSize, sSize) -> None:
        super().__init__(doc)
        self.h = h
        self.tSize = tSize
        self.sSize = sSize

    def run(self):
        mode = "RGBA"
        size = (self.width, self.height)
        pil_image = Image.frombytes(mode, size, self.pixel_data)
        numpy_image = np.array(pil_image, dtype=np.uint8)
        processed_numpy_image = cv2.fastNlMeansDenoisingColored(
            numpy_image, None, self.h, self.h, self.tSize, self.sSize)
        processed_image = Image.fromarray(processed_numpy_image, mode)
        self.result = processed_image.tobytes()
