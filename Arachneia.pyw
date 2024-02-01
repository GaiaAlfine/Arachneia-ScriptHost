import sys
import threading
import os
import re
from PySide2.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel, QPushButton, QTabBar, QFileDialog, QTextBrowser, 
    QProgressBar, QHBoxLayout, QLineEdit, QSizePolicy, QTextEdit, QButtonGroup, QScrollArea, QGridLayout
    )
from PySide2.QtGui import QPalette, QColor, QIcon, QDesktopServices
from PySide2.QtCore import Qt, QSize, QThread, Signal, QUrl, QObject, QThread, Signal, Slot
import markdown
import shutil

version = "V0.2.0"

sys.argv += ['-platform', 'windows:darkmode=2']
app = QApplication(sys.argv)

def dark_palette():
    '''Create a dark palette for the application.'''
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    palette.setColor(QPalette.Disabled, QPalette.Text, QColor(127, 127, 127))
    palette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(127, 127, 127))
    palette.setColor(QPalette.Disabled, QPalette.WindowText, QColor(127, 127, 127))
    return palette

class RotatedTabBar(QTabBar):
    def tabSizeHint(self, index):
        # Set a fixed size of 100x100 pixels for each tab
        return QSize(100, 100)

    def __init__(self, parent=None):
        super().__init__(parent)
        # Adjust icon size to fit within the 100x100 pixel tab
        self.setIconSize(QSize(80, 80))  # Adjust the size as needed

import sys

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller."""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabBar(RotatedTabBar())  # Use the custom tab bar
        self.tab_widget.setTabPosition(QTabWidget.West)  # Move tabs to the left

        # Icons for tabs (replace 'icon_path' with the actual path to your icon files)
        # icons = [
        #     QIcon(resource_path('resources/icons/homeIcon.png')),
        #     QIcon(resource_path('resources/icons/UrlExtactor.ico')),
        #     QIcon(resource_path('resources/icons/dateTranslator.ico'))
        # ] #this is for the exe
        icons = [
            QIcon('Arachneia/resources/icons/homeIcon.png'),
            QIcon('Arachneia/resources/icons/UrlExtactor.ico'),
            QIcon('Arachneia/resources/icons/dateTranslator.ico'),
            QIcon('Arachneia/resources/icons/FileCopy.png'),
            QIcon('Arachneia/resources/icons/mdscripticon.png')
        ]

        # Add tabs with icons
        for i in range(5):
            tab = QWidget()
            self.tab_widget.addTab(tab, icons[i], "")  # Empty string for no text

        self.setCentralWidget(self.tab_widget)
        self.setWindowTitle(f"Arachneia {version} - Home")
        self.resize(1000, 600)
        self.setWindowIcon(QIcon(resource_path('resources/icons/Arachneia.ico')))
        self.tab_widget.currentChanged.connect(self.loadTab)
        self.Setup_Home()
        # Connect tab activation to custom title update
        self.tab_widget.currentChanged.connect(self.updateTitle)

    def updateTitle(self, index):
        if index == 0:
            self.setWindowTitle(f"Arachneia {version} - Home")
        elif index == 1:
            self.setWindowTitle(f"Arachneia {version} - URL Extractor")
        elif index == 2:
            self.setWindowTitle(f"Arachneia {version} - Date Translator")
        elif index == 3:
            self.setWindowTitle(f"Arachneia {version} - File Copy")
        elif index == 4:
            self.setWindowTitle(f"Arachneia {version} - Markdown Editor")

    def setCustomText(self, custom_text):
        # Find the currently active tab widget
        current_tab_index = self.tab_widget.currentIndex()
        current_tab_widget = self.tab_widget.widget(current_tab_index)

        # Clear any existing layout in the tab widget
        if current_tab_widget.layout():
            layout = current_tab_widget.layout()
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()

        # Create and add a label with the custom text to the tab
        label = QLabel(custom_text)
        label.setAlignment(Qt.AlignCenter)
        current_tab_widget.layout().addWidget(label)


    def loadTab(self, index):
        """Load the content of the tab when it's selected."""
        print(f"Tab {index + 1} selected!")  
        if index == 0 and not self.tab_widget.widget(index).layout():
            self.Setup_Home()
        elif index == 1 and not self.tab_widget.widget(index).layout():
            self.Setup_URL_Extractor()
        elif index == 2 and not self.tab_widget.widget(index).layout():
            self.Setup_Date_Translator()
        elif index == 3 and not self.tab_widget.widget(index).layout():
            self.Setup_File_Copy()
        elif index == 4 and not self.tab_widget.widget(index).layout():
            self.Setup_Markdown_Editor()

    def Setup_Home(self):
        """Sets up content for Tab One."""
        self.run_Home_Script()

    def Setup_URL_Extractor(self):
        """Sets up content for Tab Two."""
        self.run_URL_Extractor_Script()

    def Setup_Date_Translator(self):
        """Sets up content for Tab Three."""
        self.run_Date_Translator_Script()

    def Setup_File_Copy(self):
        """Sets up content for Tab Three."""
        self.run_File_Copy_Script()

    def Setup_Markdown_Editor(self):
        """Sets up content for Tab Three."""
        self.run_Markdown_Editor_Script()

    def setupTab(self, index, script_function):
        """General method to set up a tab."""
        tab = self.tab_widget.widget(index)
        layout = QVBoxLayout(tab)
        script_function()

    def run_Home_Script(self):
        # Create a QTextBrowser widget to display the readme content
        text_browser = QTextBrowser()
        layout = QVBoxLayout()

        # Try to read the content of the readme.md file with UTF-8 encoding
        try:
            # with open(resource_path('resources/readme.md'), 'r', encoding='utf-8') as file:
            #     readme_content = file.read() #this is for the exe
            with open('Arachneia/resources/readme.md', 'r', encoding='utf-8') as file:
                readme_content = file.read()
            # Convert Markdown content to HTML
            readme_html = markdown.markdown(readme_content)
        except FileNotFoundError:
            readme_html = "<p>Readme.md file not found.</p>"
        except UnicodeDecodeError as e:
            print(f"Error reading file: {e}")
            readme_html = "<p>Error loading content.</p>"
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            readme_html = "<p>Unable to load content.</p>"

        # Set the HTML content to the QTextBrowser
        text_browser.setHtml(readme_html)

        # Add the QTextBrowser to the layout
        layout.addWidget(text_browser)

        # Get the first tab and set the layout
        tab_one = self.tab_widget.widget(0)
        tab_one.setLayout(layout)

    def run_URL_Extractor_Script(self):
        class URLExtractionThread(QThread):
            url_found = Signal(str)
            progress_updated = Signal(int)
            stop_flag = False

            def __init__(self, folder_path):
                super().__init__()
                self.folder_path = folder_path
                self.stop_flag = False

            def run(self):
                self.stop_flag = False
                total_files = sum([len(files) for _, _, files in os.walk(self.folder_path)])
                processed_files = 0

                for root, dirs, files in os.walk(self.folder_path):
                    if self.stop_flag:
                        break
                    for filename in files:
                        if self.stop_flag:
                            break
                        if filename.endswith(".txt"):
                            file_path = os.path.join(root, filename)
                            folder_url = f'file:///{root}'.replace('\\', '/')
                            content = self.read_file_with_fallback_encodings(file_path)
                            if content is not None:
                                urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', content)
                                if urls:
                                    formatted_entry = f'<a href="{folder_url}" style="color: #c77100;">From {filename} in [{root}]</a>:<br>' + '<br>'.join([f'<a href="{url}">{url}</a>' for url in urls]) + '<br><br>'
                                    self.url_found.emit(formatted_entry)
                        processed_files += 1
                        progress = int((processed_files / total_files) * 100)
                        self.progress_updated.emit(progress)


            def read_file_with_fallback_encodings(self, file_path):
                encodings = ['utf-8', 'iso-8859-1', 'windows-1252']
                for encoding in encodings:
                    try:
                        with open(file_path, 'r', encoding=encoding) as file:
                            return file.read()
                    except UnicodeDecodeError:
                        continue
                print(f"Could not read {file_path} due to encoding issue")
                return None
            
            def stop(self):
                self.stop_flag = True

        class URLExtractorApp(QMainWindow):
            def __init__(self):
                super().__init__()
                self.initUI()

            def initUI(self):
                # Create a central widget for the QMainWindow
                centralWidget = QWidget(self)
                layout = QVBoxLayout(centralWidget)

                # Title text at the top, use a QLabel for this
                self.titleLabel = QLabel('URL Extractor')
                self.titleLabel.setAlignment(Qt.AlignCenter)

                # Create buttons
                self.btnSelect = QPushButton('Select')
                self.btnExport = QPushButton('Export')
                self.btnClear = QPushButton('Clear')
                self.btnStop = QPushButton('Stop')

                # Create a progress bar and hide the percentage text
                self.progressBar = QProgressBar()
                self.progressBar.setTextVisible(False)  # Hide the percentage text
                
                self.progressBar.setStyleSheet("""
                    QProgressBar {
                        border: 2px solid grey;
                        border-radius: 5px;
                        text-align: center;
                    }
                    """)

                # Text browser to display URLs
                self.textBrowser = QTextBrowser()
                self.textBrowser.setPlaceholderText("Extracted URLs will be displayed here.")
                self.progressBar.setMaximum(100)

                # Connect the anchorClicked signal to the openUrl method
                self.textBrowser.anchorClicked.connect(self.openUrl)  # Add this line
                self.textBrowser.setOpenLinks(False)

                # Button layout
                buttonLayout = QHBoxLayout()
                buttonLayout.addWidget(self.btnSelect)
                buttonLayout.addWidget(self.btnExport)
                buttonLayout.addWidget(self.btnClear)

                # Add widgets to the main layout
                layout.addWidget(self.titleLabel)
                layout.addLayout(buttonLayout)
                layout.addWidget(self.progressBar)
                layout.addWidget(self.textBrowser)
                layout.addWidget(self.btnStop)

                # Set the central widget for the QMainWindow with the layout
                self.setCentralWidget(centralWidget)

                # Connect buttons to their functions
                self.btnSelect.clicked.connect(self.loadFile)
                self.btnExport.clicked.connect(self.saveFile)
                self.btnClear.clicked.connect(self.clearText)
                self.btnStop.clicked.connect(self.stopOperation)
            def loadFile(self):
                folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
                if folder_path:
                    self.textBrowser.setText("Processing files... Please wait.")
                    self.extractionThread = URLExtractionThread(folder_path)
                    self.extractionThread.url_found.connect(self.updateTextBrowser)
                    self.extractionThread.progress_updated.connect(self.updateProgressBar)
                    self.extractionThread.start()


            def updateProgressBar(self, value):
                self.progressBar.setValue(value)

            def updateTextBrowser(self, formatted_entry):
                self.textBrowser.append(formatted_entry)

            def saveFile(self):
                file_name, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Text Files (*.txt);;All Files (*)")
                if file_name:
                    # Write URLs to the selected file, getting plain text from the QTextBrowser
                    with open(file_name, 'w') as file:
                        file.write(self.textBrowser.toPlainText())

            def openUrl(self, url: QUrl):
                QDesktopServices.openUrl(url)



            def clearText(self):
                self.textBrowser.clear()

            def stopOperation(self):
                if hasattr(self, 'extractionThread') and self.extractionThread.isRunning():
                    self.extractionThread.stop()

        # Use the existing tab for Tab Two
        tab_two = self.tab_widget.widget(1)
        layout = QVBoxLayout(tab_two)

        # Create an instance of URLExtractorApp and set it up
        self.urlExtractorApp = URLExtractorApp()
        layout.addWidget(self.urlExtractorApp)

        # Set the layout for the tab
        tab_two.setLayout(layout)

    def run_Date_Translator_Script(self):
        # Function to translate date to numerical format
        def translate_date(input_date):
            for char in ".,:;/":
                input_date = input_date.replace(char, "")

            month_dict = {
                #eng
                "January": "01", "january": "01", "Jan": "01", "jan": "01", "Jan.": "01", "jan.": "01",
                "February": "02", "february": "02", "Feb": "02", "feb": "02", "Feb.": "02", "feb.": "02", 
                "March": "03", "march": "03", "Mar": "03", "mar": "03", "Mar.": "03", "mar.": "03", 
                "April": "04", "april": "04", "Apr": "04", "apr": "04","Apr.": "04", "apr.": "04",
                "May": "05", "may": "05", "May.": "05", "may.": "05", 
                "Juni": "06", "juni": "06", "Jun": "06", "jun": "06", "Jun.": "06", "jun.": "06", 
                "July": "07", "july": "07", "Jul": "07", "jul": "07", "Jul.": "07", "jul.": "07", 
                "August": "08", "august": "08", "Aug": "08", "aug": "08", "Aug.": "08", "aug.": "08", 
                "September": "09", "september": "09", "Sep": "09", "sep": "09", "Sep.": "09", "sep.": "09", 
                "October": "10", "october": "10", "Oct": "10", "oct": "10", "Oct.": "10", "oct.": "10", 
                "November": "11", "november": "11", "Nov": "11", "nov": "11", "Nov.": "11", "nov.": "11", 
                "Desember": "12", "desember": "12", "Des": "12", "des": "12", "Des.": "12", "des.": "12",
                #nok
                "Januar": "01", "januar": "01", "Jan": "01", "jan": "01", "Jan.": "01", "jan.": "01",
                "Februar": "02", "februar": "02", "Feb": "02", "feb": "02", "Feb.": "02", "feb.": "02", 
                "Mars": "03", "mars": "03", "Mar": "03", "mar": "03", "Mar.": "03", "mar.": "03", 
                "April": "04", "april": "04", "Apr": "04", "apr": "04","Apr.": "04", "apr.": "04",
                "Mai": "05", "mai": "05", "Mai.": "05", "mai.": "05", 
                "Juni": "06", "juni": "06", "Jun": "06", "jun": "06", "Jun.": "06", "jun.": "06", 
                "Juli": "07", "juli": "07", "Jul": "07", "jul": "07", "Jul.": "07", "jul.": "07", 
                "August": "08", "august": "08", "Aug": "08", "aug": "08", "Aug.": "08", "aug.": "08", 
                "September": "09", "september": "09", "Sep": "09", "sep": "09", "Sep.": "09", "sep.": "09", 
                "Oktober": "10", "oktober": "10", "Okt": "10", "okt": "10", "Okt.": "10", "okt.": "10", 
                "November": "11", "november": "11", "Nov": "11", "nov": "11", "Nov.": "11", "nov.": "11", 
                "Desember": "12", "desember": "12", "Des": "12", "des": "12", "Des.": "12", "des.": "12",
                # Japanese
                "一月": "01", "二月": "02", "三月": "03", "四月": "04", "五月": "05",
                "六月": "06", "七月": "07", "八月": "08", "九月": "09", "十月": "10",
                "十一月": "11", "十二月": "12"
            }

            parts = input_date.split()
            
            day, month, year = "", "", ""
            for part in parts:
                if part in month_dict.keys():
                    month = month_dict[part]
                elif len(part) == 4 and part.isdigit():
                    year = part
                elif part.isdigit():
                    day = part

            if day and month and year:
                numerical_date = f"{month}.{day}.{year}"
                return numerical_date
            else:
                return "Invalid date format"
            
        def revert_date_format(numerical_date):
            month_dict = {
                "01": "January", "02": "February", "03": "March", "04": "April", "05": "May", "06": "Juni",
                "07": "July", "08": "August", "09": "September", "10": "October", "11": "November", "12": "Desember"
            }
            parts = numerical_date.split(".")
            if len(parts) == 3:
                month, day, year = parts
                month = month_dict.get(month, "")
                return f"{month} {day.strip('.')} {year}"
            return "Invalid date format"

        class DateTranslatorApp(QMainWindow):
            def __init__(self):
                super().__init__()
                self.setWindowTitle("Date Translator")

                self.central_widget = QWidget(self)
                self.setCentralWidget(self.central_widget)

                self.layout = QVBoxLayout(self.central_widget)

                self.program_label = QLabel("Date Translator")
                self.program_label.setAlignment(Qt.AlignCenter)  # Align the label text to center
                self.layout.addWidget(self.program_label)

                self.date_label = QLabel("Enter a date:")
                self.layout.addWidget(self.date_label)

                self.date_input = QLineEdit()
                self.date_input.setFixedHeight(30)  # Set the fixed height for the input area
                self.layout.addWidget(self.date_input)

                self.translate_button = QPushButton("Translate")

                self.switch_button = QPushButton("↑↓")
                self.switch_button.setFixedSize(25, 25)  # Makes the button square
                self.switch_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
                self.switch_button.clicked.connect(self.switch_mode)

                # Add both translate and switch button to a horizontal layout
                self.buttons_layout = QHBoxLayout()
                self.buttons_layout.addWidget(self.translate_button)
                self.buttons_layout.addWidget(self.switch_button)
                self.layout.addLayout(self.buttons_layout)


                self.switch_button.toggled.connect(self.switch_mode)
                self.layout.addWidget(self.translate_button)
                self.layout.addWidget(self.switch_button)

                self.buttons_layout = QHBoxLayout()
                self.buttons_layout.addWidget(self.translate_button)
                self.buttons_layout.addWidget(self.switch_button)
                self.layout.addLayout(self.buttons_layout)

                self.result_area = QTextEdit()
                self.result_area.setFixedHeight(30)  # Ensure output area is the same size as input
                self.layout.addWidget(self.result_area)


                self.date_renamer_label = QLabel("Date Renamer")
                self.date_renamer_label.setAlignment(Qt.AlignCenter)  # Align the label text to center
                self.layout.addWidget(self.date_renamer_label)


                self.progress_bar = QProgressBar()
                self.progress_bar.setTextVisible(False)  # Hide the percentage text
                self.layout.addWidget(self.progress_bar)

                self.select_button = QPushButton("Select Folder")
                self.layout.addWidget(self.select_button)

                self.log_area = QTextEdit()
                self.layout.addWidget(self.log_area)

                self.start_button = QPushButton("Start")
                self.layout.addWidget(self.start_button)

                self.translate_button.clicked.connect(self.translate_button_click)

            def translate_button_click(self):
                input_date = self.date_input.text()
                if self.switch_button.text() == "↓↑":  # If the button indicates switching back to date
                    self.result_area.setText(revert_date_format(input_date))
                else:
                    numerical_date = translate_date(input_date)
                    self.result_area.setText(f"{numerical_date}")

            def switch_mode(self):
                if self.switch_button.text() == "↑↓":
                    self.switch_button.setText("↓↑")
                    self.date_label.setText("Enter a numerical date (mm. dd. yyyy):")
                else:
                    self.switch_button.setText("↑↓")
                    self.date_label.setText("Enter a date:")
        # Use the existing tab for Tab Two
        tab_three = self.tab_widget.widget(2)
        layout = QVBoxLayout(tab_three)

        # Create an instance of URLExtractorApp and set it up
        self.DateTranslatorApp = DateTranslatorApp()
        layout.addWidget(self.DateTranslatorApp)

        # Set the layout for the tab
        tab_three.setLayout(layout)

    def run_File_Copy_Script(self):
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
                    dst_dir = root.replace(self.source_folder, self.output_folder, 1)

                    if self.options['prefix_and_flatten']:
                        for file in files_to_copy:
                            subfolder_name = '' if root == self.source_folder else os.path.basename(root)
                            new_filename = f"{subfolder_name}_{file}" if subfolder_name else file
                            dst_file = os.path.join(self.output_folder, new_filename)
                            src_file = os.path.join(root, file)
                            os.makedirs(os.path.dirname(dst_file), exist_ok=True)
                            shutil.copy2(src_file, dst_file)
                            copied_files += 1
                            self.update_progress.emit(int((copied_files / total_files_to_copy) * 100))

                    elif files_to_copy or not self.options['skip_empty_folders']:
                        os.makedirs(dst_dir, exist_ok=True)
                    for file in files_to_copy:
                        dst_file = os.path.join(dst_dir, file)
                        src_file = os.path.join(root, file)
                        shutil.copy2(src_file, dst_file)
                        copied_files += 1
                        self.update_progress.emit(int((copied_files / total_files_to_copy) * 100))
                    else:
                        pass

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
                # Clear existing buttons
                for i in reversed(range(self.checkbox_container_layout.count())): 
                    widget = self.checkbox_container_layout.itemAt(i).widget()
                    if widget is not None:
                        widget.deleteLater()
                self.file_type_buttons.clear()

                # Scan for file types and update buttons
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

        # Use the existing tab for Tab Two
        tab_three = self.tab_widget.widget(3)
        layout = QVBoxLayout(tab_three)

        # Create an instance of FileCopyProgram and set it up
        self.FileCopyProgram = FileCopyProgram()
        layout.addWidget(self.FileCopyProgram)

        # Set the layout for the tab
        tab_three.setLayout(layout)

    def run_Markdown_Editor_Script(self):
        class MarkdownEditor(QMainWindow):
            def __init__(self):
                super().__init__()
                self.setWindowTitle("Markdown Editor with Preview")
                self.setGeometry(100, 100, 1200, 600)  # Adjusted for better side-by-side layout
                
                # Main layout
                mainLayout = QVBoxLayout()
                self.titleLabel = QLabel("Markdown Editor")
                self.titleLabel.setAlignment(Qt.AlignCenter)  # Center the title
                mainLayout.addWidget(self.titleLabel)
                # Buttons layout
                buttonsLayout = QHBoxLayout()
                self.openButton = QPushButton("Open")
                self.openButton.clicked.connect(self.openFile)
                self.saveButton = QPushButton("Save")
                self.saveButton.clicked.connect(self.saveFile)
                self.newButton = QPushButton("New")
                self.newButton.clicked.connect(self.newFile)
                
                # Add buttons to the buttons layout
                buttonsLayout.addWidget(self.openButton)
                buttonsLayout.addWidget(self.saveButton)
                buttonsLayout.addWidget(self.newButton)
                
                # Add buttons layout to the main layout
                mainLayout.addLayout(buttonsLayout)
                
                # Editor and Preview layout
                editorPreviewLayout = QHBoxLayout()  # This layout arranges editor and preview side by side
                
                # Create the Markdown editor area
                self.editor = QTextEdit()
                self.editor.textChanged.connect(self.updatePreview)
                
                # Create the HTML preview area
                self.preview = QTextEdit()
                self.preview.setReadOnly(True)
                
                # Add editor and preview to the editorPreviewLayout
                editorPreviewLayout.addWidget(self.editor)
                editorPreviewLayout.addWidget(self.preview)
                
                # Add editorPreviewLayout to the main layout
                mainLayout.addLayout(editorPreviewLayout)
                
                # Set the layout on a central widget
                centralWidget = QWidget()
                centralWidget.setLayout(mainLayout)
                self.setCentralWidget(centralWidget)
            
            @Slot()
            def updatePreview(self):
                md_text = self.editor.toPlainText()
                html_content = markdown.markdown(md_text)
                self.preview.setHtml(html_content)
            
            def openFile(self):
                filename, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Markdown files (*.md)")
                if filename:
                    with open(filename, 'r', encoding='utf-8') as file:
                        self.editor.setPlainText(file.read())
            
            def saveFile(self):
                filename, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Markdown files (*.md)")
                if filename:
                    with open(filename, 'w', encoding='utf-8') as file:
                        file.write(self.editor.toPlainText())
            
            def newFile(self):
                self.editor.clear()
                self.preview.clear()


        # Use the existing tab for Tab Two
        Five_three = self.tab_widget.widget(4)
        layout = QVBoxLayout(Five_three)

        # Create an instance of MarkdownEditor and set it up
        self.MarkdownEditor = MarkdownEditor()
        layout.addWidget(self.MarkdownEditor)

        # Set the layout for the tab
        Five_three.setLayout(layout)

    def runScriptWithTimeout(self, script, timeout):

        """Run a script with a timeout to avoid freezing."""
        def target():
            # Here you can call your script
            pass

        thread = threading.Thread(target=target)
        thread.start()
        thread.join(timeout)
        if thread.is_alive():
            print("Script took too long to run and was terminated.")
            thread.terminate()

if __name__ == "__main__":
    app.setPalette(dark_palette())  # This line applies the dark palette to the application.
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
