import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel, QTextEdit, QHBoxLayout, QPushButton
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
        self.setStyleSheet("QMainWindow { background-color: #2B2B2B; }"
                           "QTabWidget::pane { border: 0; }"
                           "QLabel { color: white; font-size: 24px; }"
                           "QTabBar::tab { background: #3C3F41; color: white; margin: 0; padding: 15px; }"
                           "QTabBar::tab:selected { background: #313335; }"
                           "QTextEdit { background: #2B2B2B; color: white; }")
        
        # Main layout for central widget
        self.central_layout = QVBoxLayout()  # Use QVBoxLayout as the central layout
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.central_layout)
        self.setCentralWidget(self.central_widget)

        # Add the placeholder label at the top of the central layout with customizable font size
        file_copy_font_size = 100  # Easily editable font size
        self.placeholder_label = QLabel("Settigns")
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
        self.console.setStyleSheet("font-family: 'Consolas'; font-size: 12px;")

        # Adjust the size and layout of the tabs and console
        self.tab_widget.setStyleSheet("QTabWidget { font-size: 14px; }")
        self.tab_widget.setTabPosition(QTabWidget.North)
        self.tab_widget.setTabShape(QTabWidget.Rounded)
        # self.console.setFixedHeight(1000)  # Adjust height as needed

        # Redirect sys.stdout to the console widget
        self.redirect_output_to_console()
            
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
        self.gui_tab_label = QLabel("GUI Settings")
        self.gui_tab_layout.addWidget(self.gui_tab_label)
        self.gui_tab.setLayout(self.gui_tab_layout)
        self.tab_widget.addTab(self.gui_tab, "Gui")

        # More tab
        self.more_tab = QWidget()
        self.more_tab_layout = QVBoxLayout()
        self.more_tab_label = QLabel("More Settings")
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
