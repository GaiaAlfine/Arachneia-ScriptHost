import sys
import os
from PySide2.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog, QGraphicsView, QGraphicsScene, QTreeWidget, QTreeWidgetItem, QDockWidget
from PySide2.QtGui import QPixmap
from PySide2.QtCore import Qt

class ImageViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Image Viewer with Dynamic Selection and Ordering')
        self.setGeometry(100, 100, 800, 600)
        self.folderPath = ''
        self.initUI()
        self.imageItems = {}

    def initUI(self):
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        
        self.layout = QVBoxLayout(self.centralWidget)
        
        self.btnOpenFolder = QPushButton('Open Folder')
        self.btnOpenFolder.clicked.connect(self.openFolder)
        
        self.graphicsView = QGraphicsView()
        self.scene = QGraphicsScene()
        self.graphicsView.setScene(self.scene)
        
        self.treeWidget = QTreeWidget()
        self.treeWidget.setHeaderLabels(["Folders and Images"])
        self.treeWidget.itemChanged.connect(self.handleItemChanged)
        
        self.dockWidget = QDockWidget("Folders and Images", self)
        self.dockWidget.setWidget(self.treeWidget)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dockWidget)
        
        self.layout.addWidget(self.btnOpenFolder)
        self.layout.addWidget(self.graphicsView)

    def openFolder(self):
        folderPath = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folderPath:
            self.folderPath = folderPath
            self.populateTree(folderPath)

    def populateTree(self, folderPath):
        self.treeWidget.clear()
        self.imageItems.clear()
        self.addTreeItems(folderPath, self.treeWidget.invisibleRootItem(), folderPath)
        self.treeWidget.expandAll()

    def addTreeItems(self, path, parentItem, rootPath):
        for entry in os.scandir(path):
            if entry.is_dir():
                folderItem = QTreeWidgetItem(parentItem, [entry.name])
                self.addTreeItems(entry.path, folderItem, rootPath)
            elif entry.name.lower().endswith('.png'):
                filePath = os.path.relpath(entry.path, rootPath)
                fileItem = QTreeWidgetItem(parentItem, [filePath])
                fileItem.setCheckState(0, Qt.Unchecked)

    def handleItemChanged(self, item, column):
        if item.checkState(column) == Qt.Checked:
            self.displayImage(item, True)
        else:
            self.displayImage(item, False)

    def displayImage(self, item, add):
        filePath = os.path.join(self.folderPath, item.text(0))
        if add:
            pixmap = QPixmap(filePath)
            pixmapItem = self.scene.addPixmap(pixmap)
            self.imageItems[item.text(0)] = pixmapItem
        else:
            if item.text(0) in self.imageItems:
                self.scene.removeItem(self.imageItems[item.text(0)])
                del self.imageItems[item.text(0)]

def get_tab_widget():
    widget = ImageViewer()
    return widget