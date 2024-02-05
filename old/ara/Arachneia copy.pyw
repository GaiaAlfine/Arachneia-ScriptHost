import sys
import json
import importlib
from PySide2.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QTabBar
from PySide2.QtGui import QPalette, QColor, QIcon
from PySide2.QtCore import QSize, Qt
import sys
sys.path.append('/Arachneia/scripts')

def dark_palette():
    '''Creates a dark palette for the application.'''
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
    return palette

class RotatedTabBar(QTabBar):
    '''Custom tab bar with rotated tabs.'''
    def tabSizeHint(self, index):
        return QSize(100, 100)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setIconSize(QSize(80, 80))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.loadScripts()  # Load scripts from JSON
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabBar(RotatedTabBar())
        self.tab_widget.setTabPosition(QTabWidget.West)

        for script in self.scripts:
            self.addDynamicTab(script)

        self.setCentralWidget(self.tab_widget)
        self.setWindowTitle("Dynamic GUI Tabs")
        self.resize(1000, 600)

    def loadScripts(self):
        '''Load script configurations from a JSON file.'''
        with open('Arachneia/scripts/scripts.json', 'r') as f:
            self.scripts = json.load(f)

    def addDynamicTab(self, script):
        try:
            module = importlib.import_module(script["path"])
            gui_entry = getattr(module, script["gui_entry"])()
            if isinstance(gui_entry, QWidget):
                tab = QWidget()
                layout = QVBoxLayout(tab)
                layout.addWidget(gui_entry)  # Add the script's GUI component to the layout

                self.tab_widget.addTab(tab, QIcon(script.get("icon", "")), script["name"])
            else:
                print(f"Error: {script['name']} does not provide a QWidget.")
        except Exception as e:
            print(f"Error loading {script['name']}: {e}")



if __name__ == "__main__":
    app = QApplication.instance() if QApplication.instance() else QApplication(sys.argv)
    app.setPalette(dark_palette())
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
