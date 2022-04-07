from PyQt5.QtCore import QThread, QObject
import typing
from ..ui import Loader


def launch_loader(thread: QThread):
    dialog = Loader("Processing")
    thread.finished.connect(dialog.close)
    thread.start()
    dialog.exec()


class Worker(QThread):

    def __init__(self, doc) -> None:
        super().__init__()
        self.doc = doc
        self.layer = doc.activeNode()
        self.width = doc.width()
        self.height = doc.height()
        self.pixel_data = self.layer.pixelData(0, 0, self.width, self.height)
        self.result = None

    def apply_changes(self):
        self.layer.setPixelData(self.result, 0, 0, self.width, self.height)
        self.doc.refreshProjection()
