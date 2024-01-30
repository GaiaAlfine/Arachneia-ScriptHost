import sys
import threading
import os
from PySide2.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QSizePolicy, QTabBar
from PySide2.QtGui import QPalette, QColor, QIcon, QPainter, QPen
from PySide2.QtCore import Qt, QSize, QRect

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
        # Set your desired tab height and width here
        return QSize(100, 100)  # Example: 100 width and 100 height

    def paintEvent(self, event):
        painter = QPainter(self)
        for index in range(self.count()):
            tabRect = self.tabRect(index)
            tabIcon = self.tabIcon(index)

            # Draw the outline
            outlineColor = Qt.gray if index != self.currentIndex() else Qt.white  # Change color for selected tab
            painter.setPen(QPen(outlineColor, 2))
            painter.drawRect(tabRect)

            # Center the icon
            iconSize = tabIcon.actualSize(tabRect.size())
            iconX = (tabRect.width() - iconSize.width()) // 2
            iconY = (tabRect.height() - iconSize.height()) // 2
            iconRect = QRect(tabRect.x() + iconX, tabRect.y() + iconY, iconSize.width(), iconSize.height())

            # Draw the icon
            tabIcon.paint(painter, iconRect)

class CustomTabWidget(QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTabBar(RotatedTabBar())  # Your custom RotatedTabBar
        self.setTabPosition(QTabWidget.West)  # Tabs on the left

    def paintEvent(self, event):
        painter = QPainter(self)
        selectedTabIndex = self.currentIndex()
        tabBarRect = self.tabBar().tabRect(selectedTabIndex)

        # Draw border around content area
        contentRect = self.rect()
        contentRect.adjust(tabBarRect.width(), 0, 0, 0)  # Adjust to exclude tab bar area

        # Set border color and style
        painter.setPen(QPen(Qt.blue, 2))  # Example: blue border

        # Draw the border, connecting it with the selected tab
        painter.drawLine(contentRect.topLeft(), tabBarRect.bottomLeft())
        painter.drawLine(contentRect.topRight(), contentRect.bottomRight())
        painter.drawLine(contentRect.bottomLeft(), contentRect.bottomRight())

        super().paintEvent(event)  # Call base class paint event


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabBar(RotatedTabBar())  # Use the custom tab bar
        self.tab_widget.setTabPosition(QTabWidget.West)  # Move tabs to the left

        # Icons for tabs (replace 'icon_path' with the actual path to your icon files)
        icons = [
            QIcon('Arachneia/icons/Arachneia.ico'),
            QIcon('Arachneia/icons/Arachneia.ico'),
            QIcon('Arachneia/icons/Arachneia.ico'),
            QIcon('Arachneia/icons/Arachneia.ico')
        ]

        # Add tabs with icons
        for i in range(4):
            tab = QWidget()
            self.tab_widget.addTab(tab, icons[i], "")  # Empty string for no text

        self.setCentralWidget(self.tab_widget)
        self.setWindowTitle("Arachneia V0.04")
        self.resize(1000, 600)
        self.setWindowIcon(QIcon('Arachneia/Arachneia.ico'))
        self.tab_widget.currentChanged.connect(self.loadTab)
        self.setupTabOne()

        # Adjust tab sizes
        for i in range(self.tab_widget.count()):
            self.tab_widget.tabBar().setBaseSize(QSize(100, 100))  # Set a fixed size for each tab

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
        layout.addWidget(input_textbox)  # Remove alignment argument

        # Convert button
        convert_button = QPushButton("Convert")
        layout.addWidget(convert_button)  # Remove alignment argument

        # Output label (same as input textbox)
        output_textbox = QLineEdit()
        layout.addWidget(output_textbox)  # Remove alignment argument

        # Set spacing and layout margins to zero
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        # Set the vertical size policy to Maximum for all widgets
        input_textbox.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        convert_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        output_textbox.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        # Add stretch to push all widgets to the top
        layout.addStretch(1)


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

