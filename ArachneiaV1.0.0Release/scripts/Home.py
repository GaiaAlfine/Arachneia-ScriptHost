from PySide2.QtWidgets import QWidget, QVBoxLayout, QTextEdit
from PySide2.QtCore import Qt
import markdown
import sys, os

def get_tab_widget():
    widget = QWidget()
    layout = QVBoxLayout(widget)
    
    text_edit = QTextEdit()
    text_edit.setReadOnly(True)
    text_edit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
    layout.addWidget(text_edit)

    def get_resource_path(relative_path):
        """ Convert relative resource paths to absolute paths, considering PyInstaller context. """
        if hasattr(sys, '_MEIPASS'):
            # If running in a PyInstaller bundle
            base_path = sys._MEIPASS
        else:
            # For development, use the directory of the script or another appropriate base path
            base_path = os.path.dirname(__file__)
            
        return os.path.join(base_path, relative_path)

    # When calling get_resource_path, use the correct relative path from your application's root
    filepath = get_resource_path(os.path.join('Arachneia', 'README.md'))



    def load_markdown_file():
        try:
            filepath = get_resource_path('README.md')  # Adjust if README.md is located elsewhere
            with open(filepath, 'r', encoding='utf-8') as file:
                content = markdown.markdown(file.read())
                text_edit.setHtml(content)
        except Exception as e:
            print(f"Error loading markdown file: {e}")
            text_edit.setPlainText(f"Failed to load content: {e}")

    load_markdown_file()
    
    return widget

# If this script is part of a larger application, ensure you integrate get_tab_widget()
# correctly with your application's window or widget structure.
