from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QWidget, QListWidget, QSplitter, QPlainTextEdit
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt

from functions import getFiles
from widgets import ProjectWidget, FolderWidget

class ProductivityAppMain(QMainWindow):
    def __init__(self, openFolder, newFolder, session):
        super().__init__()
        self.setWindowTitle('Productivity App')
        self.setMinimumSize(500, 200)
        self.openFolder = openFolder
        self.newFolder = newFolder
        self.selectedFolder = None
        self.session = session
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout(self)
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')

        openFolderAction = QAction('Open Folder', self)
        openFolderAction.triggered.connect(self.openFolderWrapper)
        fileMenu.addAction(openFolderAction)

        newFolderAction = QAction('New Folder', self)
        newFolderAction.triggered.connect(self.newFolder)
        fileMenu.addAction(newFolderAction)

        # set up the new project action and add it to the file menu
        # if selectedFolder in None, then the action should be disabled
        newProjectAction = QAction('New Project', self)
        newProjectAction.triggered.connect(self.create_project)
        fileMenu.addAction(newProjectAction)


        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.setCentralWidget(self.splitter)

        self.textbox = QPlainTextEdit()
        self.textbox.setReadOnly(True)

        self.updateCentralWidget()

    def create_project(self):
        self.project_widget = ProjectWidget()
        self.project_widget.show()

    def create_Folder(self):
        self.folder_widget = FolderWidget()
        self.folder_widget.show()


    def openFolderWrapper(self):
        folder_dir = self.openFolder(self)

        if folder_dir:  # Make sure a folder was selected
            self.selectedFolder = folder_dir
            self.updateCentralWidget()

    def updateCentralWidget(self):
        if self.selectedFolder is None:
            self.openFolderButton = QPushButton("Open Folder")
            self.newFolderButton = QPushButton("New Folder")

            self.openFolderButton.clicked.connect(self.openFolderWrapper)
            self.newFolderButton.clicked.connect(self.newFolder)

            layout = QVBoxLayout()
            layout.addWidget(self.openFolderButton)
            layout.addWidget(self.newFolderButton)
            widget = QWidget()
            widget.setLayout(layout)

            self.splitter.addWidget(widget)
        else:
            # remove all widgets from the splitter
            for i in reversed(range(self.splitter.count())):
                self.splitter.widget(i).deleteLater()
            self.files = getFiles(self.selectedFolder)
            self.fileList = QListWidget()
            self.fileList.addItems(self.files)
            self.fileList.itemClicked.connect(self.fileClicked)

            self.splitter.addWidget(self.fileList)
            self.splitter.addWidget(self.textbox)

            self.newProjectButton = QPushButton("New Project")
            self.newProjectButton.clicked.connect(self.create_project)

            layout = QVBoxLayout()
            layout.addWidget(self.newProjectButton)
            layout.addWidget(self.fileList)
            widget = QWidget()
            widget.setLayout(layout)

            self.splitter.addWidget(widget)
            self.splitter.addWidget(self.textbox)

    def fileClicked(self, item):
        # get the file type from the file name
        file_type = item.text().split('.')[-1]

        # if the file type is txt, read the file and display the contents
        if file_type == 'txt':
            with open(f'{self.selectedFolder}/{item.text()}', 'r') as f:
                file_contents = f.read()
                self.textbox.setPlainText(file_contents)
        # if the file type is an image type, display the image
        elif file_type in ['png', 'jpg', 'jpeg', 'gif']:
            self.textbox.setPlainText('Image file selected') 
        # if the file type is not txt or an image, display the file type
        else:
            self.textbox.setPlainText(f'File type: {file_type}')

