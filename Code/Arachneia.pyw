import sys
import os
import importlib.util
import glob
from PySide2.QtWidgets import QApplication, QMainWindow, QTabWidget, QTabBar, QStyleFactory, QMessageBox
from PySide2.QtGui import QPalette, QColor, QIcon
from PySide2.QtCore import QSize


##DO NOT DELETE THIS. THIS IS THE CODE TO RUN IN THE TURMINAL TO CRATE AN EXE FILE THAT WORKS.
#pyinstaller --onefile --noconsole --windowed --icon=icons/Arachneia.ico --add-data "scripts;scripts" Arachneia.pyw

#this also works but when i insert a markdown script the program crahes. 
#pyinstaller --onefile --noconsole --windowed --icon=icons/Arachneia.ico --add-data "scripts;scripts" --hidden-import=markdown Arachneia.pyw

# Configuration paths and application version
if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
else:
    application_path = os.path.dirname(os.path.abspath(__file__))

icon_path = os.path.join(application_path, 'icons', 'Arachneia.ico')
scripts_path = os.path.join(application_path, 'scripts')


Ver = "V1.1.0" # This is the version number for this application.

sys.argv += ['-platform', 'windows:darkmode=2']
app = QApplication(sys.argv)

def dark_palette():
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(35, 35, 35))
    palette.setColor(QPalette.WindowText, QColor(220, 220, 220))
    palette.setColor(QPalette.Base, QColor(18, 18, 18))
    palette.setColor(QPalette.AlternateBase, QColor(50, 50, 50))
    palette.setColor(QPalette.ToolTipBase, QColor(25, 25, 25))
    palette.setColor(QPalette.ToolTipText, QColor(220, 220, 220))
    palette.setColor(QPalette.Text, QColor(220, 220, 220))
    palette.setColor(QPalette.Button, QColor(50, 50, 50))
    palette.setColor(QPalette.ButtonText, QColor(220, 220, 220))
    palette.setColor(QPalette.BrightText, QColor(220, 220, 220))
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))
    palette.setColor(QPalette.Disabled, QPalette.Text, QColor(128, 128, 128))
    palette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(128, 128, 128))
    palette.setColor(QPalette.Disabled, QPalette.WindowText, QColor(128, 128, 128))
    return palette


class RotatedTabBar(QTabBar):
    def tabSizeHint(self, index):
        return QSize(100, 100)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setIconSize(QSize(80, 80))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"Arachneia - {Ver}")
        self.setWindowIcon(QIcon(icon_path))
        self.resize(1000, 600)
        
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabBar(RotatedTabBar())
        self.tab_widget.setTabPosition(QTabWidget.West)
        
        self.loadScriptsAsTabs()
        
        self.setCentralWidget(self.tab_widget)

    def loadScriptsAsTabs(self):
        script_files = glob.glob(os.path.join(scripts_path, "*.py"))
        for script_file in script_files:
            script_name = os.path.basename(script_file[:-3])  # Remove '.py' extension
            if script_name == "__init__":
                continue  # Skip __init__.py files
            self.addTabFromScript(script_name)

    def addTabFromScript(self, script_name):
        try:
            spec = importlib.util.spec_from_file_location(script_name, os.path.join(scripts_path, f"{script_name}.py"))
            script_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(script_module)

            tab_content = script_module.get_tab_widget()

            # Attempt to load an icon for the tab from the 'icons' folder
            icon_filename = getattr(script_module, 'TAB_ICON', f"{script_name}.png")  # Default to script_name.png if not specified
            icon_path = os.path.join(application_path, 'icons', icon_filename)

            if os.path.exists(icon_path):
                icon = QIcon(icon_path)
                tab_index = self.tab_widget.addTab(tab_content, icon, "")
            else:
                # If no icon is found, use a default icon or no icon
                tab_index = self.tab_widget.addTab(tab_content, QIcon(), script_name)  # Use script_name as fallback tab text

            self.tab_widget.setTabToolTip(tab_index, script_name)  # Use script_name as fallback tooltip

        except Exception as e:
            print(f"Error loading script {script_name}: {e}")
            # Handle errors or log them as needed


if __name__ == "__main__":
    QApplication.setStyle(QStyleFactory.create('Fusion'))
    app.setPalette(dark_palette())
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())