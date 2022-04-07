from krita import *
from .features import *
from PyQt5.QtWidgets import QMenu


class KritaMLExtension(Extension):

    def __init__(self, parent):
        # This is initialising the parent, always important when subclassing.
        super().__init__(parent)

    def setup(self):
        pass

    def createActions(self, window):

        action = window.createAction("kritaml", "Krita-ML", "tools/scripts")
        menu = QMenu("kritaml", window.qwindow())
        action.setMenu(menu)

        # menu = QMenu("Krita-ML", window.qwindow())
        denoise_action = window.createAction(
            "denoise", "Reduce Image Noise", "tools/scripts/kritaml")
        denoise_action.triggered.connect(apply_denoise)
        dehaze_action = window.createAction(
            "dehaze", "Remove Haze", "tools/scripts/kritaml")
        dehaze_action.triggered.connect(apply_dehaze)
        monodepth_action = window.createAction(
            "monodepth", "Monodepth", "tools/scripts/kritaml")
        monodepth_action.triggered.connect(apply_monodepth)
        recolor_action = window.createAction(
            "recolor", "Recolor", "tools/scripts/kritaml")
        recolor_action.triggered.connect(apply_recolor)
        super_resolution_action = window.createAction(
            "super_resolution", "Super Resolution", "tools/scripts/kritaml")
        super_resolution_action.triggered.connect(apply_super_resolution)
        cartoon_action = window.createAction(
            "sketch", "Sketch", "tools/scripts/kritaml")
        cartoon_action.triggered.connect(apply_sketch)


# And add the extension to Krita's list of extensions:
Krita.instance().addExtension(KritaMLExtension(Krita.instance()))
