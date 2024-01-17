import sys
import threading
from PySide2.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel
from PySide2.QtGui import QPalette, QColor, QIcon
from PySide2.QtCore import Qt

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

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tab_widget = QTabWidget()
        # Add tabs
        self.tab_widget.addTab(QWidget(), "Tab One")
        self.tab_widget.addTab(QWidget(), "Tab Two")
        self.tab_widget.addTab(QWidget(), "Tab Three")
        self.tab_widget.addTab(QWidget(), "Tab Four")
        self.setCentralWidget(self.tab_widget)
        self.setWindowTitle("Arachneia V0.03")
        self.resize(400, 600)

        # Set the window icon
        self.setWindowIcon(QIcon('Arachneia/Arachneia.ico'))  # Replace 'path_to_your_icon_file' with the actual path to your icon file.

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

    def setupTabOne(self):
        """Sets up content for Tab One."""
        self.setupTab(0, "Tab One", self.runTabOneScript)

    def setupTabTwo(self):
        """Sets up content for Tab Two."""
        self.setupTab(1, "Tab Two", self.runTabTwoScript)

    def setupTabThree(self):
        """Sets up content for Tab Three."""
        self.setupTab(2, "Tab Three", self.runTabThreeScript)

    def setupTabFour(self):
        """Sets up content for Tab Four."""
        self.setupTab(3, "Tab Four", self.runTabFourScript)

    def setupTab(self, index, label_text, script_function):
        """General method to set up a tab."""
        tab = self.tab_widget.widget(index)
        layout = QVBoxLayout(tab)
        label = QLabel(label_text)
        layout.addWidget(label)
        script_function()

    def runTabOneScript(self):
        # Your code for Tab One script here
        pass

    def runTabTwoScript(self):
        # Your code for Tab Two script here
        pass

    def runTabThreeScript(self):
        # Your code for Tab Three script here
        pass

    def runTabFourScript(self):
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