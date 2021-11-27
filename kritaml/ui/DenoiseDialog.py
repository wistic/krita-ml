from PyQt5.QtWidgets import *
from .LabelSpinBox import LabelSpinBox


class DenoiseDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Denoise")

        self.buttonBox = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.h_input = LabelSpinBox(
            "h:",
            10,
            0,
            100,
            1,
            0,
            self
        )

        self.t_input = LabelSpinBox(
            "Template Window Half Size:",
            3,
            0,
            100,
            1,
            0,
            self
        )

        self.s_input = LabelSpinBox(
            "Search Window Half Size:",
            3,
            0,
            100,
            1,
            0,
            self
        )

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.h_input)
        self.layout.addWidget(self.t_input)
        self.layout.addWidget(self.s_input)
        self.layout.addStretch()
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def get_h(self):
        return self.h_input.get_value()

    def get_template_half_size(self):
        return self.t_input.get_value()

    def get_search_half_size(self):
        return self.s_input.get_value()
