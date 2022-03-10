from krita import *
import cv2
import numpy as np
from PIL import Image
from ...ui import CartoonDialog


# Reading the Image
def run_cartoon(state):
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

        if state == 1:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            gray = cv2.medianBlur(gray, 7)
            edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 10)
            # Making a Cartoon of the image
            color = cv2.bilateralFilter(image, 12, 250, 250)
            cartoon = cv2.bitwise_and(color, color, mask=edges)
            magic_image = Image.fromarray(cartoon.astype("uint8"), "RGB")
            magic_image.putalpha(255)
            magic_pixel_data = magic_image.tobytes()
            layer.setPixelData(magic_pixel_data, 0, 0, width, height)

        if state == 2 :
            grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            # apply gaussian blur
            grayImage = cv2.GaussianBlur(grayImage, (3, 3), 0)
            # detect edges
            edgeImage = cv2.Laplacian(grayImage, -1, ksize=5)
            edgeImage = 255 - edgeImage
            # threshold image
            ret, edgeImage = cv2.threshold(edgeImage, 150, 255, cv2.THRESH_BINARY)
            # blur images heavily using edgePreservingFilter
            edgePreservingImage = cv2.edgePreservingFilter(image, flags=2, sigma_s=50, sigma_r=0.4)
            # combine cartoon image and edges image
            output = cv2.bitwise_and(edgePreservingImage, edgePreservingImage, mask=edgeImage)
            magic_image = Image.fromarray(output.astype("uint8"), "RGB")
            magic_image.putalpha(255)
            magic_pixel_data = magic_image.tobytes()
            layer.setPixelData(magic_pixel_data, 0, 0, width, height)

        if state == 3:
            cartoon_image = cv2.stylization(image, sigma_s=150, sigma_r=0.25)
            magic_image = Image.fromarray(cartoon_image.astype("uint8"), "RGB")
            magic_image.putalpha(255)
            magic_pixel_data = magic_image.tobytes()
            layer.setPixelData(magic_pixel_data, 0, 0, width, height)


        if state == 4:
            cartoon_image1, cartoon_image2 = cv2.pencilSketch(image, sigma_s=60, sigma_r=0.5, shade_factor=0.02)
            magic_image = Image.fromarray(cartoon_image2.astype("uint8"), "RGB")
            magic_image.putalpha(255)
            magic_pixel_data = magic_image.tobytes()
            layer.setPixelData(magic_pixel_data, 0, 0, width, height)

        doc.refreshProjection()



def apply_cartoon():
    dialog = CartoonDialog()
    if dialog.exec():
        state = dialog.check_state()
        run_cartoon(state)

