# Inside script1.py
from PySide2.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton
from PySide2.QtCore import Qt
import markdown

def get_tab_widget():
    widget = QWidget()
    layout = QVBoxLayout(widget)
    
    text_edit = QTextEdit()
    text_edit.setReadOnly(True)
    text_edit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
    layout.addWidget(text_edit)
    
    # Load Markdown file content
    # def load_markdown_file(filepath='../README.md'):
    #     with open(filepath, 'r', encoding='utf-8') as file:
    #         content = markdown.markdown(file.read())
    #         text_edit.setHtml(content)
    
    # load_markdown_file()
    

    
    return widget
