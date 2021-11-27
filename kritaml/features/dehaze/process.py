import os
import numpy as np
import torch
import torch.nn as nn
import torch.optim
from krita import *
from PIL import Image


class net_dehaze_net(nn.Module):

    def __init__(self):
        super(net_dehaze_net, self).__init__()

        self.relu = nn.ReLU(inplace=True)

        self.e_conv1 = nn.Conv2d(3, 3, 1, 1, 0, bias=True)
        self.e_conv2 = nn.Conv2d(3, 3, 3, 1, 1, bias=True)
        self.e_conv3 = nn.Conv2d(6, 3, 5, 1, 2, bias=True)
        self.e_conv4 = nn.Conv2d(6, 3, 7, 1, 3, bias=True)
        self.e_conv5 = nn.Conv2d(12, 3, 3, 1, 1, bias=True)

    def forward(self, x):
        source = list()
        source.append(x)

        x1 = self.relu(self.e_conv1(x))
        x2 = self.relu(self.e_conv2(x1))

        concat1 = torch.cat((x1, x2), 1)
        x3 = self.relu(self.e_conv3(concat1))

        concat2 = torch.cat((x2, x3), 1)
        x4 = self.relu(self.e_conv4(concat2))

        concat3 = torch.cat((x1, x2, x3, x4), 1)
        x5 = self.relu(self.e_conv5(concat3))

        clean_image = self.relu((x5 * x) - x5 + 1)

        return clean_image


def apply_dehaze():
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

        data_hazy = input_array
        data_hazy = torch.from_numpy(data_hazy).float()
        data_hazy = data_hazy.permute(2, 0, 1)
        data_hazy = data_hazy.cuda().unsqueeze(0)
        dehaze_net = net_dehaze_net().cuda()
        krita_cwd = os.path.dirname(os.path.realpath(__file__))
        model_path = os.path.join(krita_cwd, 'weights.pth')
        dehaze_net.load_state_dict(torch.load(model_path))
        clean_image = dehaze_net(data_hazy)

        clean_array = clean_image.detach().cpu().numpy()
        clean_array = (clean_array * 255.0).astype('uint8')
        clean_array = np.transpose(clean_array[0], (1, 2, 0))
        magic_image = Image.fromarray(clean_array, "RGB")

        magic_image.putalpha(255)

        magic_pixel_data = magic_image.tobytes()

        # ...which we can then send back to Krita.
        layer.setPixelData(magic_pixel_data, 0, 0, width, height)
        doc.refreshProjection()
