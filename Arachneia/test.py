from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QTabWidget, QSizePolicy
from PyQt5.QtGui import QColor, QPalette, QResizeEvent
import sys

class CustomColorWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.backgroundColor = '#4d4d4d'
        self.textColor = '#FFFFFF'
        self.borderColor = '#8b8b8b'
        self.initializeUI()

    def initializeUI(self):
        self.setGeometry(100, 100, 600, 400)
        self.setWindowTitle('Custom Color Window with Tabs')

        self.setBackgroundColor(self.backgroundColor)

        self.tabWidget = QTabWidget(self)
        self.styleTabs()
        self.addTabWidgets()

        layout = QVBoxLayout()
        layout.addWidget(self.tabWidget)
        self.setLayout(layout)

    def setBackgroundColor(self, color):
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor(color))
        self.setPalette(palette)

    def addTabWidgets(self):
        tab1 = QLabel("Content of Tab 1")
        tab2 = QLabel("Content of Tab 2")
        tab3 = QLabel("Content of Tab 3")

        self.tabWidget.addTab(tab1, "Tab 1")
        self.tabWidget.addTab(tab2, "Tab 2")
        self.tabWidget.addTab(tab3, "Tab 3")

    def styleTabs(self):
        self.tabWidget.setStyleSheet(f"""
            QTabWidget::pane {{ 
                border-top: 0px solid {self.borderColor}; /* Remove top border where tabs are */
                border-left: 1px solid {self.borderColor}; /* Keep left border */
                border-right: 1px solid {self.borderColor}; /* Keep right border */
                border-bottom: 1px solid {self.borderColor}; /* Keep bottom border */
                position: absolute; /* This may be adjusted based on your layout needs */
            }}
            QTabBar::tab:selected {{ 
                background: {self.backgroundColor}; 
                color: {self.textColor}; 
                border: 1px solid {self.borderColor};  
                border-bottom-color: transparent; /* Make the bottom border transparent */
            }}
            QTabBar::tab:!selected {{ 
                background: {self.backgroundColor}; 
                color: {self.textColor}; 
                border: 1px solid {self.borderColor}; 
            }}
            
            QTabBar::tab {{ 
                background: {self.backgroundColor}; 
                color: {self.textColor}; 
                width: 100%;
                padding: 5px 10px; /* Adjust padding as needed */
            }}
        """)

    def adjustTabWidths(self):
        tabCount = self.tabWidget.count()
        if tabCount > 0:
            totalWidth = self.tabWidget.width()
            tabWidth = max(100, totalWidth // tabCount)  # Ensure a minimum tab width, adjust as needed
            self.tabWidget.setStyleSheet(f"""
                QTabBar::tab {{
                    min-width: {tabWidth}px;
                }}
            """)

    def resizeEvent(self, event: QResizeEvent):
        super().resizeEvent(event)
        self.adjustTabWidths()  # Adjust the tab widths based on the new window size

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CustomColorWindow()
    window.show()
    sys.exit(app.exec_())
