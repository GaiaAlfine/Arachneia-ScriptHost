from PySide2.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, QProgressBar,
                               QHBoxLayout, QFileDialog, QScrollArea, QWidget, QGridLayout,
                               QButtonGroup, QCheckBox)
from PySide2.QtCore import QObject, Signal, Qt, QThread
import os, sys
import shutil

class CopyWorker(QObject):
    update_progress = Signal(int)
    finished = Signal(bool)  # True if completed, False if stopped

    def __init__(self, source_folder, output_folder, file_type_buttons, options):
        super().__init__()
        self.source_folder = source_folder
        self.output_folder = output_folder
        self.file_type_buttons = file_type_buttons
        self.options = options
        self.keep_copying = True

    def stop(self):
        self.keep_copying = False

    def copy_files(self):
        total_files_to_copy = self.calculate_total_files()
        copied_files = 0
        self.update_progress.emit(0)

        for root, dirs, files in os.walk(self.source_folder, topdown=False):
            if not self.keep_copying:
                self.finished.emit(False)  # Stopped
                return

            files_to_copy = [f for f in files if any(f.endswith(ext) for ext, btn in self.file_type_buttons.items() if btn.isChecked())]

            # Handle prefix_and_flatten option
            if self.options['prefix_and_flatten']:
                for file in files_to_copy:
                    subfolder_name = '' if root == self.source_folder else os.path.basename(root)
                    new_filename = f"{subfolder_name}_{file}" if subfolder_name else file
                    dst_file = os.path.join(self.output_folder, new_filename)
                    src_file = os.path.join(root, file)
                    shutil.copy2(src_file, dst_file)
                    copied_files += 1
                    self.update_progress.emit(int((copied_files / total_files_to_copy) * 100))
                continue  # Skip the regular copying process for this iteration

            # Regular copying process for non-prefix_and_flatten option
            if not self.options['skip_empty_folders'] or files_to_copy:
                dst_dir = root.replace(self.source_folder, self.output_folder, 1)
                os.makedirs(dst_dir, exist_ok=True)
                for file in files_to_copy:
                    dst_file = os.path.join(dst_dir, file)
                    src_file = os.path.join(root, file)
                    shutil.copy2(src_file, dst_file)
                    copied_files += 1
                    self.update_progress.emit(int((copied_files / total_files_to_copy) * 100))

        self.finished.emit(True)  # Completed


    def calculate_total_files(self):
        total = 0
        for root, _, files in os.walk(self.source_folder):
            for file in files:
                if any(file.endswith(ext) for ext, btn in self.file_type_buttons.items() if btn.isChecked()):
                    total += 1
        return total

class FileCopyProgram(QWidget):
    def __init__(self):
        super().__init__()
        self.file_type_buttons = {}
        self.setWindowTitle("File Copy Program")
        
        # Main layout
        self.layout = QVBoxLayout(self)
        
        # Setup UI
        self.setup_ui()

        self.source_folder = None
        self.output_folder = None

    def setup_ui(self):
        self.placeholder_label = QLabel("File Copy")
        self.placeholder_label.setAlignment(Qt.AlignCenter)
        self.placeholder_label.setStyleSheet("text-decoration: underline;")
        self.layout.addWidget(self.placeholder_label)

        # Input and Output buttons with Progress Bar
        self.io_layout = QHBoxLayout()
        self.select_source_folder_btn = QPushButton("Select Source Folder")
        self.select_source_folder_btn.clicked.connect(self.select_source_folder)
        self.io_layout.addWidget(self.select_source_folder_btn)
        
        self.progressBar = QProgressBar()
        self.progressBar.setTextVisible(False)
        self.io_layout.addWidget(self.progressBar)
        
        self.select_output_folder_btn = QPushButton("Select Output Folder")
        self.select_output_folder_btn.clicked.connect(self.select_output_folder)
        self.io_layout.addWidget(self.select_output_folder_btn)
        self.layout.addLayout(self.io_layout)

        # Toggle buttons
        self.settings_layout = QHBoxLayout()

        self.option_group = QButtonGroup(self)
        self.option_group.setExclusive(True)

        self.add_option_button("None", -1)
        self.add_option_button("Skip Empty Folders", 0)
        self.add_option_button("Prefix and Flatten", 1)
        self.layout.addLayout(self.settings_layout)

        # Status label
        self.status_label = QLabel("")
        self.layout.addWidget(self.status_label)

        # Scroll Area for file type buttons
        self.scrollArea = QScrollArea()
        self.scrollAreaWidgetContents = QWidget()
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.scrollArea.setWidgetResizable(True)
        self.checkbox_container_layout = QGridLayout(self.scrollAreaWidgetContents)
        self.layout.addWidget(self.scrollArea)

        # Start and Stop buttons
        self.button_layout = QHBoxLayout()
        self.start_btn = QPushButton("Start")
        self.start_btn.clicked.connect(self.start_copying)
        self.button_layout.addWidget(self.start_btn)

        self.stop_btn = QPushButton("Stop")
        self.stop_btn.clicked.connect(self.stop_copying)
        self.stop_btn.setEnabled(False)
        self.button_layout.addWidget(self.stop_btn)

        self.layout.addLayout(self.button_layout)

    def add_option_button(self, name, id):
        toggle_button = QPushButton(name)
        toggle_button.setCheckable(True)
        self.settings_layout.addWidget(toggle_button)
        self.option_group.addButton(toggle_button, id)

    def select_source_folder(self):
        self.source_folder = QFileDialog.getExistingDirectory(self, "Select Source Folder")
        if self.source_folder:
            self.update_file_type_toggle_buttons()

    def select_output_folder(self):
        self.output_folder = QFileDialog.getExistingDirectory(self, "Select Output Folder")

    def update_file_type_toggle_buttons(self):
        for i in reversed(range(self.checkbox_container_layout.count())): 
            widget = self.checkbox_container_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
        self.file_type_buttons.clear()

        file_types = set()
        for root, dirs, files in os.walk(self.source_folder):
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if ext:
                    file_types.add(ext)

        row, col = 0, 0
        for file_type in sorted(file_types):
            toggle_button = QPushButton(file_type)
            toggle_button.setCheckable(True)
            self.checkbox_container_layout.addWidget(toggle_button, row, col)
            self.file_type_buttons[file_type] = toggle_button
            col += 1
            if col >= 4:
                row += 1
                col = 0

    def start_copying(self):
        self.thread = QThread()
        options = {
            "skip_empty_folders": self.option_group.button(0).isChecked(),
            "prefix_and_flatten": self.option_group.button(1).isChecked()
        }
        self.worker = CopyWorker(self.source_folder, self.output_folder, self.file_type_buttons, options)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.copy_files)
        self.worker.update_progress.connect(self.progressBar.setValue)
        self.worker.finished.connect(self.on_copy_finished)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.stop_btn.clicked.connect(self.worker.stop)
        self.stop_btn.setEnabled(True)
        self.start_btn.setEnabled(False)

        self.thread.start()

    def stop_copying(self):
        if self.worker:
            self.worker.stop()
            self.stop_btn.setEnabled(False)

    def on_copy_finished(self, completed):
        self.status_label.setText("Copying Completed" if completed else "Copying Stopped")
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
def get_tab_widget():
    widget = FileCopyProgram()
    return widget