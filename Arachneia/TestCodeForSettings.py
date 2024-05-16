import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel, QTextEdit, QHBoxLayout, QPushButton, QListWidget, QLineEdit, QInputDialog
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, Qt
from PyQt5.QtGui import QTextCursor

class EmittingStream(QObject):
    textWritten = pyqtSignal(str)

    def write(self, text):
        self.textWritten.emit(str(text))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Setting")
        
        # Styling
        self.setStyleSheet(
            """
            QMainWindow {
                background-color: #2B2B2B; 
                }
            QTabWidget::pane { 
                border: 1px solid gray ; 
                top: -1px;
                width: 1142px;
                }
            QLabel { 
                color: white; font-size: 24px; 
                }
            QTabBar::tab:first{
                border-top-left-radius: 20px;
                border: 1px solid gray ; 
                border-right: transparent;
                }
            QTabBar::tab:last{
                border-top-right-radius: 20px;
                border-left: transparent;
        }
            QTabBar::tab {
                width: 350px;
                background: #2B2B2B; 
                color: white; 
                margin: 0; 
                padding: 15px;
                border: transparent;
                border-top: 1px solid gray;
                border-left: 1px solid gray;
                border-right: 1px solid gray;
                border-bottom: 1px solid gray;
                }
            QTabBar::tab:selected {
                border-bottom: 1px solid #2B2B2B;
                background: #2B2B2B;
                }
            QTextEdit {
                background: #2B2B2B; 
                color: white; 
                font-family: 'Consolas'; 
                font-size: 12px; 
                min-width: 100px;
                }
            """
            )
        
        # Main layout for central widget
        self.central_layout = QVBoxLayout()  # Use QVBoxLayout as the central layout
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.central_layout)
        self.setCentralWidget(self.central_widget)

        # Add the placeholder label at the top of the central layout with customizable font size
        file_copy_font_size = 100  # Easily editable font size
        self.placeholder_label = QLabel("Settings")
        self.placeholder_label.setAlignment(Qt.AlignCenter)
        self.placeholder_label.setStyleSheet(f"font-size: {file_copy_font_size}px; text-decoration:")
        self.central_layout.addWidget(self.placeholder_label)
        
        # Create a container widget for the tab widget and console, using QHBoxLayout
        self.container_widget = QWidget()
        self.container_layout = QHBoxLayout()
        self.container_widget.setLayout(self.container_layout)

        # Add the tab widget to the container layout
        self.tab_widget = QTabWidget()
        self.container_layout.addWidget(self.tab_widget)

        # Create the tabs
        self.create_tabs()

        # Create the console
        self.console = QTextEdit()
        self.console.setReadOnly(True)  # Making the console read-only
        self.console.setPlaceholderText("Console Output")
        self.console.setFixedWidth(700)  # Set the fixed width of the console
        self.container_layout.addWidget(self.console)

        # Add the container widget to the central layout, below the placeholder label
        self.central_layout.addWidget(self.container_widget)
        self.placeholder_label.setText("Settings")
        self.placeholder_label.setStyleSheet("font-size: 48px; color: white;")

        # Adjust tab labels to match the image
        self.scripts_tab_label.setText("Scripts Settings")
        self.gui_tab_label.setText("GUI Settings")
        self.more_tab_label.setText("More Settings")

        # Adjust the console to match the image
        self.console.setStyleSheet(
            """
            QTextEdit {
                background: #2B2B2B; 
                color: white; 
                font-family: 'Consolas'; 
                font-size: 12px;
                border: 1px solid gray; 
                max-width: 700px;  /* Set the maximum width here */
                }
            """
        )

        # Adjust the size and layout of the tabs and console
        self.tab_widget.setStyleSheet("QTabWidget { font-size: 14px; }")
        self.tab_widget.setTabPosition(QTabWidget.North)
        self.tab_widget.setTabShape(QTabWidget.Rounded)

        # Redirect sys.stdout to the console widget
        self.redirect_output_to_console()

        # Create and add a button to send a test message to the terminal
        self.test_button = QPushButton("Send Test Message")
        self.test_button.clicked.connect(self.send_test_message)
        self.central_layout.addWidget(self.test_button)

        # Scripts list to pass to SettingsWindow
        self.scripts = ["Script1", "Script2", "Script3"]
        self.populate_scripts_tab()

    def create_tabs(self):
        # Scripts tab
        self.scripts_tab = QWidget()
        self.scripts_tab_layout = QVBoxLayout()
        self.scripts_tab_label = QLabel("Scripts Settings")
        self.scripts_tab_layout.addWidget(self.scripts_tab_label)
        self.scripts_tab.setLayout(self.scripts_tab_layout)
        self.tab_widget.addTab(self.scripts_tab, "Scripts")

        # GUI tab
        self.gui_tab = QWidget()
        self.gui_tab_layout = QVBoxLayout()
        self.gui_tab_label = QLabel("No GUI Settings Yet")
        self.gui_tab_layout.addWidget(self.gui_tab_label)
        self.gui_tab.setLayout(self.gui_tab_layout)
        self.tab_widget.addTab(self.gui_tab, "Gui")

        # More tab
        self.more_tab = QWidget()
        self.more_tab_layout = QVBoxLayout()
        self.more_tab_label = QLabel("No More Settings Yet")
        self.more_tab_layout.addWidget(self.more_tab_label)
        self.more_tab.setLayout(self.more_tab_layout)
        self.tab_widget.addTab(self.more_tab, "More")

    def redirect_output_to_console(self):
        # Create an instance of the EmittingStream and connect its signal to the append_text method
        sys.stdout = EmittingStream(textWritten=self.append_text_to_console)

    @pyqtSlot(str)
    def append_text_to_console(self, text):
        # Append text to the QTextEdit console
        self.console.moveCursor(QTextCursor.End)
        self.console.insertPlainText(text)

    def send_test_message(self):
        # Method to send a test message to the terminal
        print("Test message sent to the terminal")

    def populate_scripts_tab(self):
        self.scriptListWidget = QListWidget()
        self.scripts_tab_layout.addWidget(self.scriptListWidget)

        for script in self.scripts:
            self.scriptListWidget.addItem(script)

        # Buttons for adding and removing scripts
        buttonsLayout = QHBoxLayout()
        self.addButton = QPushButton('Add')
        self.removeButton = QPushButton('Remove')
        buttonsLayout.addWidget(self.addButton)
        buttonsLayout.addWidget(self.removeButton)
        self.scripts_tab_layout.addLayout(buttonsLayout)

        self.addButton.clicked.connect(self.addScript)
        self.removeButton.clicked.connect(self.removeSelectedScript)

    def addScript(self):
        text, ok = QInputDialog.getText(self, 'Add Script', 'Enter script name:')
        if ok and text:
            self.scriptListWidget.addItem(text)
            self.scripts.append(text)
            print(f"Script added: {text}")

    def removeSelectedScript(self):
        listItems = self.scriptListWidget.selectedItems()
        if not listItems: return
        for item in listItems:
            self.scriptListWidget.takeItem(self.scriptListWidget.row(item))
            self.scripts.remove(item.text())
            print(f"Script removed: {item.text()}")

if __name__ == "__main__":
    app = QApplication([])

    # Backup the original stdout and stderr
    original_stdout = sys.stdout
    original_stderr = sys.stderr

    window = MainWindow()
    window.show()

    app.exec_()

    # Restore the original stdout and stderr after the app closes
    sys.stdout = original_stdout
    sys.stderr = original_stderr
    