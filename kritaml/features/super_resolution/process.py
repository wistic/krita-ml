import cv2
from cv2 import dnn_superres
from krita import *
from PIL import Image
import numpy as np

def apply_super_resolution():
    doc = Krita.instance().activeDocument()
    if doc is not None:

        layer = doc.activeNode()
        width = doc.width()
        height = doc.height()
        pixel_data = layer.pixelData(0, 0, width, height)
        mode = "RGBA"
        size = (width, height)
        pil_image = Image.frombytes(mode, size, pixel_data)
        alpha_composite = pil_image.convert('RGB')

        image = np.array(alpha_composite, dtype=np.uint8)

        # Create an SR object
        sr = dnn_superres.DnnSuperResImpl_create()

        # Read image
        #image = cv2.imread('./input.png')

        # Read the desired model
        krita_cwd = os.path.dirname(os.path.realpath(__file__))
        path = os.path.join(krita_cwd, "EDSR_x3.pb")
        sr.readModel(path)

        # Set the desired model and scale to get correct pre- and post-processing
        sr.setModel("edsr", 3)

        # Upscale the image
        result = sr.upsample(image)
        result = (result).astype(np.uint8)

        # Save the image
        #cv2.imwrite("/home/dazai/pic.png", result)
        magic_image = Image.fromarray(result, "RGB")
        #magic_image1 = Image.fromarray(result, "RGB").save('pic1.png')
        magic_image.putalpha(255)
        magic_pixel_data = magic_image.tobytes()

        # ...which we can then send back to Krita.
        n_width=3*width
        n_height=3*height
        doc.resizeImage(0,0,n_width,n_height)
        layer.setPixelData(magic_pixel_data, 0, 0, n_width, n_height)
        doc.refreshProjection()
        

