import os
import re
from PySide2 import QtWidgets

class FolderRenamerApp(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle('Folder Renamer')
        self.setGeometry(100, 100, 400, 200)

        self.select_folder_button = QtWidgets.QPushButton('Select Folder', self)
        self.select_folder_button.setGeometry(50, 50, 150, 30)
        self.select_folder_button.clicked.connect(self.select_folder)

        self.rename_button = QtWidgets.QPushButton('Rename Folders', self)
        self.rename_button.setGeometry(220, 50, 150, 30)
        self.rename_button.clicked.connect(self.rename_folders)
        self.rename_button.setEnabled(False)

        self.selected_folder = None

    def select_folder(self):
        self.selected_folder = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Root Folder')
        if self.selected_folder:
            self.rename_button.setEnabled(True)
            QtWidgets.QMessageBox.information(self, 'Selected', 'Folder selected successfully.')

    def rename_folders(self):
        if not self.selected_folder:
            QtWidgets.QMessageBox.warning(self, 'Error', 'No folder selected.')
            return

        for root, dirs, files in os.walk(self.selected_folder, topdown=False):
            date_found = False
            for file_name in sorted(files):
                if file_name.endswith('.txt'):
                    file_path = os.path.join(root, file_name)
                    with open(file_path, 'r') as file:
                        text = file.read()
                        date_match = re.search(r'\d+\.\s\w+\.\s\d{4}', text)
                        if date_match:
                            old_date = date_match.group(0)
                            day, month, year = old_date.split('.')
                            new_date = f"{month.strip()[:3]}_{day.strip()}_{year.strip()}_"
                            new_folder_name = os.path.join(os.path.dirname(root), new_date)
                            if not os.path.exists(new_folder_name):
                                os.rename(root, new_folder_name)
                            date_found = True
                            break  # Stop checking more files if date is found
                try:
                    os.rename(root, new_folder_name)
                except PermissionError as e:
                    QtWidgets.QMessageBox.warning(self, 'Permission Error', f'Access denied for {root}: {e}')
                except OSError as e:
                    QtWidgets.QMessageBox.warning(self, 'OS Error', f'Error for {root}: {e}')


            if date_found:
                continue  # Move to the next folder since this one is renamed

        QtWidgets.QMessageBox.information(self, 'Done', 'Folder structure renamed successfully.')


def main():
    app = QtWidgets.QApplication([])
    renamer_app = FolderRenamerApp()
    renamer_app.show()
    app.exec_()

if __name__ == '__main__':
    main()
