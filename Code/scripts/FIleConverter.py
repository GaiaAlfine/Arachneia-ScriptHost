# Insert this code where you need to select input and output file paths using buttons

from PySide2.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QFileDialog, QLabel

class FileConverter(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('File Converter')
        self.layout = QVBoxLayout()

        self.inputButton = QPushButton('Select Input File')
        self.inputButton.clicked.connect(self.selectInputFile)
        self.layout.addWidget(self.inputButton)

        self.inputLabel = QLabel('Input File Path: None')
        self.layout.addWidget(self.inputLabel)

        self.outputButton = QPushButton('Select Output File Path')
        self.outputButton.clicked.connect(self.selectOutputFile)
        self.layout.addWidget(self.outputButton)

        self.outputLabel = QLabel('Output File Path: None')
        self.layout.addWidget(self.outputLabel)

        self.setLayout(self.layout)
    
    def selectInputFile(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Input File")
        if file_path:
            self.inputLabel.setText(f'Input File Path: {file_path}')
            self.input_file_path = file_path
    
    def selectOutputFile(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Select Output File Path")
        if file_path:
            self.outputLabel.setText(f'Output File Path: {file_path}')
            self.output_file_path = file_path

def get_tab_widget():
    widget = FileConverter()
    return widget