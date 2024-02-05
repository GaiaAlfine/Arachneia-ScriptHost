import sys
import re
import os
from PySide2.QtWidgets import QPushButton, QFileDialog, QTextBrowser, QVBoxLayout, QWidget, QLabel, QProgressBar, QHBoxLayout, QApplication
from PySide2.QtGui import QDesktopServices
from PySide2.QtCore import Qt, QThread, Signal

class URLExtractionThread(QThread):
    url_found = Signal(str)
    progress_updated = Signal(int)
    stop_flag = False

    def __init__(self, folder_path):
        super().__init__()
        self.folder_path = folder_path

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
                    content = self.read_file_with_fallback_encodings(file_path)
                    if content:
                        urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', content)
                        folder_url = f'file:///{root}'
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
        return None

    def stop(self):
        self.stop_flag = True

def get_tab_widget():
    widget = QWidget()
    layout = QVBoxLayout(widget)

    titleLabel = QLabel('URL Extractor')
    titleLabel.setAlignment(Qt.AlignCenter)

    btnSelect = QPushButton('Select Folder')
    btnExport = QPushButton('Export URLs')
    btnClear = QPushButton('Clear')
    btnStop = QPushButton('Stop')
    
    progressBar = QProgressBar()
    progressBar.setTextVisible(False)

    textBrowser = QTextBrowser()
    textBrowser.setPlaceholderText("Extracted URLs will be displayed here.")

    buttonLayout = QHBoxLayout()
    buttonLayout.addWidget(btnSelect)
    buttonLayout.addWidget(btnExport)
    buttonLayout.addWidget(btnClear)
    buttonLayout.addWidget(btnStop)

    layout.addWidget(titleLabel)
    layout.addLayout(buttonLayout)
    layout.addWidget(progressBar)
    layout.addWidget(textBrowser)

    extractionThread = None

    def loadFile():
        folder_path = QFileDialog.getExistingDirectory(widget, "Select Folder")
        if folder_path:
            nonlocal extractionThread
            textBrowser.setText("Processing files... Please wait.")
            
            # Initialize the progress bar at the start of the loading operation
            progressBar.setValue(0)  # Set the progress bar to 0 to indicate the start
            
            extractionThread = URLExtractionThread(folder_path)
            extractionThread.url_found.connect(lambda url: textBrowser.append(url))
            extractionThread.progress_updated.connect(progressBar.setValue)
            extractionThread.start()


    def saveFile():
        file_name, _ = QFileDialog.getSaveFileName(widget, "Save File", "", "Text Files (*.txt);;All Files (*)")
        if file_name:
            with open(file_name, 'w') as file:
                file.write(textBrowser.toPlainText())

    def clearText():
        progressBar.setValue(0) 
        textBrowser.clear()

    def stopOperation():
        if extractionThread and extractionThread.isRunning():
            progressBar.setValue(100)
            extractionThread.stop()
            

    btnSelect.clicked.connect(loadFile)
    btnExport.clicked.connect(saveFile)
    btnClear.clicked.connect(clearText)
    btnStop.clicked.connect(stopOperation)

    return widget
