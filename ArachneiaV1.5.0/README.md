# Arachneia Application Documentation

## Overview

Arachneia is a versatile application designed to leverage the power of PyQt5 for building a dynamic and customizable user interface. It incorporates a tab-based structure allowing users to manage and execute scripts within a unified environment. This document outlines the core functionalities, setup procedures, and key components of Arachneia.

### Key Features

- Dynamic script loading and execution
- Dark mode interface for enhanced visual comfort
- Customizable tabs for organizing scripts
- Integrated settings for script management
- Version 2.0.0

## Installation

### Requirements

- Python 3.x
- PyQt5
- PyInstaller (for creating an executable)

### Creating an Executable

To create an executable version of the Arachneia application, run the following command in the terminal:

```sh
pyinstaller --noconsole --windowed --icon=icons/Arachneia.ico --hidden-import=markdown --add-data "icons;icons" --add-data "scripts;scripts" Arachneia.pyw
```

This command packages the application with all its resources, ensuring it can run as a standalone executable.

## Usage

Upon launching Arachneia, users are greeted with a tabbed interface where each tab can represent a script or a functional module. The application starts with a default Home tab and dynamically adds tabs for scripts.

### Adding Scripts

Scripts can be added to the application in one way:

1. Through the "+" tab which opens a file dialog for selecting Python scripts.

### Script Conversion

Arachneia includes a utility function `convert_pyside2_to_pyqt5` that converts PySide2 scripts to PyQt5, facilitating the use of scripts initially developed for PySide2.

### Settings Window

The Settings window allows users to manage their scripts, including adding new scripts or removing existing ones from the application.

## Development

### Customization

Developers can customize Arachneia by modifying its source code. This includes adding new functionalities, customizing the UI, and extending the script execution capabilities.

### Dark Palette

A dark palette is implemented to provide a comfortable UI experience, especially beneficial for prolonged use.

## Components

### `MainWindow`

Serves as the primary window of the application, hosting the tab widget and menu bar.

### `SettingsWindow`

A dialog for managing scripts, accessible through the Settings menu.

### `RotatedTabBar`

A custom tab bar with rotated labels for a unique UI presentation.

## Conclusion

Arachneia offers a flexible platform for Python developers to run and manage scripts within a PyQt5-based interface. Its customizable nature allows for a wide range of applications, from simple script execution to complex application development.