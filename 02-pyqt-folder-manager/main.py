from PyQt6 import QtWidgets, QtGui
import sys
import os
from sqlalchemy.orm.exc import NoResultFound
from app.models import Session, Folder, Project, Task


class FolderApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.session = Session()
        self.setMinimumSize(500, 200)
        self.setWindowTitle("Folder Management")
        self.init_ui()
        self.connect_events()

    def init_ui(self):
        self.layout = QtWidgets.QVBoxLayout(self)
        self.btn_delete_selected = QtWidgets.QPushButton("Delete Selected Item")
        self.layout.addWidget(self.btn_delete_selected)
        self.create_folder_ui()
        self.create_project_ui()
        self.create_task_ui()
        self.create_refresh_button()

    def create_folder_ui(self):
        self.folder_list = self.create_list_widget()
        self.input_label = QtWidgets.QLabel("Folder Path")
        self.layout.addWidget(self.input_label)
        self.input_path = QtWidgets.QLineEdit()
        self.layout.addWidget(self.input_path)
        self.btn_new = QtWidgets.QPushButton("Create New Folder")
        self.layout.addWidget(self.btn_new)
        self.btn_delete_folder = QtWidgets.QPushButton("Delete Folder")
        self.layout.addWidget(self.btn_delete_folder)

    def create_project_ui(self):
        self.project_list = self.create_list_widget()
        self.project_name = QtWidgets.QLineEdit()
        self.project_name.setPlaceholderText("Enter Project Name")
        self.layout.addWidget(self.project_name)
        self.btn_add_project = QtWidgets.QPushButton("Add Project")
        self.layout.addWidget(self.btn_add_project)
        self.btn_delete_project = QtWidgets.QPushButton("Delete Project")
        self.layout.addWidget(self.btn_delete_project)
        self.btn_complete_project = QtWidgets.QPushButton("Mark Project as Complete")
        self.layout.addWidget(self.btn_complete_project)
        self.btn_list_projects = QtWidgets.QPushButton("List Projects in Folder")
        self.layout.addWidget(self.btn_list_projects)

    def create_task_ui(self):
        self.task_list = self.create_list_widget()
        self.task_name = QtWidgets.QLineEdit()
        self.task_name.setPlaceholderText("Enter Task Name")
        self.layout.addWidget(self.task_name)
        self.btn_add_task = QtWidgets.QPushButton("Add Task")
        self.layout.addWidget(self.btn_add_task)
        self.btn_delete_task = QtWidgets.QPushButton("Delete Task")
        self.layout.addWidget(self.btn_delete_task)
        self.btn_complete_task = QtWidgets.QPushButton("Mark Task as Complete")
        self.layout.addWidget(self.btn_complete_task)

    def create_list_widget(self):
        list_widget = QtWidgets.QListWidget()
        self.layout.addWidget(list_widget)
        return list_widget

    def create_refresh_button(self):
        self.btn_refresh = QtWidgets.QPushButton("Refresh Lists")
        self.layout.addWidget(self.btn_refresh)

    def connect_events(self):
        self.btn_refresh.clicked.connect(self.refresh_lists)
        self.btn_new.clicked.connect(self.new_folder)
        self.btn_delete_folder.clicked.connect(self.delete_folder)
        self.btn_add_project.clicked.connect(self.add_project)
        self.btn_delete_project.clicked.connect(self.delete_project)
        self.btn_complete_project.clicked.connect(self.complete_project)
        self.btn_list_projects.clicked.connect(self.list_projects)
        self.btn_add_task.clicked.connect(self.add_task)
        self.btn_delete_task.clicked.connect(self.delete_task)
        self.btn_complete_task.clicked.connect(self.complete_task)
        self.btn_delete_selected.clicked.connect(self.delete_selected_item)


    def new_folder(self):
        folder_path = self.input_path.text()
        os.makedirs(folder_path, exist_ok=True)
        folder = Folder(path=folder_path)
        self.session.add(folder)
        self.session.commit()
        QtWidgets.QMessageBox.information(self, "Success", "Folder created successfully!")

    def add_project(self):
        project_name = self.project_name.text()
        folder_path = self.input_path.text()
        folder = self.session.query(Folder).filter_by(path=folder_path).one()
        project = Project(name=project_name, folder=folder)
        self.session.add(project)
        self.session.commit()
        QtWidgets.QMessageBox.information(self, "Success", f"Project '{project_name}' added successfully!")

    def add_task(self):
        task_name = self.task_name.text()
        project_name = self.project_name.text()
        project = self.session.query(Project).filter_by(name=project_name).one()
        task = Task(name=task_name, project=project)
        self.session.add(task)
        self.session.commit()
        QtWidgets.QMessageBox.information(self, "Success", f"Task '{task_name}' added successfully!")


    def list_projects(self):
        folder_path = self.input_path.text()
        try:
            folder = self.session.query(Folder).filter_by(path=folder_path).one()
            projects = folder.projects
            project_names = [project.name for project in projects]
            QtWidgets.QMessageBox.information(self, "Projects in Folder", '\n'.join(project_names))
        except NoResultFound:
            QtWidgets.QMessageBox.information(self, "No Projects", "No projects found in this folder.")


    def refresh_lists(self):
        self.folder_list.clear()
        self.project_list.clear()
        self.task_list.clear()
        
        folders = self.session.query(Folder).all()
        for folder in folders:
            self.folder_list.addItem(folder.path)
        
        projects = self.session.query(Project).all()
        for project in projects:
            self.project_list.addItem(project.name)

        tasks = self.session.query(Task).all()
        for task in tasks:
            self.task_list.addItem(task.name)

    def delete_selected_item(self):
        if self.folder_list.currentItem() is not None:
            self.delete_folder()
        elif self.project_list.currentItem() is not None:
            self.delete_project()
        elif self.task_list.currentItem() is not None:
            self.delete_task()

    def delete_folder(self):
        folder_path = self.folder_list.currentItem().text()
        folder = self.session.query(Folder).filter_by(path=folder_path).one()
        self.session.delete(folder)
        self.session.commit()
        QtWidgets.QMessageBox.information(self, "Success", "Folder deleted successfully!")


    def delete_project(self):
        project_path = self.project_list.currentItem().text()
        project = self.session.query(Project).filter_by(name=project_path).one()
        self.session.delete(project)
        self.session.commit()
        QtWidgets.QMessageBox.information(self, "Success", "Project deleted successfully!")

    def delete_task(self):
        task_path = self.task_list.currentItem().text()
        task = self.session.query(Task).filter_by(name=task_path).one()
        self.session.delete(task)
        self.session.commit()
        QtWidgets.QMessageBox.information(self, "Success", "Task deleted successfully!")

    def complete_project(self):
        project_name = self.project_name.text()
        project = self.session.query(Project).filter_by(name=project_name).one()
        project.completed = True
        self.session.commit()
        QtWidgets.QMessageBox.information(self, "Success", f"Project '{project_name}' marked as completed!")

    def complete_task(self):
        task_name = self.task_name.text()
        task = self.session.query(Task).filter_by(name=task_name).one()
        task.completed = True
        self.session.commit()
        QtWidgets.QMessageBox.information(self, "Success", f"Task '{task_name}' marked as completed!")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = FolderApp()
    window.showMaximized()
    window.show()

    sys.exit(app.exec())