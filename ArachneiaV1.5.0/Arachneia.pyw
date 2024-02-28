import sys, os, subprocess, pkg_resources, shutil, importlib.util, glob
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QTabBar, QStyleFactory, QFileDialog, QWidget, QAction, QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QListWidget, QMessageBox
from PyQt5.QtGui import QPalette, QColor, QIcon
from PyQt5.QtCore import QSize

##DO NOT DELETE THIS. THIS IS THE CODE TO RUN IN THE TURMINAL TO CRATE AN EXE FILE THAT WORKS.
#pyinstaller --noconsole --windowed --icon=icons/Arachneia.ico --hidden-import=markdown --add-data "icons;icons" --add-data "scripts;scripts" Arachneia.pyw

# Configuration paths and application version
if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
else:
    application_path = os.path.dirname(os.path.abspath(__file__))

icon_path = os.path.join(application_path,'_internal', 'icons', 'Arachneia.ico')
scripts_path = os.path.join(application_path,'_internal', 'scripts')
Ver = "V2.0.0"  # This is the version number for this application.

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



def dark_palette():
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, QColor(220, 220, 220))
    palette.setColor(QPalette.Base, QColor(35, 35, 35))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, QColor(25, 25, 25))
    palette.setColor(QPalette.ToolTipText, QColor(220, 220, 220))
    palette.setColor(QPalette.Text, QColor(220, 220, 220))
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, QColor(220, 220, 220))
    palette.setColor(QPalette.BrightText, QColor(255, 255, 255))
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))
    palette.setColor(QPalette.Disabled, QPalette.Text, QColor(128, 128, 128))
    palette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(105, 105, 105))
    palette.setColor(QPalette.Disabled, QPalette.WindowText, QColor(128, 128, 128))
    return palette

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

def load_scripts_from_folder(scripts_folder):
    script_modules = []
    for script_path in glob.glob(os.path.join(scripts_folder, '*.py')):
        module_name = os.path.basename(script_path)[:-3]
        spec = importlib.util.spec_from_file_location(module_name, script_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        script_modules.append(module)
    return script_modules

def copy_script_to_folder(self, source_path, destination_folder=scripts_path):
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    shutil.copy(source_path, destination_folder)

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

    def addScript(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open Script", "", "Python Scripts (*.py)")
        if filename:
            self.scriptListWidget.addItem(filename)
            self.mainWindow.addScript(filename)

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
        self.setWindowIcon(QIcon(icon_path))
        self.resize(1000, 600)
        
        self.tabWidget = QTabWidget(self)
        self.setCentralWidget(self.tabWidget)

        # Options bar setup
        self.menuBar = self.menuBar()
        self.fileMenu = self.menuBar.addMenu('&File')
        self.settingsMenu = self.menuBar.addMenu('&Settings')
        self.helpMenu = self.menuBar.addMenu('&Help')

        # Example actions
        self.exitAction = QAction('&Exit', self)
        self.exitAction.triggered.connect(self.close)
        self.fileMenu.addAction(self.exitAction)

        # Settings action
        self.settingsAction = QAction('&Remove Scripts', self)
        self.settingsAction.triggered.connect(self.openSettings)
        self.settingsMenu.addAction(self.settingsAction)

        # About action (placeholder)
        self.aboutAction = QAction('&About', self)
        # Connect this action to the appropriate method for showing about information
        self.helpMenu.addAction(self.aboutAction)
        
        self.tab_widget = QTabWidget(self)
        self.setCentralWidget(self.tab_widget)

        self.tab_widget.setTabBar(RotatedTabBar())
        self.tab_widget.setTabPosition(QTabWidget.West)

        # Call the method to add the Home tab
        self.addHomeTab()

        self.tab_widget.addTab(QWidget(), "+")
        self.tab_widget.tabBarClicked.connect(self.tabClicked)
        self.loadAndDisplayScripts()
        self.scripts = []  # For storing script paths
        

    def loadAndDisplayScripts(self):
        self.scripts = load_scripts_from_folder(scripts_path)
        # Assuming you have a method to display these scripts or add tabs for them
        for script_module in self.scripts:
            # Use the script_module to add tabs or functionality
            print(f"Loaded script module: {script_module}")

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
                    
                tab_index = self.tab_widget.insertTab(self.tab_widget.count() - 1, tab_content, script_name)
                self.tab_widget.setCurrentIndex(tab_index)
                
                self.scripts.append(filename)  # Add the script to the list
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error loading script {script_name}: {str(e)}")
            print(f"Error loading script {script_name}: {e}")



    def addScript(self, filename):
        """Adds a script to the application and opens a tab for it."""
        # Copy the script to the scripts folder
        self.copy_script_to_folder(filename, scripts_path)
        # Now, load and add the script as a tab
        if filename not in self.scripts:
            self.scripts.append(filename)
            self.addTabFromScript(filename)

    # Assuming the issue might be with reinitialization or improper access, ensure that your QTabWidget is always valid
    def removeScript(self, filename):
        if filename in self.scripts:
            self.scripts.remove(filename)
            for i in range(self.tab_widget.count() - 1, -1, -1):  # Note: Adjusted to iterate correctly
                if self.tab_widget.tabText(i) == os.path.basename(filename)[:-3]:  # Assuming script_name is used as tabText
                    self.tab_widget.removeTab(i)
                    break


    def openSettings(self):
        """Opens the settings window, passing in the current scripts and a reference to self."""
        self.settingsWindow = SettingsWindow(self, self.scripts)
        self.settingsWindow.show()

if __name__ == "__main__":
    QApplication.setStyle(QStyleFactory.create('Fusion'))
    app.setPalette(dark_palette())
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())