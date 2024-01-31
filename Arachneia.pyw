import sys
import threading
import os
import re
from PySide2.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel, QPushButton, QTabBar, QFileDialog, QTextBrowser, QProgressBar, QHBoxLayout
from PySide2.QtGui import QPalette, QColor, QIcon, QDesktopServices
from PySide2.QtCore import Qt, QSize, QThread, Signal

sys.argv += ['-platform', 'windows:darkmode=2']
app = QApplication(sys.argv)

def dark_palette():
    '''Create a dark palette for the application.'''
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    palette.setColor(QPalette.Disabled, QPalette.Text, QColor(127, 127, 127))
    palette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(127, 127, 127))
    palette.setColor(QPalette.Disabled, QPalette.WindowText, QColor(127, 127, 127))
    return palette

class RotatedTabBar(QTabBar):
    def tabSizeHint(self, index):
        # Set a fixed size of 100x100 pixels for each tab
        return QSize(100, 100)

    def __init__(self, parent=None):
        super().__init__(parent)
        # Adjust icon size to fit within the 100x100 pixel tab
        self.setIconSize(QSize(80, 80))  # Adjust the size as needed


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabBar(RotatedTabBar())  # Use the custom tab bar
        self.tab_widget.setTabPosition(QTabWidget.West)  # Move tabs to the left

        # Icons for tabs (replace 'icon_path' with the actual path to your icon files)
        icons = [
            QIcon('Arachneia/icons/'),
            QIcon('Arachneia/icons/UrlExtactor.ico'),
            QIcon('Arachneia/icons/dateTranslator.ico')
        ]

        # Add tabs with icons
        for i in range(3):
            tab = QWidget()
            self.tab_widget.addTab(tab, icons[i], "")  # Empty string for no text

        self.setCentralWidget(self.tab_widget)
        self.setWindowTitle("Arachneia V0.1")
        self.resize(1000, 600)
        self.setWindowIcon(QIcon('Arachneia/Arachneia.ico'))
        self.tab_widget.currentChanged.connect(self.loadTab)
        self.setupTabOne()

    

    def loadTab(self, index):
        """Load the content of the tab when it's selected."""
        print(f"Tab {index + 1} selected!")  
        if index == 0 and not self.tab_widget.widget(index).layout():
            self.setupTabOne()
        elif index == 1 and not self.tab_widget.widget(index).layout():
            self.setupTabTwo()
        elif index == 2 and not self.tab_widget.widget(index).layout():
            self.setupTabThree()

    def setupTabOne(self):
        """Sets up content for Tab One."""
        self.runTabOneScript()

    def setupTabTwo(self):
        """Sets up content for Tab Two."""
        self.runTabTwoScript()

    def setupTabThree(self):
        """Sets up content for Tab Three."""
        self.runTabThreeScript()

    def setupTab(self, index, script_function):
        """General method to set up a tab."""
        tab = self.tab_widget.widget(index)
        layout = QVBoxLayout(tab)
        script_function()

    def runTabOneScript(self):
        pass

    def runTabTwoScript(self):
        class URLExtractionThread(QThread):
            url_found = Signal(str)
            progress_updated = Signal(int)
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
                # Create a central widget for the QMainWindow
                centralWidget = QWidget(self)
                layout = QVBoxLayout(centralWidget)

                # Title text at the top, use a QLabel for this
                self.titleLabel = QLabel('URL Extractor')
                self.titleLabel.setAlignment(Qt.AlignCenter)

                # Create buttons
                self.btnSelect = QPushButton('Select')
                self.btnExport = QPushButton('Export')
                self.btnClear = QPushButton('Clear')
                self.btnStop = QPushButton('Stop')

                # Create a progress bar and hide the percentage text
                self.progressBar = QProgressBar()
                self.progressBar.setTextVisible(False)  # Hide the percentage text

                # Text browser to display URLs
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

                # Set the central widget for the QMainWindow with the layout
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

        # Use the existing tab for Tab Two
        tab_two = self.tab_widget.widget(1)
        layout = QVBoxLayout(tab_two)

        # Create an instance of URLExtractorApp and set it up
        self.urlExtractorApp = URLExtractorApp()
        layout.addWidget(self.urlExtractorApp)

        # Set the layout for the tab
        tab_two.setLayout(layout)

    def runTabThreeScript(self):
        # Your script here
        pass

    def runScriptWithTimeout(self, script, timeout):

        """Run a script with a timeout to avoid freezing."""
        def target():
            # Here you can call your script
            pass

        thread = threading.Thread(target=target)
        thread.start()
        thread.join(timeout)
        if thread.is_alive():
            print("Script took too long to run and was terminated.")
            thread.terminate()

if __name__ == "__main__":
    app.setPalette(dark_palette())  # This line applies the dark palette to the application.
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())