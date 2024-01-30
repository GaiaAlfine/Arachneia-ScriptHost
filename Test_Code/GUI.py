import sys
import threading
import os
import re
from PySide2.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QSizePolicy, QTabBar, QFileDialog, QTextBrowser
from PySide2.QtGui import QPalette, QColor, QIcon, QDesktopServices
from PySide2.QtCore import Qt, QSize

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
            QIcon('Arachneia/Arachneia.ico'),
            QIcon('Arachneia/Arachneia.ico'),
            QIcon('Arachneia/Arachneia.ico'),
            QIcon('Arachneia/Arachneia.ico'),
            QIcon('Arachneia/Arachneia.ico'),
            QIcon('Arachneia/Arachneia.ico'),
            QIcon('Arachneia/Arachneia.ico'),
            QIcon('Arachneia/Arachneia.ico'),
            QIcon('Arachneia/Arachneia.ico'),
            QIcon('Arachneia/Arachneia.ico')
        ]

        # Add tabs with icons
        for i in range(10):
            tab = QWidget()
            self.tab_widget.addTab(tab, icons[i], "")  # Empty string for no text

        self.setCentralWidget(self.tab_widget)
        self.setWindowTitle("Arachneia V0.04")
        self.resize(1000, 600)
        self.setWindowIcon(QIcon('Arachneia/Arachneia.ico'))
        self.tab_widget.currentChanged.connect(self.loadTab)
        self.setupTabOne()

    def loadTab(self, index):
        """Load the content of the tab when it's selected."""
        if index == 0 and not self.tab_widget.widget(index).layout():
            self.setupTabOne()
        elif index == 1 and not self.tab_widget.widget(index).layout():
            self.setupTabTwo()
        elif index == 2 and not self.tab_widget.widget(index).layout():
            self.setupTabThree()
        elif index == 3 and not self.tab_widget.widget(index).layout():
            self.setupTabFour()
        elif index == 4 and not self.tab_widget.widget(index).layout():
            self.setupTabFive()
        elif index == 5 and not self.tab_widget.widget(index).layout():
            self.setupTabSix()
        elif index == 6 and not self.tab_widget.widget(index).layout():
            self.setupTabSeven()
        elif index == 7 and not self.tab_widget.widget(index).layout():
            self.setupTabEight()
        elif index == 8 and not self.tab_widget.widget(index).layout():
            self.setupTabNine()
        elif index == 9 and not self.tab_widget.widget(index).layout():
            self.setupTabTen()

    def setupTabOne(self):
        """Sets up content for Tab One."""
        self.setupTab(0, self.runTabOneScript)

    def setupTabTwo(self):
        """Sets up content for Tab Two."""
        self.setupTab(1, "Tab Two", self.runTabTwoScript)

    def setupTabThree(self):
        """Sets up content for Tab Three."""
        self.setupTab(2, "Tab Three", self.runTabThreeScript)

    def setupTabFour(self):
        """Sets up content for Tab Four."""
        self.setupTab(3, "Tab Four", self.runTabFourScript)

    def setupTabFive(self):
        """Sets up content for Tab Four."""
        self.setupTab(4, "Tab Four", self.runTabFourScript)

    def setupTabSix(self):
        """Sets up content for Tab Four."""
        self.setupTab(5, "Tab Four", self.runTabFourScript)

    def setupTabSeven(self):
        """Sets up content for Tab Four."""
        self.setupTab(6, "Tab Four", self.runTabFourScript)

    def setupTabEight(self):
        """Sets up content for Tab Four."""
        self.setupTab(7, "Tab Four", self.runTabFourScript)

    def setupTabNine(self):
        """Sets up content for Tab Four."""
        self.setupTab(8, "Tab Four", self.runTabFourScript)

    def setupTabTen(self):
        """Sets up content for Tab Four."""
        self.setupTab(9, "Tab Four", self.runTabFourScript)

    def setupTab(self, index, script_function):
        """General method to set up a tab."""
        tab = self.tab_widget.widget(index)
        layout = QVBoxLayout(tab)
        script_function()

    def runTabOneScript(self):
        
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
        
    def runTabTwoScript(self):
        # Your code for Tab Two script here
        pass

    def runTabThreeScript(self):
        # Your code for Tab Three script here
        pass

    def runTabFourScript(self):
        # Your code for Tab four script here
        pass

    def runTabFiveScript(self):
        # Your code for Tab four script here
        pass

    def runTabSixScript(self):
        # Your code for Tab four script here
        pass

    def runTabSevenScript(self):
        # Your code for Tab four script here
        pass

    def runTabEightScript(self):
        # Your code for Tab four script here
        pass

    def runTabNineScript(self):
        # Your code for Tab four script here
        pass
    
    def runTabTenScript(self):
        # Your code for Tab four script here
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