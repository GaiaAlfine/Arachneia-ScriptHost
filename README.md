# Arachneia

Arachneia is a dynamic, modular application designed to seamlessly integrate and manage a variety of Python scripts, each offering distinct functionality within individual tabs of the main GUI. Built with flexibility in mind, Arachneia allows for the easy addition, removal, and management of these scripts through a JSON configuration file, facilitating a customizable and expandable toolset for a wide range of tasks.

## What is Arachneia?

Arachneia is a PyQt/PySide2-based desktop application that serves as a host for various Python scripts, each loaded into its own tab within the application's main window. This design enables users to have a single, unified interface for multiple tools and utilities, ranging from file viewers and editors to data visualization tools.

## Features

- **Dynamic Script Loading**: Scripts are loaded dynamically from a specified directory, allowing users to add or remove scripts without altering the main application code.
- **Tabbed Interface**: Each script operates within its own tab, ensuring that tools are neatly organized and easily accessible.
- **Configurable Through JSON**: Scripts and their metadata, such as names and icons, are configured using a JSON file, making it simple to customize the application's functionality.
- **Isolated Script Execution**: Scripts are executed in isolation, enhancing stability by ensuring that errors in one script do not affect others or the main application.
- **Extendable**: Developers can easily extend the application by creating new scripts, following the provided guidelines for structure and integration.

## Tutorial

###First create a code with the normal code structure with a gui using pyside2

###Then change the end of the code.

before: 
>
app = QApplication(sys.argv)<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; mainWindow = URLExtractorApp()<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; mainWindow.show()<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; sys.exit(app.exec_())<br>


After: 
>
def get_tab_widget():<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; widget = URLExtractorApp()<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; return widget<br>


###import icons into the program

The icons need to be white and thay have to be rotated 90 degrees to the right.

The icons can not be .ico it has to be a png file.

---
## File Structure

Arachneia/<br>
│<br>
├── Arachneia.py                 # Main application file<br>
├── tab_config.json              # Configuration file for tabs<br>
│<br>
├── scripts/                     # Directory for scripts<br>
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── __init__.py              # Makes Python treat the directories as containing packages<br>
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── script1.py               # First script (example: Markdown viewer)<br>
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── script2.py               # Second script (additional scripts can be added)<br>
│<br>
└── icons/                       # Directory for icons used by the application<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── home.png<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── icon.png<br>

## Updates
>###Update notes V0.2.9
- **Core Changes Programing**
- Changed the core of the program. now the program runs scripts form a folder called scripts.

>### Update notes V0.2.0
- **Version 0.2.0 (File Copy and Markdown Editor)**:
- Added File Copy and Markdown editor.
- Fixed some names inside code.
- Fixed some broken code inside **URL extractor**.
- Made the program an executeble.


>### Update Notes V0.1.7
- **Version 0.1.7 (URLs and Date)**:
- Added URL Extracor and Date Translator.
- Implemented a stop button to halt script execution at any point.
- Added a progress bar and time estimate for better user feedback.
- Improved the graphical user interface (GUI) for cleaner navigation.
- Added title name for which tab the user is on.
