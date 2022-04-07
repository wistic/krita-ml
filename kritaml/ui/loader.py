from PyQt5.QtWidgets import QVBoxLayout, QDialog, QProgressBar
from PyQt5 import QtCore


class Loader(QDialog):

    def __init__(self, title, parent=None):
        super().__init__(parent)

        self.setWindowFlags(self.windowFlags() | QtCore.Qt.CustomizeWindowHint)

        self.setWindowFlags(self.windowFlags() & ~
                            QtCore.Qt.WindowCloseButtonHint)
        self.setModal(True)

        self.setWindowTitle(title)
        layout = QVBoxLayout(self)

        self.progressBar = QProgressBar(self)
        self.progressBar.setRange(0, 0)
        layout.addWidget(self.progressBar)
