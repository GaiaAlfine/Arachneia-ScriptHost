import sys, os, subprocess, pkg_resources, shutil, platform
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QTabBar, QStyleFactory, QFileDialog, QWidget, QAction, QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QListWidget, QMessageBox
from PyQt5.QtGui import QPalette, QColor, QIcon, QDesktopServices
from PyQt5.QtCore import QSize, QUrl

##DO NOT DELETE THIS. THIS IS THE CODE TO RUN IN THE TURMINAL TO CRATE AN EXE FILE THAT WORKS.
#pyinstaller --noconsole --windowed --icon=icons/Arachneia.ico --hidden-import=markdown --add-data "icons;icons" --add-data "scripts;scripts" Arachneia.pyw

# Configuration paths and application version
if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
else:
    application_path = os.path.dirname(os.path.abspath(__file__))

App_icon_path = os.path.join(application_path,'icons', 'Arachneia.ico')
icon_path = os.path.join(application_path,'icons')
scripts_path = os.path.join(application_path,'scripts')
Ver = "V2.1.0"  # This is the version number for this application.

sys.argv += ['-platform', 'windows:darkmode=2']
app = QApplication(sys.argv)

def install_package(package_name):
    try:
        # Check if the package is already installed
        pkg_resources.get_distribution(package_name)
        print(f"{package_name} is already installed.")
    except pkg_resources.DistributionNotFound:
        # If not installed, install it using pip
        print(f"Installing {package_name}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])

backgroundColor = '#4d4d4d'
textColor = '#FFFFFF'
borderColor = '#8b8b8b'

def apply_dark_stylesheet():
    stylesheet = """
    QPushButton{
        border: 1px solid #8b8b8b;
        background: #4d4d4d;
        padding: 10px;
        opacity: 50;
    }
    QPushButton::hover{
        border: 1px solid #8b8b8b;
        background: #5d5d5d;
        padding: 10px;
        opacity: 100;
    }
    QWidget {
        background-color: #4d4d4d;
        color: #ffffff;
    }
    QTabWidget::pane {
        border: 1px solid #8b8b8b;
        position: absolute;
        left: -1px;
    }

    QTabBar::tab {
        background-color: #4d4d4d;
        color: #FFFFFF;
        /* Add left padding or margin to move the tab to the right */
        padding-left: 1px; /* Adjust the value as needed */
        border-right: 1px solid #8b8b8b;
        border-top: 1px solid #8b8b8b;
        border-bottom: 1px solid #8b8b8b;
        border-left: 1px solid #8b8b8b;
    }
    QTabBar::tab:selected {
        /* Styles for selected tab */
        background-color: #4d4d4d;
        color: #ffffff;
        border-right: transparent;
    }

    QMenuBar {
        background-color: #4d4d4d;
        color: #FFFFFF;
    }
    QMenuBar::item:selected {
        background-color: #4d4d4d;
        color: #FFFFFF;
    }
    QMenu {
        background-color: #4d4d4d;
        color: #FFFFFF;
    }
    QMenu::item:selected {
        background-color: #4d4d4d;
        color: #FFFFFF;
    }
    QScrollBar:vertical {
        border: 1px solid #8b8b8b;
        background: #4d4d4d;
        width: 15px;
        margin: 22px 0 22px 0;
    }
    QScrollBar::handle:vertical {
        background: #4d4d4d;
        min-height: 20px;
    }
    QScrollBar::add-line:vertical {
        border: 1px solid #8b8b8b;
        background: #4d4d4d;
        height: 20px;
        subcontrol-position: bottom;
        subcontrol-origin: margin;
    }
    QScrollBar::sub-line:vertical {
        border: 1px solid #8b8b8b;
        background: #4d4d4d;
        height: 20px;
        subcontrol-position: top;
        subcontrol-origin: margin;
    }
    QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
        border: 1px solid #8b8b8b;
        width: 3px;
        height: 3px;
        background: #4d4d4d;
    }
    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
        background: none;
    }
    """
    app.setStyleSheet(stylesheet)


def convert_pyside2_to_pyqt5(script_path):
    with open(script_path, 'r') as file:
        script_code = file.read()
    
    # Basic replacements for common components and patterns
    replacements = {
        'from PySide2.QtCore import Signal': 'from PyQt5.QtCore import pyqtSignal',
        'from PySide2.QtCore import Slot': 'from PyQt5.QtCore import pyqtSlot',
        'from PySide2.QtWidgets': 'from PyQt5.QtWidgets',
        'from PySide2.QtGui': 'from PyQt5.QtGui',
        'from PySide2.QtCore': 'from PyQt5.QtCore',
        'PySide2.': 'PyQt5.'
    }
    
    # Apply replacements
    for old, new in replacements.items():
        script_code = script_code.replace(old, new)
    
    # Handle Signal and Slot if not explicitly imported
    script_code = script_code.replace('Signal', 'pyqtSignal')
    script_code = script_code.replace('Slot', 'pyqtSlot')
    
    # Additional specific replacements can be added here as needed
    # This could include handling specific method name differences or property changes
    
    return script_code

class SettingsWindow(QDialog):
    def __init__(self, mainWindow, scripts):
        super().__init__(mainWindow)
        self.mainWindow = mainWindow
        self.setWindowTitle('Settings')
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()
        self.scriptListWidget = QListWidget()
        layout.addWidget(QLabel('Scripts:'))
        layout.addWidget(self.scriptListWidget)

        for script in scripts:
            self.scriptListWidget.addItem(script)

        # Buttons for adding and removing scripts
        buttonsLayout = QHBoxLayout()
        # self.addButton = QPushButton('Add')
        self.removeButton = QPushButton('Remove')
        # buttonsLayout.addWidget(self.addButton)
        buttonsLayout.addWidget(self.removeButton)
        layout.addLayout(buttonsLayout)

        # self.addButton.clicked.connect(self.addScript)
        self.removeButton.clicked.connect(self.removeSelectedScript)

        closeButton = QPushButton('Close')
        closeButton.clicked.connect(self.close)
        layout.addWidget(closeButton)

        self.setLayout(layout)

    def removeSelectedScript(self):
        listItems = self.scriptListWidget.selectedItems()
        if not listItems: return
        for item in listItems:
            self.scriptListWidget.takeItem(self.scriptListWidget.row(item))
            self.mainWindow.removeScript(item.text())
            
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
        self.setWindowIcon(QIcon(App_icon_path))
        self.resize(1000, 600)
        
        self.tabWidget = QTabWidget(self)
        self.setCentralWidget(self.tabWidget)
        
        # Options bar setup
        self.menuBar = self.menuBar()
        self.fileMenu = self.menuBar.addMenu('&File')
        self.settingsMenu = self.menuBar.addMenu('&Settings')
        self.helpMenu = self.menuBar.addMenu('&Help')

        self.exitAction = QAction('&Exit', self)
        self.exitAction.triggered.connect(self.close)
        self.fileMenu.addAction(self.exitAction)

        self.settingsAction = QAction('&Remove Scripts', self)
        self.settingsAction.triggered.connect(self.openSettings)
        self.settingsMenu.addAction(self.settingsAction)

        # New action to open a link
        self.openLinkAction = QAction('&About', self)
        self.openLinkAction.triggered.connect(lambda: self.openLink("https://github.com/GaiaAlfine/Arachneia-ScriptHost"))
        self.helpMenu.addAction(self.openLinkAction)

        self.tab_widget = QTabWidget(self)
        self.setCentralWidget(self.tab_widget)

        self.tab_widget.setTabBar(RotatedTabBar())
        self.tab_widget.setTabPosition(QTabWidget.West)

        self.addHomeTab()

        self.tab_widget.addTab(QWidget(), "+")
        self.tab_widget.tabBarClicked.connect(self.tabClicked)
        self.scripts = []  # For storing script paths
        
        # Load scripts from the scripts folder at startup
        self.loadScriptsFromFolder()

    # Method to open a link
    def openLink(self, url):
        QDesktopServices.openUrl(QUrl(url))

    # New method to load scripts from the scripts folder
    def loadScriptsFromFolder(self):
        if os.path.exists(scripts_path):
            for script_file in os.listdir(scripts_path):
                if script_file.endswith(".py"):
                    full_path = os.path.join(scripts_path, script_file)
                    self.addTabFromScript(full_path)
        else:
            print(f"The scripts folder at {scripts_path} does not exist.")        

    # Method to add the Home tab
    def addHomeTab(self):
        homeTabContent = QWidget()  # Create the widget for the tab content
        homeLayout = QVBoxLayout(homeTabContent)  # Set a layout for this widget

        # Add content to the home tab here, for example, a welcome label
        welcomeLabel = QLabel("Welcome to Arachneia!")
        homeLayout.addWidget(welcomeLabel)

        # Add more widgets to homeLayout as needed

        # Add the tab to the tab widget
        self.tab_widget.insertTab(0, homeTabContent, "Home")

    def tabClicked(self, index):
        if self.tab_widget.tabText(index) == "+":
            filename, _ = QFileDialog.getOpenFileName(self, "Open Script", "", "Python Scripts (*.py)")
            if filename:
                self.addTabFromScript(filename)

    def addTabFromScript(self, filename):
        script_name = os.path.basename(filename)[:-3]
        try:
            if filename not in self.scripts:  # Check if the script is not already added
                # Determine the target path for the script in the scripts folder
                target_script_path = os.path.join(scripts_path, os.path.basename(filename))
                
                # Copy the script to the scripts folder if it's not already there
                if not os.path.exists(target_script_path):
                    shutil.copy(filename, scripts_path)
                    print(f"Copied {filename} to {scripts_path}")
                
                # Convert PySide2 script to PyQt5 dynamically
                script_code = convert_pyside2_to_pyqt5(filename)
                
                # Custom image loader with fallback
                def custom_image_loader(image_path, default_text):
                    if os.path.exists(image_path):
                        return QIcon(image_path)  # or however you load images
                    else:
                        # Fallback: return a placeholder or text
                        print(f"Image not found: {image_path}, using default text.")
                        return default_text
                
                # Prepare the execution environment with the custom image loader
                exec_globals = {
                    'custom_image_loader': custom_image_loader,
                }
                exec(script_code, exec_globals)
                
                # Now, use the globals dictionary to access the script's content
                if 'get_tab_widget' in exec_globals:
                    tab_content = exec_globals['get_tab_widget']()
                else:
                    tab_content = QWidget()

                # Check for a corresponding icon in the icons folder
                icon_filename = os.path.join(icon_path, script_name + ".png")
                if os.path.exists(icon_filename):
                    # If the icon exists, set it for the tab
                    tab_index = self.tab_widget.insertTab(self.tab_widget.count() - 1, tab_content, "")
                    self.tab_widget.setTabIcon(tab_index, QIcon(icon_filename))
                else:
                    # If no icon is found, set the script name as the tab label
                    tab_index = self.tab_widget.insertTab(self.tab_widget.count() - 1, tab_content, script_name)

                self.tab_widget.setCurrentIndex(tab_index)
                self.scripts.append(filename)  # Add the script to the list
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error loading script {script_name}: {str(e)}")
            print(f"Error loading script {script_name}: {e}")



    # Assuming the issue might be with reinitialization or improper access, ensure that your QTabWidget is always valid
    def removeScript(self, filename):
        if filename in self.scripts:
            # Attempt to remove the script file from the scripts folder
            try:
                target_script_path = os.path.join(scripts_path, os.path.basename(filename))
                if os.path.exists(target_script_path):
                    os.remove(target_script_path)
                    print(f"Removed {target_script_path} from the scripts folder.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error removing script file {os.path.basename(filename)}: {str(e)}")
                print(f"Error removing script file {os.path.basename(filename)}: {e}")

            # Remove the script from the application's list of scripts
            self.scripts.remove(filename)

            # Remove the corresponding tab from the GUI
            for i in range(self.tab_widget.count() - 1, -1, -1):
                if self.tab_widget.tabText(i) == os.path.basename(filename)[:-3]:
                    self.tab_widget.removeTab(i)
                    break



    def openSettings(self):
        """Opens the settings window, passing in the current scripts and a reference to self."""
        self.settingsWindow = SettingsWindow(self, self.scripts)
        self.settingsWindow.show()

if __name__ == "__main__":
    QApplication.setStyle(QStyleFactory.create('Fusion'))
    apply_dark_stylesheet()
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
