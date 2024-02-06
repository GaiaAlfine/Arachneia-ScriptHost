import sys
from PySide2.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QTextEdit, QProgressBar, QHBoxLayout, QHBoxLayout, QSizePolicy
from PySide2.QtCore import Qt

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
        "01": "Jan", "02": "Feb", "03": "Mar", "04": "Apr", "05": "May", "06": "Jun",
        "07": "Jul", "08": "Aug", "09": "Sep", "10": "Oct", "11": "Nov", "12": "Dec"
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

        self.program_label = QLabel("URL Extractor")
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




def main():
    app = QApplication(sys.argv)
    window = DateTranslatorApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
