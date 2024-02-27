import sys
from PySide2.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog,
    QProgressBar, QLabel, QMessageBox, QCheckBox, QScrollArea, QGridLayout, QCheckBox
)
from PySide2.QtCore import QThread, Signal, Qt
import os
import shutil
class CopyWorker(QThread):
    update_progress = Signal(int)
    finished = Signal(bool)

    def __init__(self, source_folder, output_folder, file_types, options):
        super().__init__()
        self.source_folder = source_folder
        self.output_folder = output_folder
        self.file_types = file_types
        self.options = options

    def run(self):
        total_files_to_copy, total_dirs_to_copy = self.calculate_total_files_and_dirs()
        total_items_to_copy = total_files_to_copy + (total_dirs_to_copy if not self.options.get('skip_empty_folders', True) else 0)
        copied_items = 0

        for root, dirs, files in os.walk(self.source_folder, topdown=False):
            # Handle directory creation for prefix_and_flatten option or non-empty dirs/files
            dst_dir = os.path.join(self.output_folder, os.path.relpath(root, self.source_folder))
            if self.options.get('prefix_and_flatten', False) or files or not self.options.get('skip_empty_folders', True):
                if not os.path.exists(dst_dir):
                    os.makedirs(dst_dir, exist_ok=True)
                    if not self.options.get('skip_empty_folders', True):
                        copied_items += 1  # Count directory creation towards progress
                        self.update_progress.emit(int((copied_items / total_items_to_copy) * 100))

            for file in files:
                if not self.file_types or any(file.endswith(ext) for ext in self.file_types):
                    if self.options.get('prefix_and_flatten', False):
                        relative_path = os.path.relpath(root, self.source_folder)
                        new_filename = f"{relative_path.replace(os.sep, '_')}_{file}" if relative_path != '.' else file
                        dst_file = os.path.join(self.output_folder, new_filename)
                    else:
                        dst_file = os.path.join(dst_dir, file)
                    shutil.copy2(os.path.join(root, file), dst_file)
                    copied_items += 1
                    self.update_progress.emit(int((copied_items / total_items_to_copy) * 100))

        self.finished.emit(True)

    def calculate_total_files_and_dirs(self):
        total_files = 0
        total_dirs = 0
        for root, dirs, files in os.walk(self.source_folder):
            if not self.options.get('skip_empty_folders', True):
                total_dirs += 1  # Count each directory
            total_files += sum(1 for file in files if not self.file_types or any(file.endswith(ext) for ext in self.file_types))
        return total_files, total_dirs


    def stop(self):
        self.requestInterruption()
        self.wait()


def get_tab_widget():
    widget = QWidget()
    layout = QVBoxLayout(widget)

    source_folder = ''
    output_folder = ''
    worker = None  # Define worker here to make it accessible

    select_source_folder_btn = QPushButton("Select Source Folder")
    select_output_folder_btn = QPushButton("Select Output Folder")
    progressBar = QProgressBar()
    start_btn = QPushButton("Start")
    stop_btn = QPushButton("Stop")
    status_label = QLabel("Status: Idle")
    skip_empty_folders_cb = QCheckBox("Skip Empty Folders")
    prefix_and_flatten_cb = QCheckBox("Prefix and Flatten")

    scrollArea = QScrollArea()
    scrollAreaWidgetContents = QWidget()
    scrollArea.setWidget(scrollAreaWidgetContents)
    scrollArea.setWidgetResizable(True)
    file_types_layout = QGridLayout(scrollAreaWidgetContents)

    def update_file_types():
        nonlocal source_folder
        if os.path.exists(source_folder):
            for i in reversed(range(file_types_layout.count())): 
                widget_to_remove = file_types_layout.itemAt(i).widget()
                if widget_to_remove is not None:  # Ensure the widget is not None before removing
                    widget_to_remove.setParent(None)
                    widget_to_remove.deleteLater()
            file_types = set()
            for root, dirs, files in os.walk(source_folder):
                for file in files:
                    ext = os.path.splitext(file)[1].lower()
                    if ext:
                        file_types.add(ext)
            for ext in sorted(file_types):
                cb = QCheckBox(ext)
                file_types_layout.addWidget(cb)

    def select_source_folder():
        nonlocal source_folder
        temp = QFileDialog.getExistingDirectory(widget, "Select Source Folder")
        if temp:  # Check if the user made a selection
            source_folder = temp
            status_label.setText(f"Source folder selected: {source_folder}")
            update_file_types()

    def select_output_folder():
        nonlocal output_folder
        temp = QFileDialog.getExistingDirectory(widget, "Select Output Folder")
        if temp:  # Check if the user made a selection
            output_folder = temp
            status_label.setText(f"Output folder selected: {output_folder}")

    def start_copying():
        nonlocal worker
        selected_file_types = [cb.text() for cb in scrollAreaWidgetContents.findChildren(QCheckBox) if cb.isChecked()]
        if not source_folder or not output_folder:
            QMessageBox.warning(widget, "Warning", "Please select both source and output folders.")
            return
        options = {
            'skip_empty_folders': skip_empty_folders_cb.isChecked(),
            'prefix_and_flatten': prefix_and_flatten_cb.isChecked(),
        }
        worker = CopyWorker(source_folder, output_folder, selected_file_types, options)
        worker.update_progress.connect(progressBar.setValue)
        worker.finished.connect(lambda: status_label.setText("Copy finished."))
        worker.start()
        start_btn.setEnabled(False)
        stop_btn.setEnabled(True)

    def stop_copying():
        nonlocal worker
        if worker is not None:
            worker.stop()
            start_btn.setEnabled(True)
            stop_btn.setEnabled(False)

    select_source_folder_btn.clicked.connect(select_source_folder)
    select_output_folder_btn.clicked.connect(select_output_folder)
    start_btn.clicked.connect(start_copying)
    stop_btn.clicked.connect(stop_copying)
    stop_btn.setEnabled(False)

    layout.addWidget(select_source_folder_btn)
    layout.addWidget(select_output_folder_btn)
    layout.addWidget(progressBar)
    layout.addWidget(skip_empty_folders_cb)
    layout.addWidget(prefix_and_flatten_cb)
    layout.addWidget(scrollArea)
    layout.addWidget(start_btn)
    layout.addWidget(stop_btn)
    layout.addWidget(status_label)

    return widget

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWidget = get_tab_widget()
    mainWidget.show()
    sys.exit(app.exec_())
