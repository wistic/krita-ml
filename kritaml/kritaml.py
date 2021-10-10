from krita import *
from .features import *


class KritaMLExtension(Extension):

    def __init__(self, parent):
        # This is initialising the parent, always important when subclassing.
        super().__init__(parent)

    def setup(self):
        pass

    def createActions(self, window):
        action = window.createAction("denoise", "Reduce Image Noise", "tools/scripts")
        action.triggered.connect(denoise)


# And add the extension to Krita's list of extensions:
Krita.instance().addExtension(KritaMLExtension(Krita.instance()))
