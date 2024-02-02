from PySide2.QtWidgets import QWidget, QVBoxLayout, QLabel

class CustomWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        self.setLayout(layout)
        layout.addWidget(QLabel("Content of the script"))

def get_widget():
    return CustomWidget()
