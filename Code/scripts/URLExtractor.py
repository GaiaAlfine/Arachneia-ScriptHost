from PySide2.QtCore import QThread, Qt, QUrl, Signal
from PySide2.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QProgressBar, QTextBrowser, QHBoxLayout, QFileDialog, QApplication
from PySide2.QtGui import QDesktopServices
import os, re, sys

class URLExtractionThread(QThread):
    url_found = Signal(str)
    progress_updated = Signal(int)

    def __init__(self, folder_path):
        super().__init__()
        self.folder_path = folder_path
        self.stop_flag = False

    def run(self):
        total_files = sum(1 for _, _, files in os.walk(self.folder_path) if any(file.endswith('.txt') for file in files))
        processed_files = 0

        for root, dirs, files in os.walk(self.folder_path):
            if self.stop_flag:
                break
            for filename in files:
                if self.stop_flag:
                    break
                if filename.endswith(".txt"):
                    file_path = os.path.join(root, filename)
                    folder_url = f'file:///{root}'.replace('\\', '/')
                    content = self.read_file_with_fallback_encodings(file_path)
                    if content:
                        urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', content)
                        urls = self.separate_adjacent_urls(urls)
                        if urls:
                            formatted_entry = f'<a href="{folder_url}" style="color: #c77100;">From {filename} in [{root}]</a>:<br>' + '<br>'.join([f'<a href="{url}">{url}</a>' for url in urls]) + '<br><br>'
                            self.url_found.emit(formatted_entry)
                processed_files += 1
                progress = int((processed_files / total_files) * 100)
                self.progress_updated.emit(progress)

    def separate_adjacent_urls(self, urls):
        separated_urls = []
        for url in urls:
            adjacent_urls = re.split(r'(?=http[s]?://)', url)
            separated_urls.extend(adjacent_urls)
        return separated_urls

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
        centralWidget = QWidget(self)
        layout = QVBoxLayout(centralWidget)

        self.titleLabel = QLabel('URL Extractor')
        self.titleLabel.setAlignment(Qt.AlignCenter)

        self.btnSelect = QPushButton('Select Folder')
        self.btnExport = QPushButton('Export Links')
        self.btnClear = QPushButton('Clear Output')
        self.btnStop = QPushButton('Stop Extraction')

        self.progressBar = QProgressBar()
        self.progressBar.setTextVisible(False)

        self.textBrowser = QTextBrowser()
        self.textBrowser.setPlaceholderText("Extracted URLs will be displayed here.")
        self.progressBar.setMaximum(100)

        self.textBrowser.anchorClicked.connect(self.openUrl)
        self.textBrowser.setOpenLinks(False)

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.btnSelect)
        buttonLayout.addWidget(self.btnExport)
        buttonLayout.addWidget(self.btnClear)

        layout.addWidget(self.titleLabel)
        layout.addLayout(buttonLayout)
        layout.addWidget(self.progressBar)
        layout.addWidget(self.textBrowser)
        layout.addWidget(self.btnStop)

        self.setCentralWidget(centralWidget)

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
            with open(file_name, 'w') as file:
                file.write(self.textBrowser.toPlainText())

    def openUrl(self, url: QUrl):
        QDesktopServices.openUrl(url)

    def clearText(self):
        self.textBrowser.clear()

    def stopOperation(self):
        if hasattr(self, 'extractionThread') and self.extractionThread.isRunning():
            self.extractionThread.stop()

def get_tab_widget():
    widget = URLExtractorApp()
    return widget
