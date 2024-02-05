import sys
import os
import json
from PySide2.QtWidgets import QApplication, QMainWindow, QTabWidget, QTabBar, QStyleFactory, QMessageBox
from PySide2.QtGui import QPalette, QColor, QIcon
from PySide2.QtCore import QSize

Ver = "V0.3.0" # This is the version number for this application.

sys.argv += ['-platform', 'windows:darkmode=2']
app = QApplication(sys.argv)

def dark_palette():
    '''Enhance the dark palette for the application to ensure dark mode in tabs.'''
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
        return QSize(100, 100)  # Set a fixed size for each tab
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setIconSize(QSize(80, 80))  # Adjust the size as needed

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"Arachneia - {Ver}")
        self.setWindowIcon(QIcon('Arachneia/icons/Arachneia.ico'))
        self.resize(1000, 600)
        
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabBar(RotatedTabBar())  
        self.tab_widget.setTabPosition(QTabWidget.West)  
        
        self.loadTabsFromConfig()
        
        self.setCentralWidget(self.tab_widget)

    def loadTabsFromConfig(self):
        config_path = 'Arachneia/tab_config.json'
        if not os.path.exists(config_path):
            print("Configuration file not found.")
            return
        
        with open(config_path, 'r') as config_file:
            tab_config = json.load(config_file)
        
        for tab_info in tab_config:
            self.addTabFromInfo(tab_info)
    
    def addTabFromInfo(self, tab_info):
        try:
            # Attempt to dynamically import the module specified in the config
            script_module = __import__(f"scripts.{tab_info['script']}", fromlist=[''])
            
            # Assume the module provides a function or class that returns a QWidget
            tab_content = script_module.get_tab_widget()  # Ensure this function is defined in each script module
            
            icon_path = tab_info.get('icon', '')
            tab_text = tab_info.get('name', 'Unnamed Tab')
            
            if os.path.exists(icon_path):
                icon = QIcon(icon_path)
                tab_index = self.tab_widget.addTab(tab_content, icon, "")  # Set text to empty if icon exists
            else:
                icon = QIcon()  # Use a default icon or none
                tab_index = self.tab_widget.addTab(tab_content, icon, tab_text)  # Set text if no icon exists
            
            self.tab_widget.setTabToolTip(tab_index, tab_text)
        
        except ImportError as e:
            error_message = (f"Failed to import script module '{tab_info['script']}': {e}.\n\n"
                            "Possible reasons and fixes:\n"
                            "- The script file is missing in the 'scripts' folder.\n"
                            "- There's a typo in the script name in your configuration file.\n"
                            "- The script does not have an '__init__.py' file in its directory (if it's a package).\n"
                            "\nPlease ensure the script exists, is correctly named, and is in the right location.")
            QMessageBox.critical(self, "Import Error", error_message)
        except AttributeError as e:
            error_message = (f"Script module '{tab_info['script']}' does not have a 'get_tab_widget' function: {e}.\n\n"
                            "To fix this issue:\n"
                            "- Ensure the script defines a 'get_tab_widget' function that returns a QWidget instance.\n"
                            "- Check for typos in the function name.\n"
                            "- Ensure the function is properly defined at the top level of the module.")
            QMessageBox.critical(self, "Attribute Error", error_message)



if __name__ == "__main__":
    QApplication.setStyle(QStyleFactory.create('Fusion'))
    app.setPalette(dark_palette())
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())