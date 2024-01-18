import os
import re
from PySide2 import QtWidgets, QtGui, QtCore
from datetime import datetime

class DateConverterApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Date Converter and Folder Renamer")
        self.setGeometry(100, 100, 400, 200)

        # Folder selection button
        self.folder_button = QtWidgets.QPushButton("Select Folder")
        self.folder_button.clicked.connect(self.select_folder)

        # Start button
        self.start_button = QtWidgets.QPushButton("Start Conversion")
        self.start_button.clicked.connect(self.convert_and_rename)

        # Status label
        self.status_label = QtWidgets.QLabel()

        # Layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.folder_button)
        layout.addWidget(self.start_button)
        layout.addWidget(self.status_label)
        self.setLayout(layout)

        self.selected_folder = ""

    def select_folder(self):
        folder_dialog = QtWidgets.QFileDialog()
        folder_dialog.setFileMode(QtWidgets.QFileDialog.Directory)
        if folder_dialog.exec_():
            self.selected_folder = folder_dialog.selectedFiles()[0]
            self.status_label.setText(f"Selected Folder: {self.selected_folder}")

    def convert_and_rename(self):
        if not self.selected_folder:
            self.status_label.setText("Please select a folder first.")
            return

        for root, dirs, files in os.walk(self.selected_folder):
            for dir_name in dirs:
                dir_path = os.path.join(root, dir_name)
                txt_files = [f for f in os.listdir(dir_path) if f.endswith(".txt")]
                if txt_files:
                    date_match = re.search(r'(\w{3} \d{1,2} \d{4})', dir_name)
                    if date_match:
                        date_str = date_match.group(1)
                        try:
                            date_obj = datetime.strptime(date_str, '%b %d %Y')
                            new_date = date_obj.strftime('%m_%d_%Y')
                            new_folder_name = os.path.join(root, new_date)
                            os.rename(dir_path, new_folder_name)
                            self.status_label.setText(f"Renamed folder to: {new_folder_name}")
                        except ValueError:
                            self.status_label.setText(f"Invalid date format: {date_str}")

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = DateConverterApp()
    window.show()
    app.exec_()
