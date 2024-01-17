import sys
import threading
import os
from PySide2.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PySide2.QtGui import QPalette, QColor, QIcon
from PySide2.QtCore import Qt


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

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tab_widget = QTabWidget()
        # Add tabs
        self.tab_widget.addTab(QWidget(), "Date Converter")
        self.tab_widget.addTab(QWidget(), "Tab Two")
        self.tab_widget.addTab(QWidget(), "Tab Three")
        self.tab_widget.addTab(QWidget(), "Tab Four")
        self.setCentralWidget(self.tab_widget)
        self.setWindowTitle("Arachneia V0.03")
        self.resize(400, 600)

        # Set the window icon
        self.setWindowIcon(QIcon('Arachneia/Arachneia.ico'))  # Replace 'path_to_your_icon_file' with the actual path to your icon file.

        self.tab_widget.currentChanged.connect(self.loadTab)

        self.setupTabOne()

    def loadTab(self, index):
        """Load the content of the tab when it's selected."""
        if index == 0 and not self.tab_widget.widget(index).layout():
            self.setupTabOne()
        elif index == 1 and not self.tab_widget.widget(index).layout():
            self.setupTabTwo()
        elif index == 2 and not self.tab_widget.widget(index).layout():
            self.setupTabThree()
        elif index == 3 and not self.tab_widget.widget(index).layout():
            self.setupTabFour()

    def setupTabOne(self):
        """Sets up content for Tab One."""
        self.setupTab(0, self.runTabOneScript)

    def setupTabTwo(self):
        """Sets up content for Tab Two."""
        self.setupTab(1, "Tab Two", self.runTabTwoScript)

    def setupTabThree(self):
        """Sets up content for Tab Three."""
        self.setupTab(2, "Tab Three", self.runTabThreeScript)

    def setupTabFour(self):
        """Sets up content for Tab Four."""
        self.setupTab(3, "Tab Four", self.runTabFourScript)

    def setupTab(self, index, script_function):
        """General method to set up a tab."""
        tab = self.tab_widget.widget(index)
        layout = QVBoxLayout(tab)
        script_function()

    def runTabOneScript(self):
        layout = self.tab_widget.widget(0).layout()

        # Input label and text box
        input_textbox = QLineEdit()
        input_textbox.setContentsMargins(0, 0, 0, 0)  # Set margins to zero
        layout.addWidget(input_textbox, alignment=Qt.AlignTop)  # Add alignment to place widgets at the top

        # Convert button
        convert_button = QPushButton("Convert")
        convert_button.setContentsMargins(0, 0, 0, 0)  # Set margins to zero
        layout.addWidget(convert_button, alignment=Qt.AlignTop)  # Align the button to the top

        # Output label (same as input textbox)
        output_textbox = QLineEdit()
        output_textbox.setContentsMargins(0, 0, 0, 0)  # Set margins to zero
        layout.addWidget(output_textbox, alignment=Qt.AlignTop)  # Align the output textbox to the top

        # Set spacing and layout margins to zero
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)



        def convert_date():
            input_date = input_textbox.text()
            input_date = input_date.replace('.', ' ').strip()
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
            if len(parts) == 3 and parts[0].lower() in month_dict:
                converted_date = f"{month_dict[parts[0].lower()]} {parts[1]} {parts[2]}"
                output_textbox.setText(converted_date)
            else:
                output_textbox.setText("Invalid date format")

        convert_button.clicked.connect(convert_date)
        


    def runTabTwoScript(self):
        # Your code for Tab Two script here
        pass

    def runTabThreeScript(self):
        # Your code for Tab Three script here
        pass

    def runTabFourScript(self):
        # Your code for Tab four script here
        pass

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

