from krita import *
import cv2
import numpy as np
from PIL import Image


def denoise():
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
        processed_numpy_image = cv2.fastNlMeansDenoisingColored(numpy_image, None, 10, 10, 7, 21)

        # Back to PIL image
        processed_image = Image.fromarray(processed_numpy_image, mode)

        # Back to image data
        processed_pixel_data = processed_image.tobytes()

        # ...which we can then send back to Krita.
        layer.setPixelData(processed_pixel_data, 0, 0, width, height)

        # Last, but least, let's refresh krita so that we see our changes.
        doc.refreshProjection()
