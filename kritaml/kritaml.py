from krita import *
from .features import *


class KritaMLExtension(Extension):

    def __init__(self, parent):
        # This is initialising the parent, always important when subclassing.
        super().__init__(parent)

    def setup(self):
        pass

    def createActions(self, window):
        denoise_action = window.createAction("denoise", "Reduce Image Noise", "tools/scripts")
        denoise_action.triggered.connect(apply_denoise)
        dehaze_action = window.createAction("dehaze", "Remove Haze", "tools/scripts")
        dehaze_action.triggered.connect(apply_dehaze)
        monodepth_action = window.createAction("monodepth", "Monodepth", "tools/scripts")
        monodepth_action.triggered.connect(apply_monodepth)
        recolor_action = window.createAction("recolor", "Recolor", "tools/scripts")
        recolor_action.triggered.connect(apply_recolor)

# And add the extension to Krita's list of extensions:
Krita.instance().addExtension(KritaMLExtension(Krita.instance()))
