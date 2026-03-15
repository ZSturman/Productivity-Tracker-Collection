import os
import PyQt6.QtWidgets as qtw
from models import Project, Task, Deliverable, Milestone
from database import Session

class FolderWidget(qtw.QWidget):
    def __init__(self):
        super().__init__()

        self.layout = qtw.QFormLayout(self)

        self.title = qtw.QLineEdit(self)

        self.layout.addRow('Title:', self.title)

        self.btn_save = qtw.QPushButton('Save', self)
        self.layout.addRow(self.btn_save)

        self.btn_save.clicked.connect(self.save_folder)

    def save_folder(self):
        folder_title = self.title.text()
        if folder_title:
            os.mkdir(folder_title)
            self.selectedFolder = folder_title
            self.updateCentralWidget()



class ProjectWidget(qtw.QWidget):
    def __init__(self):
        super().__init__()

        self.layout = qtw.QFormLayout(self)

        self.title = qtw.QLineEdit(self)
        self.description = qtw.QTextEdit(self)
        self.status = qtw.QLineEdit(self)
        self.priority = qtw.QLineEdit(self)
        self.completed = qtw.QCheckBox(self)

        self.layout.addRow('Title:', self.title)
        self.layout.addRow('Description:', self.description)
        self.layout.addRow('Status:', self.status)
        self.layout.addRow('Priority:', self.priority)
        self.layout.addRow('Completed:', self.completed)

        self.btn_save = qtw.QPushButton('Save', self)
        self.layout.addRow(self.btn_save)

        self.btn_save.clicked.connect(self.save_project)

    def save_project(self):
        session = Session()
        project = Project()
        project.title = self.title.text()
        project.description = self.description.toPlainText()
        project.status = self.status.text()
        project.priority = self.priority.text()
        project.completed = self.completed.isChecked()

        project.date_created = QtCore.QDateTime.currentDateTime()
        project.date_modified = QtCore.QDateTime.currentDateTime()
        """ project.folder_dir = 
        project.identifying_type
        project.actual_time_to_complete
        project.title
        project.description
        project.status
        project.priority
        project.completed
        project.datetime_completed
        project.no_start_date
        project.start_date
        project.estimated_time_to_complete_checkbox
        project.estimated_time_to_complete
        project.no_due_date
        project.datetime_due
        project.category
        project.goal_verb
        project.genre
        project.use_case
        project.deliverables
        project.tasks
        project.milestones """

        session.add(project)
        session.commit()
        self.close()

        # create JSON file from project
        project_json = project.to_json()
        with open(f'{project.title}.json', 'w') as f:
            f.write(project_json)

