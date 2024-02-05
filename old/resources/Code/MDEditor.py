import sys
from PySide2.QtWidgets import (QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget, QPushButton,
                               QHBoxLayout, QFileDialog)
from PySide2.QtCore import Slot
import markdown

class MarkdownEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Markdown Editor with Preview")
        self.setGeometry(100, 100, 1200, 600)  # Adjusted for better side-by-side layout
        
        # Main layout
        mainLayout = QVBoxLayout()
        
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
        current_scroll_position = self.preview.verticalScrollBar().value()  # Store current scroll position
        html_content = markdown.markdown(md_text)
        self.preview.setHtml(html_content)
        self.preview.verticalScrollBar().setValue(current_scroll_position)  # Set back the scroll position

    
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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    editor = MarkdownEditor()
    editor.show()
    sys.exit(app.exec_())
