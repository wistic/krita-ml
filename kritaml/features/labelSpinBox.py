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
