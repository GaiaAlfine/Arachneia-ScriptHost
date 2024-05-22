import sys, os, subprocess, pkg_resources, shutil
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QTabBar, QStyleFactory, QFileDialog, QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QListWidget, QMessageBox, QPlainTextEdit
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtCore import QSize, QUrl

##DO NOT DELETE THIS. THIS IS THE CODE TO RUN IN THE TERMINAL TO CREATE AN EXE FILE THAT WORKS.
#pyinstaller --noconsole --windowed --icon=icons/Arachneia.png --hidden-import=markdown --add-data "icons;icons" --add-data "scripts;scripts" Arachneia-ScriptHost.pyw

if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
else:
    application_path = os.path.dirname(os.path.abspath(__file__))

App_icon_path = os.path.join(application_path, 'icons', 'Arachneia.png')
icon_path = os.path.join(application_path, 'icons')
scripts_path = os.path.join(application_path, 'scripts')
Ver = "V0.8.1"

sys.argv += ['-platform', 'windows:darkmode=2']
app = QApplication(sys.argv)

def install_package(package_name):
    try:
        pkg_resources.get_distribution(package_name)
        print(f"{package_name} is already installed.")
    except pkg_resources.DistributionNotFound:
        print(f"Installing {package_name}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])

def apply_dark_stylesheet():
    stylesheet = """
    QPushButton{
        border: 1px solid #8b8b8b;
        background: #030021;
        padding: 10px;
        opacity: 50;
        border-radius: 5px;
    }
    QPushButton::hover{
        background: #141132;
        padding: 10px;
        opacity: 100;
    } 
    QPushButton:checked {
        background: #252253;
        padding: 10px;
        opacity: 100;
    } 
    QWidget {
        background-color: #030021;
        color: #ffffff;
    }
    QTabWidget::pane {
        border: 1px solid #8b8b8b;
        background-color: #030021;  /* Background color for the tab row */
        position: absolute;
        left: -1px;
        border-top: 1px solid #8b8b8b;
    }
    QTabBar::tab {
        background-color: #030021;
        color: #FFFFFF;
        padding-left: 1px; /* Adjust the value as needed */
        border-right: 1px solid #8b8b8b;
        border-bottom: 1px solid #8b8b8b;
        border-left: 1px solid #8b8b8b;
    }
    QTabBar::tab:first {
        border-top: 1px solid #8b8b8b;
    }
    QTabBar::tab:selected {
        background-color: #030021;
        color: #ffffff;
        border-right: transparent;
    }
    QTabBar {
        border-top: 1px solid #8b8b8b;
        background-color: #030021;  /* Background color for the tab row */
    }
    QMenuBar {
        background-color: #030021;
        color: #FFFFFF;
    }
    QMenuBar::item:selected {
        background-color: #4d4d4d;
        color: #FFFFFF;
    }
    QMenu {
        background-color: #030021;
        color: #FFFFFF;
    }
    QMenu::item:selected {
        background-color: #4d4d4d;
        color: #FFFFFF;
    }
    QTabBar::scroller {
        width: 0;
        height: 0;
    }
    QPlainTextEdit {
        border: 1px solid #8b8b8b;
        border-radius: 5px;
        padding: 5px;
        background-color: #141414;
        color: #ffffff;
    }
    QListWidget {
        border: 1px solid #8b8b8b;
    }
    """
    app.setStyleSheet(stylesheet)

def convert_pyside2_to_pyqt5(script_path):
    with open(script_path, 'r') as file:
        script_code = file.read()
    
    replacements = {
        'from PySide2.QtCore import Signal': 'from PyQt5.QtCore import pyqtSignal',
        'from PySide2.QtCore': 'from PyQt5.QtCore',
        'from PySide2.QtWidgets': 'from PyQt5.QtWidgets',
        'from PySide2.QtGui': 'from PyQt5.QtGui',
        'PySide2.': 'PyQt5.'
    }
    
    for old, new in replacements.items():
        script_code = script_code.replace(old, new)
    
    script_code = script_code.replace('Signal', 'pyqtSignal')
    script_code = script_code.replace('Slot', 'pyqtSlot')
    
    return script_code

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
        self.resize(1280, 720)
        
        self.scripts = []
        
        self.tabWidget = QTabWidget(self)
        self.setCentralWidget(self.tabWidget)

        self.tab_widget = QTabWidget(self)
        self.setCentralWidget(self.tab_widget)

        self.tab_widget.setTabBar(RotatedTabBar())
        self.tab_widget.setTabPosition(QTabWidget.West)
        
        self.addHomeTab()

        self.tab_widget.addTab(QWidget(), "+")
        self.tab_widget.tabBarClicked.connect(self.tabClicked)
        
        self.loadScriptsFromFolder()

    def openLink(self, url):
        QDesktopServices.openUrl(QUrl(url))

    def loadScriptsFromFolder(self):
        if os.path.exists(scripts_path):
            for script_file in os.listdir(scripts_path):
                if script_file.endswith(".py"):
                    full_path = os.path.join(scripts_path, script_file)
                    self.addTabFromScript(full_path)
        else:
            print(f"The scripts folder at {scripts_path} does not exist.")        

    def addHomeTab(self):
        homeTabContent = QWidget()
        homeLayout = QVBoxLayout(homeTabContent)

        contentLayout = QHBoxLayout()

        scriptLayout = QVBoxLayout()
        scriptLayout.addWidget(QLabel('Scripts:'))
        self.scriptListWidget = QListWidget()
        scriptLayout.addWidget(self.scriptListWidget)

        for script in self.scripts:
            self.scriptListWidget.addItem(script)

        self.removeButton = QPushButton('Remove')
        scriptLayout.addWidget(self.removeButton)

        self.removeButton.clicked.connect(self.removeSelectedScript)

        contentLayout.addLayout(scriptLayout)

        self.terminalOutput = QPlainTextEdit()
        self.terminalOutput.setReadOnly(True)
        self.terminalOutput.setMinimumWidth(300)
        contentLayout.addWidget(self.terminalOutput)

        homeLayout.addLayout(contentLayout)

        self.tab_widget.insertTab(0, homeTabContent, "Home")

    def removeSelectedScript(self):
        listItems = self.scriptListWidget.selectedItems()
        if not listItems: return
        for item in listItems:
            self.scriptListWidget.takeItem(self.scriptListWidget.row(item))
            self.removeScript(item.text())

    def tabClicked(self, index):
        if self.tab_widget.tabText(index) == "+":
            filename, _ = QFileDialog.getOpenFileName(self, "Open Script", "", "Python Scripts (*.py)")
            if filename:
                self.addTabFromScript(filename)

    def addTabFromScript(self, filename):
        script_name = os.path.basename(filename)[:-3]
        try:
            if filename not in self.scripts:
                target_script_path = os.path.join(scripts_path, os.path.basename(filename))
                
                if not os.path.exists(target_script_path):
                    shutil.copy(filename, scripts_path)
                    print(f"Copied {filename} to {scripts_path}")
                
                script_code = convert_pyside2_to_pyqt5(filename)
                
                def custom_image_loader(image_path, default_text):
                    if os.path.exists(image_path):
                        return QIcon(image_path)
                    else:
                        print(f"Image not found: {image_path}, using default text.")
                        return default_text
                
                exec_globals = {
                    'custom_image_loader': custom_image_loader,
                }
                exec(script_code, exec_globals)
                
                if 'get_tab_widget' in exec_globals:
                    tab_content = exec_globals['get_tab_widget']()
                else:
                    tab_content = QWidget()

                icon_filename = os.path.join(icon_path, script_name + ".png")
                if os.path.exists(icon_filename):
                    tab_index = self.tab_widget.insertTab(self.tab_widget.count() - 1, tab_content, "")
                    self.tab_widget.setTabIcon(tab_index, QIcon(icon_filename))
                else:
                    tab_index = self.tab_widget.insertTab(self.tab_widget.count() - 1, tab_content, script_name)

                self.tab_widget.setCurrentIndex(tab_index)
                self.scripts.append(filename)
                self.scriptListWidget.addItem(filename)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error loading script {script_name}: {str(e)}")
            print(f"Error loading script {script_name}: {e}")

    def removeScript(self, filename):
        if filename in self.scripts:
            try:
                target_script_path = os.path.join(scripts_path, os.path.basename(filename))
                if os.path.exists(target_script_path):
                    os.remove(target_script_path)
                    print(f"Removed {target_script_path} from the scripts folder.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error removing script file {os.path.basename(filename)}: {str(e)}")
                print(f"Error removing script file {os.path.basename(filename)}: {e}")

            self.scripts.remove(filename)

            for i in range(self.tab_widget.count() - 1, -1, -1):
                if self.tab_widget.tabText(i) == os.path.basename(filename)[:-3]:
                    self.tab_widget.removeTab(i)
                    break

    def write(self, message):
        self.terminalOutput.appendPlainText(message)
        self.terminalOutput.ensureCursorVisible()

if __name__ == "__main__":
    QApplication.setStyle(QStyleFactory.create('Fusion'))
    apply_dark_stylesheet()
    window = MainWindow()    
    sys.stdout = window
    sys.stderr = window
    window.show()
    sys.exit(app.exec_())
