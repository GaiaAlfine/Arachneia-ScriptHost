# Import the required modules from PySide2
from PySide2.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget

# Define the main window class
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySide2 GUI Example")

        # Create a central widget and set it to the main window
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        # Create a vertical layout
        self.layout = QVBoxLayout()

        # Create a button and add it to the layout
        self.button = QPushButton("Click Me")
        self.button.clicked.connect(self.on_button_clicked)
        self.layout.addWidget(self.button)

        # Set the layout to the central widget
        self.centralWidget.setLayout(self.layout)

    # Slot for button click event
    def on_button_clicked(self):
        print("Button clicked!")

# Entry point of the application
def get_tab_widget():
    widget = MainWindow()
    return widget