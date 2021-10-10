from krita import *
from .features import *
from PyQt5.QtWidgets import *

class LabelSpinBox(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.label = QLabel(self)
        self.spinbox = QDoubleSpinBox(self)
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.spinbox)
        self.setLayout(self.layout)


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


class KritaMLExtension(Extension):

    def __init__(self, parent):
        # This is initialising the parent, always important when subclassing.
        super().__init__(parent)

    def setup(self):
        pass

    def createActions(self, window):
        action = window.createAction("denoise", "Reduce Image Noise", "tools/scripts")
        # action.triggered.connect(denoise)
        action.triggered.connect(self.showDialog)

    def showDialog(self):
        DenoiseDialog().run()


# And add the extension to Krita's list of extensions:
Krita.instance().addExtension(KritaMLExtension(Krita.instance()))