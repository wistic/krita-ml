import os
import torch
import cv2
import numpy as np
from krita import *
from PIL import Image
from torchvision.transforms import Compose
from .dpt.models import DPTDepthModel
from .dpt.transforms import Resize, NormalizeImage, PrepareForNet


def run_monodepth(model_path, input_image):

    torch.backends.cudnn.enabled = True
    torch.backends.cudnn.benchmark = True  

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    net_w = net_h = 384

    model = DPTDepthModel(
        path=model_path,
        backbone="vitb_rn50_384",
        non_negative=True,
        enable_attention_hooks=False,
    )
    normalization = NormalizeImage(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])

    transform = Compose(
        [
            Resize(
                net_w,
                net_h,
                resize_target=None,
                keep_aspect_ratio=True,
                ensure_multiple_of=32,
                resize_method="minimal",
                image_interpolation_method=cv2.INTER_CUBIC,
            ),
            normalization,
            PrepareForNet(),
        ]
    )

    model.eval()

    if device == torch.device("cuda"):
        model = model.to(memory_format=torch.channels_last)
        model = model.half()

    model.to(device)

    img_input = transform({"image": input_image})["image"]

    with torch.no_grad():
        sample = torch.from_numpy(img_input).to(device).unsqueeze(0)

        if device == torch.device("cuda"):
            sample = sample.to(memory_format=torch.channels_last)
            sample = sample.half()

        prediction = model.forward(sample)
        prediction = (
            torch.nn.functional.interpolate(
                prediction.unsqueeze(1),
                size=input_image.shape[:2],
                mode="bicubic",
                align_corners=False,
            )
            .squeeze()
            .cpu()
            .numpy()
        )
        return prediction


def apply_monodepth():
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
        input_array = np.array(alpha_composite, dtype=np.uint8) / 255.0
        krita_cwd = os.path.dirname(os.path.realpath(__file__))
        model_path = os.path.join(krita_cwd, "weights.pt")

        depth = run_monodepth(model_path, input_array)

        depth_min = depth.min()
        depth_max = depth.max()

        if depth_max - depth_min > np.finfo("float").eps:
            depth = (depth - depth_min) * (255.0 / (depth_max - depth_min))
        else:
            depth = np.zeros(depth.shape, dtype=depth.dtype)

        depth = np.repeat(depth.reshape(depth.shape[0], depth.shape[1], 1), 3, axis=2)
        magic_image = Image.fromarray(depth.astype("uint8"), "RGB")
        magic_image.putalpha(255)
        magic_pixel_data = magic_image.tobytes()
        layer.setPixelData(magic_pixel_data, 0, 0, width, height)
        doc.refreshProjection()