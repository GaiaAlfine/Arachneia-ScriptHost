# script2.py in the scripts folder
from PySide2.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton

def get_tab_widget():
    widget = QWidget()
    layout = QVBoxLayout(widget)
    
    label = QLabel("Enter something:")
    layout.addWidget(label)
    
    line_edit = QLineEdit()
    layout.addWidget(line_edit)
    
    button = QPushButton("Submit")
    layout.addWidget(button)
    
    # Update label to show input text when the button is clicked
    button.clicked.connect(lambda: label.setText(f"You entered: {line_edit.text()}"))
    
    return widget
