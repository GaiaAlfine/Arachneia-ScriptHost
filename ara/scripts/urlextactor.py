import sys
import re
import os
from PySide2.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QTextBrowser, QVBoxLayout, QWidget, QLabel, QProgressBar, QHBoxLayout
from PySide2.QtGui import QDesktopServices
from PySide2.QtCore import Qt, QThread, Signal

class URLExtractionThread(QThread):
    url_found = Signal(str)
    progress_updated = Signal(int)  # Signal to emit progress percentage
    stop_flag = False

    def __init__(self, folder_path):
        super().__init__()
        self.folder_path = folder_path
        self.stop_flag = False

    def run(self):
        self.stop_flag = False
        total_files = sum([len(files) for _, _, files in os.walk(self.folder_path)])
        processed_files = 0

        for root, dirs, files in os.walk(self.folder_path):
            if self.stop_flag:
                break
            for filename in files:
                if self.stop_flag:
                    break
                if filename.endswith(".txt"):
                    file_path = os.path.join(root, filename)
                    folder_url = f'file:///{root}'
                    content = self.read_file_with_fallback_encodings(file_path)
                    if content is not None:
                        urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', content)
                        if urls:
                            formatted_entry = f'<a href="{folder_url}" style="color: #c77100;">From {filename} in [{root}]</a>:<br>' + '<br>'.join([f'<a href="{url}">{url}</a>' for url in urls]) + '<br><br>'
                            self.url_found.emit(formatted_entry)
                processed_files += 1
                progress = int((processed_files / total_files) * 100)
                self.progress_updated.emit(progress)


    def read_file_with_fallback_encodings(self, file_path):
        encodings = ['utf-8', 'iso-8859-1', 'windows-1252']
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as file:
                    return file.read()
            except UnicodeDecodeError:
                continue
        print(f"Could not read {file_path} due to encoding issue")
        return None
    
    def stop(self):
        self.stop_flag = True

class URLExtractorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('URL Extractor')
        self.setGeometry(300, 300, 600, 400)

        layout = QVBoxLayout()

        # Title text at the top, use a QLabel for this
        self.titleLabel = QLabel('URL Extractor')
        self.titleLabel.setAlignment(Qt.AlignCenter)

        # Create buttons as per the new layout
        self.btnSelect = QPushButton('Select')
        self.btnExport = QPushButton('Export')
        self.btnClear = QPushButton('Clear')
        self.btnStop = QPushButton('Stop')

        # Create a progress bar and hide the percentage text
        self.progressBar = QProgressBar()
        self.progressBar.setTextVisible(False)  # Hide the percentage text

        # Modify textBrowser to display URLs
        self.textBrowser = QTextBrowser()
        self.textBrowser.setPlaceholderText("Extracted URLs will be displayed here.")
        self.progressBar.setMaximum(100)
        # Button layout
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.btnSelect)
        buttonLayout.addWidget(self.btnExport)
        buttonLayout.addWidget(self.btnClear)

        # Add widgets to the main layout
        layout.addWidget(self.titleLabel)
        layout.addLayout(buttonLayout)
        layout.addWidget(self.progressBar)
        layout.addWidget(self.textBrowser)
        layout.addWidget(self.btnStop)

        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

        # Connect buttons to their functions
        self.btnSelect.clicked.connect(self.loadFile)
        self.btnExport.clicked.connect(self.saveFile)
        self.btnClear.clicked.connect(self.clearText)
        self.btnStop.clicked.connect(self.stopOperation)
        
    def loadFile(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder_path:
            self.textBrowser.setText("Processing files... Please wait.")
            self.extractionThread = URLExtractionThread(folder_path)
            self.extractionThread.url_found.connect(self.updateTextBrowser)
            self.extractionThread.progress_updated.connect(self.updateProgressBar)
            self.extractionThread.start()


    def updateProgressBar(self, value):
        self.progressBar.setValue(value)

    def updateTextBrowser(self, formatted_entry):
        self.textBrowser.append(formatted_entry)

    def saveFile(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Text Files (*.txt);;All Files (*)")
        if file_name:
            # Write URLs to the selected file, getting plain text from the QTextBrowser
            with open(file_name, 'w') as file:
                file.write(self.textBrowser.toPlainText())

    def openUrl(self, url):
        # Open the URL in the default web browser and prevent default action
        QDesktopServices.openUrl(url)

    def clearText(self):
        self.textBrowser.clear()

    def stopOperation(self):
        if hasattr(self, 'extractionThread') and self.extractionThread.isRunning():
            self.extractionThread.stop()
    # Add this function to the script that defines URLExtractorApp
    def get_widget():
        return URLExtractorApp()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = URLExtractorApp()
    mainWin.show()
    sys.exit(app.exec_())
