import os
from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtCore import QStandardPaths

from widgets import ProjectWidget, FolderWidget

def getFiles(directory):
    # get a list of all the files in the directory
    files = os.listdir(directory)

    return files

def openFolder(window):
    folder_dir = QFileDialog.getExistingDirectory(window, 'Open Directory', QStandardPaths.standardLocations(QStandardPaths.StandardLocation.HomeLocation)[0])
    return folder_dir

def newFolder(window):
    window.FolderWidget = FolderWidget()
    window.FolderWidget.show()