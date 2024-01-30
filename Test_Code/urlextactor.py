import sys
import re
import os
from PySide2.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QTextBrowser, QVBoxLayout, QWidget, QLabel, QProgressBar, QHBoxLayout
from PySide2.QtGui import QDesktopServices
from PySide2.QtCore import Qt

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

        # Create a progress bar (assuming you want a visual progress indicator)
        self.progressBar = QProgressBar()

        # Modify textBrowser to display URLs
        self.textBrowser = QTextBrowser()
        self.textBrowser.setPlaceholderText("Extracted URLs will be displayed here.")

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

    def clearText(self):
        # Clear the text from the QTextBrowser
        self.textBrowser.clear()

    def stopOperation(self):
        # You would implement whatever you need to stop the operation here
        # This is dependent on how your URL extraction is implemented
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = URLExtractorApp()
    mainWin.show()
    sys.exit(app.exec_())