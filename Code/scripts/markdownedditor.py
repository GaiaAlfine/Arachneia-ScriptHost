from PySide2.QtWidgets import (QPushButton, QFileDialog, QVBoxLayout, QWidget, QLabel, QHBoxLayout, QTextEdit, QApplication, QScrollBar)
from PySide2.QtCore import Qt, Slot
import markdown
import sys

class MarkdownEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Main layout
        mainLayout = QVBoxLayout()
        titleLabel = QLabel("Markdown Editor")
        titleLabel.setAlignment(Qt.AlignCenter)
        mainLayout.addWidget(titleLabel)

        # Buttons layout
        buttonsLayout = QHBoxLayout()
        openButton = QPushButton("Open")
        openButton.clicked.connect(self.openFile)
        saveButton = QPushButton("Save")
        saveButton.clicked.connect(self.saveFile)
        newButton = QPushButton("New")
        newButton.clicked.connect(self.newFile)

        buttonsLayout.addWidget(openButton)
        buttonsLayout.addWidget(saveButton)
        buttonsLayout.addWidget(newButton)
        mainLayout.addLayout(buttonsLayout)

        # Editor and Preview layout
        editorPreviewLayout = QHBoxLayout()

        self.editor = QTextEdit()
        self.editor.textChanged.connect(self.updatePreview)

        self.preview = QTextEdit()
        self.preview.setReadOnly(True)

        editorPreviewLayout.addWidget(self.editor)
        editorPreviewLayout.addWidget(self.preview)
        mainLayout.addLayout(editorPreviewLayout)

        self.setLayout(mainLayout)

    @Slot()
    def updatePreview(self):
        md_text = self.editor.toPlainText()
        current_scroll_position = self.preview.verticalScrollBar().value()
        html_content = markdown.markdown(md_text)
        self.preview.setHtml(html_content)
        self.preview.verticalScrollBar().setValue(current_scroll_position)

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

def get_tab_widget():
    widget = MarkdownEditor()
    return widget
