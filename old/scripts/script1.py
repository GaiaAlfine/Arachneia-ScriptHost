# Example script that returns a QWidget
from PySide2.QtWidgets import QWidget, QVBoxLayout, QLabel

def main_widget():
    widget = QWidget()
    layout = QVBoxLayout()
    widget.setLayout(layout)
    layout.addWidget(QLabel("This is an example script GUI"))
    return widget
