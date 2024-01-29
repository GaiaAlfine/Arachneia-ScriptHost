import sys
import re
import os
from PySide2.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QTextBrowser, QVBoxLayout, QWidget
from PySide2.QtGui import QDesktopServices
from PySide2.QtCore import QUrl, Qt

class URLExtractorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('URL Extractor')
        self.setGeometry(300, 300, 600, 400)

        layout = QVBoxLayout()

        self.textBrowser = QTextBrowser()
        self.btnLoad = QPushButton('Load File')
        self.btnSave = QPushButton('Save URLs')

        layout.addWidget(self.textBrowser)
        layout.addWidget(self.btnLoad)
        layout.addWidget(self.btnSave)

        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

        self.btnLoad.clicked.connect(self.loadFile)
        self.btnSave.clicked.connect(self.saveFile)

        # Connect the anchorClicked signal to openUrl
        self.textBrowser.anchorClicked.connect(self.openUrl)
        # Set this to ensure QTextBrowser doesn't try to open links internally
        self.textBrowser.setOpenLinks(False)



    def loadFile(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder_path:
            all_formatted_entries = []
            print(f"Selected folder: {folder_path}")  # Debugging output
            for root, dirs, files in os.walk(folder_path):
                for filename in files:
                    if filename.endswith(".txt"):
                        file_path = os.path.join(root, filename)
                        folder_url = f'file:///{root}'  # URL for the folder
                        try:
                            with open(file_path, 'r', encoding='utf-8') as file:
                                content = file.read()
                                urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', content)
                                if urls:
                                    # Apply inline CSS to change the color to orange
                                    formatted_entry = f'<a href="{folder_url}" style="color: #c77100;">From {filename} in [{root}]</a>:<br>' + '<br>'.join([f'<a href="{url}">{url}</a>' for url in urls]) + '<br><br>'
                                    all_formatted_entries.append(formatted_entry)
                                print(f"Found URLs in {filename}: {urls}")
                        except UnicodeDecodeError:
                            print(f"Could not read {filename} due to encoding issue")

            # Set formatted URLs and clickable file paths with color styling as HTML in the QTextBrowser
            self.textBrowser.setHtml(''.join(all_formatted_entries))
            print("Final URL list:", all_formatted_entries)


    def saveFile(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Text Files (*.txt);;All Files (*)")
        if file_name:
            # Write URLs to the selected file, getting plain text from the QTextBrowser
            with open(file_name, 'w') as file:
                file.write(self.textBrowser.toPlainText())

    def openUrl(self, url):
        # Open the URL in the default web browser and prevent default action
        QDesktopServices.openUrl(url)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = URLExtractorApp()
    mainWin.show()
    sys.exit(app.exec_())