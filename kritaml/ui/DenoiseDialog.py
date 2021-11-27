from PyQt5.QtWidgets import *
from .LabelSpinBox import LabelSpinBox

class DenoiseDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Denoise")

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.h_input = LabelSpinBox(self)
        self.h_input.label.setText("h:")
        self.h_input.spinbox.setValue(10)
        self.h_input.spinbox.setMinimum(0)
        self.h_input.spinbox.setMaximum(100)
        self.h_input.spinbox.setSingleStep(1)
        self.h_input.spinbox.setDecimals(0)

        self.t_input = LabelSpinBox(self)
        self.t_input.label.setText("Template Window Half Size:")
        self.t_input.spinbox.setValue(3)
        self.t_input.spinbox.setMinimum(0)
        self.t_input.spinbox.setMaximum(100)
        self.t_input.spinbox.setSingleStep(1)
        self.t_input.spinbox.setDecimals(0)

        self.s_input = LabelSpinBox(self)
        self.s_input.label.setText("Search Window Half Size:")
        self.s_input.spinbox.setValue(3)
        self.s_input.spinbox.setMinimum(0)
        self.s_input.spinbox.setMaximum(100)
        self.s_input.spinbox.setSingleStep(1)
        self.s_input.spinbox.setDecimals(0)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.h_input)
        self.layout.addWidget(self.t_input)
        self.layout.addWidget(self.s_input)
        self.layout.addStretch()
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    
    def get_h(self):
        return self.h_input.spinbox.value()

    
    def get_template_half_size(self):
        return self.t_input.spinbox.value()

    
    def get_search_half_size(self):
        return self.s_input.spinbox.value()