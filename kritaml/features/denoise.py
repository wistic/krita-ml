from PyQt5.QtWidgets import *
from krita import *
import cv2
import numpy as np
from PIL import Image
from .labelSpinBox import LabelSpinBox


def denoise(h=10, tSize=7, sSize=21):
    doc = Krita.instance().activeDocument()

    # Check if document is empty
    if doc is not None:
        layer = doc.activeNode()
        width = doc.width()
        height = doc.height()

        # And let's grab the pixel data from it.
        pixel_data = layer.pixelData(0, 0, width, height)

        # Now we can form a PIL Image out of it.
        mode = "RGBA"
        size = (width, height)
        pil_image = Image.frombytes(mode, size, pixel_data)

        # and it's really easy to turn into a NumPy array:
        numpy_image = np.array(pil_image, dtype=np.uint8)

        # Reducing the image noise
        processed_numpy_image = cv2.fastNlMeansDenoisingColored(numpy_image, None, h, h, tSize, sSize)

        # Back to PIL image
        processed_image = Image.fromarray(processed_numpy_image, mode)

        # Back to image data
        processed_pixel_data = processed_image.tobytes()

        # ...which we can then send back to Krita.
        layer.setPixelData(processed_pixel_data, 0, 0, width, height)

        # Last, but least, let's refresh krita so that we see our changes.
        doc.refreshProjection()


class DenoiseDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Denoise")

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.hInput = LabelSpinBox(self)
        self.hInput.label.setText("h:")
        self.hInput.spinbox.setValue(10)
        self.hInput.spinbox.setMinimum(0)
        self.hInput.spinbox.setMaximum(100)
        self.hInput.spinbox.setSingleStep(1)
        self.hInput.spinbox.setDecimals(0)

        self.tSizeInput = LabelSpinBox(self)
        self.tSizeInput.label.setText("Template Window Half Size:")
        self.tSizeInput.spinbox.setValue(3)
        self.hInput.spinbox.setMinimum(0)
        self.hInput.spinbox.setMaximum(100)
        self.hInput.spinbox.setSingleStep(1)
        self.hInput.spinbox.setDecimals(0)

        self.sSizeInput = LabelSpinBox(self)
        self.sSizeInput.label.setText("Search Window Half Size:")
        self.sSizeInput.spinbox.setValue(3)
        self.hInput.spinbox.setMinimum(0)
        self.hInput.spinbox.setMaximum(100)
        self.hInput.spinbox.setSingleStep(1)
        self.hInput.spinbox.setDecimals(0)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.hInput)
        self.layout.addWidget(self.tSizeInput)
        self.layout.addWidget(self.sSizeInput)
        self.layout.addStretch()
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def run(self):
        if self.exec():
            h = int(self.hInput.spinbox.value())
            tSize = int(self.tSizeInput.spinbox.value()) * 2 + 1
            sSize = int(self.sSizeInput.spinbox.value()) * 2 + 1
            denoise(h, tSize, sSize)


def showDenoiseDialog():
    DenoiseDialog().run()
