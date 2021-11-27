from PyQt5.QtWidgets import *


class LabelSpinBox(QWidget):
    def __init__(self, text, value, minimum, maximum, step, decimal, parent=None):
        super().__init__(parent)
        self.label = QLabel(self)
        self.spinbox = QDoubleSpinBox(self)
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.spinbox)
        self.setLayout(self.layout)
        self.label.setText(text)
        self.spinbox.setValue(value)
        self.spinbox.setMinimum(minimum)
        self.spinbox.setMaximum(maximum)
        self.spinbox.setSingleStep(step)
        self.spinbox.setDecimals(decimal)

    def get_value(self):
        return self.spinbox.value()
