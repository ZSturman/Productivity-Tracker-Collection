import os
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QListWidget, QFileDialog, QLabel)

Base = declarative_base()

class Folder(Base):
    __tablename__ = 'folders'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    # connect the project class to the folder class using a foreign key
    project_id = Column(Integer)


class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    folder_id = Column(Integer, ForeignKey('folders.id'))  # declare foreign key pointing to folders.id

    # relationship() to access the Folder instance
    folder = relationship('Folder', backref='projects')

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    project_id = Column(Integer, ForeignKey('projects.id'))  # declare foreign key pointing to projects.id

    # relationship() to access the Project instance
    project = relationship('Project', backref='tasks')

class MainWindow(QWidget):
    def __init__(self, session):
        super().__init__()
        self.session = session
        self.layout = QHBoxLayout()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 800, 400)
        self.setWindowTitle('Streamlit Like App')


        self.side_nav_container = QVBoxLayout()
        self.nav_one = QPushButton('Nav One')
        self.nav_two = QPushButton('Nav Two')
        self.nav_three = QPushButton('Nav Three')
        self.side_nav_container.addWidget(self.nav_one)
        self.side_nav_container.addWidget(self.nav_two)
        self.side_nav_container.addWidget(self.nav_three)



        self.folder_container = QVBoxLayout()
        self.folder_label = QLabel('Folders')
        self.folder_container.addWidget(self.folder_label)

        self.project_container = QVBoxLayout()
        self.project_label = QLabel('Projects')
        self.project_container.addWidget(self.project_label)

        self.task_container = QVBoxLayout()
        self.task_label = QLabel('Tasks')
        self.task_container.addWidget(self.task_label)

        self.layout.addLayout(self.side_nav_container)
        self.layout.addLayout(self.folder_container)
        self.layout.addLayout(self.project_container)
        self.layout.addLayout(self.task_container)
        self.setLayout(self.layout)





engine = create_engine('sqlite:///:memory:')  # replace with your own database URL
Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)

session = Session()

app = QApplication([])
window = MainWindow(session)
window.show()
app.exec()