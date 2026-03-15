from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QListWidget, QFileDialog, QLabel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

Base = declarative_base()

class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True)
    name = Column(String)

class MainWindow(QWidget):
    def __init__(self, session):
        super().__init__()
        self.session = session
        self.layout = QVBoxLayout()

        # Create a horizontal layout for the text field and the button
        self.horizontal_layout = QHBoxLayout()
        self.text_field = QLineEdit()
        self.submit_button = QPushButton('Create Folder')
        self.submit_button.clicked.connect(self.create_folder)
        self.horizontal_layout.addWidget(self.text_field)
        self.horizontal_layout.addWidget(self.submit_button)

        # Create another horizontal layout for the list widget and the button
        self.horizontal_layout_2 = QHBoxLayout()
        self.folder_list = QListWidget()
        self.browse_button = QPushButton('Browse Folders')
        self.browse_button.clicked.connect(self.browse_folders)
        self.horizontal_layout_2.addWidget(self.folder_list)
        self.horizontal_layout_2.addWidget(self.browse_button)

        # Add the horizontal layouts to the main vertical layout
        self.layout.addLayout(self.horizontal_layout)
        self.layout.addLayout(self.horizontal_layout_2)
        self.setLayout(self.layout)

    def create_folder(self):
        folder_name = self.text_field.text()
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
            self.folder_list.addItem(folder_name)
            project = Project(name=folder_name)
            self.session.add(project)
            self.session.commit()

    def browse_folders(self):
        folder_name = QFileDialog.getExistingDirectory(self, "Select Directory")
        if folder_name:
            self.folder_list.addItem(folder_name)

engine = create_engine('sqlite:///:memory:')  # replace with your own database URL
Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)

session = Session()

app = QApplication([])
window = MainWindow(session)
window.show()
app.exec()
