import os
from PyQt6.QtWidgets import QMainWindow, QApplication, QListWidget, QPushButton, QMenu, QFileDialog, QLabel, QWidget
from PyQt6.QtCore import QStandardPaths
from PyQt6 import uic
from PyQt6.QtGui import QPixmap
import sys

class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()

        self.seleced_folder = None

        ui_file = 'productive_app_1.ui'
        
        # Load the UI file
        uic.loadUi(ui_file, self)

        # define home screen
        self.homeScreenContainer = QWidget(self)

        # define widgets
        self.openFolderBtnHome = self.findChild(QPushButton, 'openFolderBtn_home')
        self.newFolderBtnHome = self.findChild(QPushButton, 'newFolderBtn_home')
        self.rencentsLabel = self.findChild(QLabel, 'label')
        self.windowTitle = self.findChild(QMainWindow, 'windowTitle')

        self.folderContentsListWidget = self.findChild(QListWidget, 'folderContentsListWidget')
        self.folderContentsListWidget.hide()

        # define signals
        self.openFolderBtnHome.clicked.connect(self.openFolder)

        # show the window
        self.show()

    def openFolder(self):
        folder_path = QFileDialog.getExistingDirectory(self, 'Open Directory', QStandardPaths.standardLocations(QStandardPaths.StandardLocation.HomeLocation)[0])
        if folder_path:  # if a folder has been selected
            self.seleced_folder = folder_path
            self.rencentsLabel.setText(self.seleced_folder)

            self.windowTitle = f'Productive App - {self.seleced_folder}'
            
            # Hide home screen widgets
            self.openFolderBtnHome.hide()
            self.newFolderBtnHome.hide()
            self.rencentsLabel.hide()

            # Show and populate the folder contents widget
            self.folderContentsListWidget.show()
            self.populateFolderContents(folder_path)

    def populateFolderContents(self, folder_path):
        self.folderContentsListWidget.clear()  # clear the list widget
        for item in os.listdir(folder_path):  # list the contents of the folder
            self.folderContentsListWidget.addItem(item)  # add each item to the list widget


app = QApplication(sys.argv)
UIWindow = UI()
app.exec()