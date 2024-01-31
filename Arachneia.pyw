import sys
import threading
import os
import re
from PySide2.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QSizePolicy, QTabBar, QFileDialog, QTextBrowser, QProgressBar, QHBoxLayout
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
            QIcon('Arachneia/icons/dateTranslator.ico'),
            QIcon('Arachneia/icons/'),
            QIcon('Arachneia/icons/'),
            QIcon('Arachneia/icons/'),
            QIcon('Arachneia/icons/'),
            QIcon('Arachneia/icons/'),
            QIcon('Arachneia/icons/'),
            QIcon('Arachneia/icons/')
        ]

        # Add tabs with icons
        for i in range(10):
            tab = QWidget()
            self.tab_widget.addTab(tab, icons[i], "")  # Empty string for no text

        self.setCentralWidget(self.tab_widget)
        self.setWindowTitle("Arachneia V0.05")
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
        self.setupTab(1, self.runTabTwoScript)

    def setupTabThree(self):
        """Sets up content for Tab Three."""
        self.setupTab(2, self.runTabThreeScript)

    def setupTabFour(self):
        """Sets up content for Tab Four."""
        self.setupTab(3, self.runTabFourScript)

    def setupTabFive(self):
        """Sets up content for Tab Four."""
        self.setupTab(4, self.runTabFourScript)

    def setupTabSix(self):
        """Sets up content for Tab Four."""
        self.setupTab(5, self.runTabFourScript)

    def setupTabSeven(self):
        """Sets up content for Tab Four."""
        self.setupTab(6, self.runTabFourScript)

    def setupTabEight(self):
        """Sets up content for Tab Four."""
        self.setupTab(7, self.runTabFourScript)

    def setupTabNine(self):
        """Sets up content for Tab Four."""
        self.setupTab(8, self.runTabFourScript)

    def setupTabTen(self):
        """Sets up content for Tab Four."""
        self.setupTab(9, self.runTabFourScript)

    def setupTab(self, index, script_function):
        """General method to set up a tab."""
        tab = self.tab_widget.widget(index)
        layout = QVBoxLayout(tab)
        script_function()

    def runTabOneScript(self):
        # Your script here
        pass

    def runTabTwoScript(self):
        # Your script here
        pass

    def runTabThreeScript(self):
        # Your script here
        pass

    def runTabFourScript(self):
        # Your script here
        pass

    def runTabFiveScript(self):
        # Your script here
        pass

    def runTabSixScript(self):
        # Your script here
        pass

    def runTabSevenScript(self):
        # Your script here
        pass

    def runTabEightScript(self):
        # Your script here
        pass

    def runTabNineScript(self):
        # Your script here
        pass
    
    def runTabTenScript(self):
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