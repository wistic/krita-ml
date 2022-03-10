from PyQt5.QtWidgets import *


class CartoonDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Cartoon")

        self.b1 = QRadioButton("Cartoonize")
        self.b1.setChecked(True)
        self.b2 = QRadioButton("Blurring Image")
        self.b3 = QRadioButton("Stylization")
        self.b4 = QRadioButton("Pencil Sketch")


        self.buttonBox = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.b1)
        self.layout.addWidget(self.b2)
        self.layout.addWidget(self.b3)
        self.layout.addWidget(self.b4)
        self.layout.addStretch()
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def check_state(self):
        if self.b1.isChecked():
            return 1
        if self.b2.isChecked():
            return 2
        if self.b3.isChecked():
            return 3
        if self.b4.isChecked():
            return 4

