import os
import datetime
import json
from sqlalchemy import or_, create_engine, inspect
from PyQt6 import QtCore
from PyQt6.QtWidgets import QApplication, QWizard, QWizardPage, QVBoxLayout, QLabel, QLineEdit, QDialog, QPushButton, QGroupBox, QHBoxLayout, QComboBox, QDateEdit, QTimeEdit, QCheckBox, QSpinBox, QListWidget, QTextEdit, QFileDialog, QCalendarWidget, QRadioButton, QButtonGroup, QDateTimeEdit, QMessageBox, QTableWidget, QTableWidgetItem, QTreeWidgetItem, QTreeWidget, QCompleter
from PyQt6.QtCore import QDate, QTime, QRect, Qt, pyqtSignal, QDateTime
from user_settings.user_settings_db import UserSettings, create_user_settings_db, sessionmaker
from user_settings.user_defaults import folder_directory as default_folder_directory
from models.models import Folder, Project, Task, Deliverable, Milestone, Note, Attachment, ToDo
from custom_widgets.custom_widgets import NewTaskForm, NewSubTaskForm, NewDeliverableForm, NewMilestoneForm, NewToDoForm
from database.database import DatabaseManager


"""

make folders, tasks etc. saved to db when leaving page

"""

class DateTimeDialog(QDialog):
    date_selected = pyqtSignal(QDateTime)

    def __init__(self, parent=None):
        super().__init__(parent, Qt.WindowType.WindowStaysOnTopHint)

        layout = QVBoxLayout(self)

        self.calendar_widget = QCalendarWidget(self)
        self.calendar_widget.setGridVisible(True)
        layout.addWidget(self.calendar_widget)

        self.time_edit = QTimeEdit(self)
        layout.addWidget(self.time_edit)

        ok_button = QPushButton('Ok', self)
        ok_button.clicked.connect(self.select_date)
        layout.addWidget(ok_button)

    def select_date(self):
        date = self.calendar_widget.selectedDate()
        time = self.time_edit.time()
        datetime = QDateTime(date, time)
        self.date_selected.emit(datetime)
        self.close()

class MyLineEdit(QLineEdit):
    focused = QtCore.pyqtSignal()

    def focusInEvent(self, e):
        super(MyLineEdit, self).focusInEvent(e)
        self.focused.emit()



class Page1(QWizardPage):
    def __init__(self, db_manager, folder_directory, parent=None):
        super(Page1, self).__init__(parent)

        layout = QVBoxLayout(self)

        self.folder_group_box = QGroupBox('Folder Directory', self)
        self.folder_layout = QHBoxLayout(self.folder_group_box)  # Changed to QHBoxLayout

        self.db_manager = db_manager
        self.session = self.db_manager.session

        self.folder_directory=folder_directory

        # search the session for all folders and populate the combo box
        folders = [folder.title for folder in self.session.query(Folder).all()]
        self.folder_line_edit = QLineEdit(self.folder_group_box)
        completer = QCompleter(folders)
        self.folder_line_edit.setCompleter(completer)


        self.browse_button = QPushButton("Browse...", self.folder_group_box)
        self.browse_button.clicked.connect(self.browse_folder)

        self.folder_layout.addWidget(self.folder_line_edit)
        self.folder_layout.addWidget(self.browse_button)
        layout.addWidget(self.folder_group_box)

        self.selected_folder_label = QLabel(self)
        layout.addWidget(self.selected_folder_label)

        self.title_group_box = QGroupBox('Project Title', self)
        self.title_layout = QVBoxLayout(self.title_group_box)
        self.project_name_line_edit = QLineEdit(self.title_group_box)
        self.title_layout.addWidget(self.project_name_line_edit)
        layout.addWidget(self.title_group_box)

        self.setLayout(layout)

        # connect textChanged signal to completeChanged for both LineEdit's
        self.project_name_line_edit.textChanged.connect(self.completeChanged)
        self.folder_line_edit.textChanged.connect(self.completeChanged)

    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory()
        if folder:
            self.folder_line_edit.setText(folder)
            self.selected_folder_label.setText(f"Selected Folder: {folder}")
    
    def isComplete(self):
        # returns True only if both line edits have text
        return bool(self.project_name_line_edit.text()) and bool(self.folder_line_edit.text())
    
    def get_folder(self):
        return self.folder_line_edit.text()
    
    def get_project_title(self):
        return self.project_name_line_edit.text()

    def nextId(self):
        return 1



# Project Description, Priority and Status #
class Page2(QWizardPage):
    def __init__(self, db_manager, status_options, priority_options, parent=None):
        super(Page2, self).__init__(parent)

        layout = QVBoxLayout(self)

        self.description_group_box = QGroupBox('Description', self)
        self.description_layout = QVBoxLayout(self.description_group_box)
        self.description_line_edit = QTextEdit(self.description_group_box)
        self.description_layout.addWidget(self.description_line_edit)
        layout.addWidget(self.description_group_box)

        self.priority_group_box = QGroupBox('Priority', self)
        self.priority_layout = QVBoxLayout(self.priority_group_box)
        self.priority_combobox = QComboBox(self.priority_group_box)
        self.priority_combobox.addItems(priority_options)
        self.priority_layout.addWidget(self.priority_combobox)
        layout.addWidget(self.priority_group_box)

        self.status_group_box = QGroupBox('Status', self)
        self.status_layout = QVBoxLayout(self.status_group_box)
        self.status_line_edit = MyLineEdit(self.status_group_box)
        self.status_line_edit.setCompleter(QCompleter(status_options))
        self.status_line_edit.focused.connect(self.show_completer)
        self.status_line_edit.editingFinished.connect(lambda: self.update_options(self.status_line_edit, status_options))
        self.status_layout.addWidget(self.status_line_edit)
        layout.addWidget(self.status_group_box)

        self.setLayout(layout)

    def get_description(self):
        return self.description_line_edit.toPlainText()
    
    def set_description(self, description):
        self.description_line_edit.setText(description)

    def get_priority(self):
        return self.priority_combobox.currentText()
    
    def set_priority(self, priority):
        self.priority_combobox.setCurrentText(priority)

    def get_status(self):
        return self.status_line_edit.text()
    
    def set_status(self, status):
        self.status_line_edit.setText(status)

    def update_options(self, line_edit, options):
        text = line_edit.text()
        if text not in options:
            options.append(text)
            line_edit.setCompleter(QCompleter(options))

    def show_completer(self):
        self.sender().completer().complete()

    def nextId(self):
        return 2

class Page3(QWizardPage):
    def __init__(self, db_manager, parent=None):
        super(Page3, self).__init__(parent)
        layout = QVBoxLayout(self)

        # Estimated time to complete
        self.estimated_time_group_box = QGroupBox('Project Estimated Time', self)
        self.estimated_time_layout = QVBoxLayout(self.estimated_time_group_box)
        self.no_estimated_time_checkbox = QCheckBox("No Estimated Time", self.estimated_time_group_box)
        self.no_estimated_time_checkbox.setChecked(False)
        self.no_estimated_time_checkbox.stateChanged.connect(self.estimatedTimeCheckboxChanged)
        self.estimated_time_layout.addWidget(self.no_estimated_time_checkbox)
        self.project_estimated_time_spin_box = QSpinBox(self.estimated_time_group_box)
        self.project_estimated_time_spin_box.setMinimum(1)
        self.project_estimated_time_spin_box.setMaximum(1000)
        self.project_estimated_time_combo_box = QComboBox(self.estimated_time_group_box)
        self.project_estimated_time_combo_box.addItems(['Minutes', 'Hours', 'Days', 'Weeks', 'Months', 'Years'])
        self.estimated_time_layout.addWidget(self.project_estimated_time_spin_box)
        self.estimated_time_layout.addWidget(self.project_estimated_time_combo_box)
        layout.addWidget(self.estimated_time_group_box)

        # Start Date
        self.start_date_group_box = QGroupBox('Start Date', self)
        self.start_date_layout = QVBoxLayout(self.start_date_group_box)
        self.no_start_date_checkbox = QCheckBox('No start date', self.start_date_group_box)
        self.no_start_date_checkbox.setChecked(False)
        self.no_start_date_checkbox.stateChanged.connect(self.startDateCheckboxChanged)
        self.start_date_button = QPushButton('Select Date', self)
        self.start_date_button.clicked.connect(self.show_calendar_start_date)
        self.start_date_edit = QDateTimeEdit(self.start_date_group_box)
        self.start_date_layout.addWidget(self.no_start_date_checkbox)
        self.start_date_layout.addWidget(self.start_date_edit)
        self.start_date_layout.addWidget(self.start_date_button)
        layout.addWidget(self.start_date_group_box)

        # Due Date
        self.due_date_group_box = QGroupBox('Due Date', self)
        self.due_date_layout = QVBoxLayout(self.due_date_group_box)
        self.no_due_date_checkbox = QCheckBox('No due date', self.due_date_group_box)
        self.no_due_date_checkbox.setChecked(False)
        self.no_due_date_checkbox.stateChanged.connect(self.dueDateCheckboxChanged)
        self.due_date_button = QPushButton('Select Date', self)
        self.due_date_button.clicked.connect(self.show_calendar_due_date)
        self.due_date_edit = QDateTimeEdit(self.due_date_group_box)
        self.due_date_layout.addWidget(self.no_due_date_checkbox)
        self.due_date_layout.addWidget(self.due_date_edit)
        self.due_date_layout.addWidget(self.due_date_button)
        layout.addWidget(self.due_date_group_box)

        self.setLayout(layout)

    def nextId(self):
        return 3

    def show_calendar_start_date(self):
        self.datetime_dialog = DateTimeDialog()
        self.datetime_dialog.date_selected.connect(self.update_start_date)
        self.datetime_dialog.exec()

    def show_calendar_due_date(self):
        self.datetime_dialog = DateTimeDialog()
        self.datetime_dialog.date_selected.connect(self.update_due_date)
        self.datetime_dialog.exec()

    def update_start_date(self, datetime):
        self.start_date_edit.setDateTime(datetime)

    def update_due_date(self, datetime):
        self.due_date_edit.setDateTime(datetime)
        
    def dueDateCheckboxChanged(self):
        if self.no_due_date_checkbox.isChecked():
            self.due_date_button.setEnabled(False)
            self.due_date_edit.setEnabled(False)
        else:
            self.due_date_button.setEnabled(True)
            self.due_date_edit.setEnabled(True)

    def startDateCheckboxChanged(self):
        if self.no_start_date_checkbox.isChecked():
            self.start_date_button.setEnabled(False)
            self.start_date_edit.setEnabled(False)
        else:
            self.start_date_button.setEnabled(True)
            self.start_date_edit.setEnabled(True)

    def estimatedTimeCheckboxChanged(self):
        if self.no_estimated_time_checkbox.isChecked():
            self.project_estimated_time_spin_box.setEnabled(False)
            self.project_estimated_time_combo_box.setEnabled(False)
        else:
            self.project_estimated_time_spin_box.setEnabled(True)
            self.project_estimated_time_combo_box.setEnabled(True)

    
    def get_no_start_date(self):
        return self.no_start_date_checkbox.isChecked()
    def get_no_due_date(self):
        return self.no_due_date_checkbox.isChecked()
    def get_no_estimated_time(self):
        return self.no_estimated_time_checkbox.isChecked()
    def get_start_date(self):
        return self.start_date_edit.dateTime().toPyDateTime()
    def get_due_date(self):
        return self.due_date_edit.dateTime().toPyDateTime()
    def get_estimated_time(self):
        units = self.project_estimated_time_combo_box.currentText()
        if units == 'Minutes':
            return self.project_estimated_time_spin_box.value() * 60
        elif units == 'Hours':
            return self.project_estimated_time_spin_box.value() * 60 * 60
        elif units == 'Days':
            return self.project_estimated_time_spin_box.value() * 60 * 60 * 24
        elif units == 'Weeks':
            return self.project_estimated_time_spin_box.value() * 60 * 60 * 24 * 7
        elif units == 'Months':
            return self.project_estimated_time_spin_box.value() * 60 * 60 * 24 * 30
        elif units == 'Years':
            return self.project_estimated_time_spin_box.value() * 60 * 60 * 24 * 365
        else:
            return 0
    


class Page4(QWizardPage):
    def __init__(self, db_manager, category_options, goal_verb_options, genre_options, use_case_options, parent=None):
        super(Page4, self).__init__(parent)

        layout = QVBoxLayout(self)

        # Category
        self.category_group_box = QGroupBox('Category', self)
        self.category_layout = QVBoxLayout(self.category_group_box)
        self.category_line_edit = MyLineEdit(self.category_group_box)
        self.category_line_edit.setCompleter(QCompleter(category_options))
        self.category_line_edit.focused.connect(self.show_completer)
        self.category_line_edit.editingFinished.connect(lambda: self.update_options(self.category_line_edit, category_options))
        self.category_layout.addWidget(self.category_line_edit)
        layout.addWidget(self.category_group_box)

        # Goal Verb
        self.goal_verb_group_box = QGroupBox('Goal Verb', self)
        self.goal_verb_layout = QVBoxLayout(self.goal_verb_group_box)
        self.goal_verb_line_edit = MyLineEdit(self.goal_verb_group_box)
        self.goal_verb_line_edit.setCompleter(QCompleter(goal_verb_options))
        self.goal_verb_line_edit.focused.connect(self.show_completer)
        self.goal_verb_line_edit.editingFinished.connect(lambda: self.update_options(self.goal_verb_line_edit, goal_verb_options))
        self.goal_verb_layout.addWidget(self.goal_verb_line_edit)
        layout.addWidget(self.goal_verb_group_box)

        # Genre
        self.genre_group_box = QGroupBox('Genre', self)
        self.genre_layout = QVBoxLayout(self.genre_group_box)
        self.genre_line_edit = MyLineEdit(self.genre_group_box)
        self.genre_line_edit.setCompleter(QCompleter(genre_options))
        self.genre_line_edit.focused.connect(self.show_completer)
        self.genre_line_edit.editingFinished.connect(lambda: self.update_options(self.genre_line_edit, genre_options))
        self.genre_layout.addWidget(self.genre_line_edit)
        layout.addWidget(self.genre_group_box)

        # Use Case
        self.use_case_group_box = QGroupBox('Use Case', self)
        self.use_case_layout = QVBoxLayout(self.use_case_group_box)
        self.use_case_line_edit = MyLineEdit(self.use_case_group_box)
        self.use_case_line_edit.setCompleter(QCompleter(use_case_options))
        self.use_case_line_edit.focused.connect(self.show_completer)
        self.use_case_line_edit.editingFinished.connect(lambda: self.update_options(self.use_case_line_edit, use_case_options))
        self.use_case_layout.addWidget(self.use_case_line_edit)
        layout.addWidget(self.use_case_group_box)

        self.setLayout(layout)

    def get_category(self):
        return self.category_line_edit.text()

    def get_goal_verb(self):
        return self.goal_verb_line_edit.text()

    def get_genre(self):
        return self.genre_line_edit.text()

    def get_use_case(self):
        return self.use_case_line_edit.text()
    
    def update_options(self, line_edit, options):
        text = line_edit.text()
        if text not in options:
            options.append(text)
            line_edit.setCompleter(QCompleter(options))

    def show_completer(self):
        self.sender().completer().complete()

    def nextId(self):
        return 4

class Page5(QWizardPage):
    def __init__(self, db_manager, parent=None):
        super(Page5, self).__init__(parent)

        layout = QVBoxLayout(self)

        self.tasks_group_box = QGroupBox('Tasks', self)
        self.tasks_layout = QVBoxLayout(self.tasks_group_box)

        # use a QTreeWidget instead of a QTableWidget
        self.tasks_tree = QTreeWidget()
        self.tasks_tree.setColumnCount(3)
        self.tasks_tree.setHeaderLabels(['Name', 'Status', 'Due Date'])
        self.tasks_layout.addWidget(self.tasks_tree)
        
        add_button = QPushButton('Add Task')
        remove_button = QPushButton('Remove Task')
        add_button.clicked.connect(self.add_task)
        remove_button.clicked.connect(self.remove_task)
        
        button_layout = QHBoxLayout()
        button_layout.addWidget(add_button)
        button_layout.addWidget(remove_button)
        self.tasks_layout.addLayout(button_layout)
        
        layout.addWidget(self.tasks_group_box)
        
        self.setLayout(layout)

    def initializePage(self):
        # fill the tree with tasks when the page is shown
        for task in self.wizard().get_tasks():
            self.add_task_to_tree(task)

    def add_task(self):
        self.wizard().show_tasks_dialog()
        
    def add_task_to_tree(self, task):
        item = QTreeWidgetItem(self.tasks_tree)
        item.setText(0, task.title)
        item.setText(1, task.status)
        item.setText(2, task.due_date)

        for subtask in task.subtasks:
            subitem = QTreeWidgetItem(item)
            subitem.setText(0, subtask.title)
            subitem.setText(1, subtask.status)
            subitem.setText(2, subtask.due_date)

    def remove_task(self):
        selected_items = self.tasks_tree.selectedItems()
        if not selected_items:
            return
        for item in selected_items:
            if item.parent():
                # If the selected item has a parent, it's a subtask
                # We can remove it with takeChild
                parent = item.parent()
                parent.takeChild(parent.indexOfChild(item))
            else:
                # The selected item is a top-level task
                # We can remove it with takeTopLevelItem
                index = self.tasks_tree.indexOfTopLevelItem(item)
                self.tasks_tree.takeTopLevelItem(index)

    def nextId(self):
        return 5


class Page6(QWizardPage):
    def __init__(self, db_manager, parent=None):
        super(Page6, self).__init__(parent)

        layout = QVBoxLayout(self)

        self.deliverables_group_box = QGroupBox('Deliverables', self)
        self.deliverables_layout = QVBoxLayout(self.deliverables_group_box)

        # use a QTreeWidget instead of a QTableWidget
        self.deliverables_tree = QTreeWidget()
        self.deliverables_tree.setColumnCount(3)
        self.deliverables_tree.setHeaderLabels(['Name', 'Status', 'Due Date'])
        self.deliverables_layout.addWidget(self.deliverables_tree)
        
        add_button = QPushButton('Add Deliverable')
        remove_button = QPushButton('Remove Deliverable')
        add_button.clicked.connect(self.add_deliverable)
        remove_button.clicked.connect(self.remove_deliverable)
        
        button_layout = QHBoxLayout()
        button_layout.addWidget(add_button)
        button_layout.addWidget(remove_button)
        self.deliverables_layout.addLayout(button_layout)
        
        layout.addWidget(self.deliverables_group_box)
        
        self.setLayout(layout)

    def initializePage(self):
        # fill the tree with deliverables when the page is shown
        for deliverable in self.wizard().get_deliverables():
            self.add_deliverable_to_tree(deliverable)

    def add_deliverable(self):
        self.wizard().show_deliverables_dialog()
        
    def add_deliverable_to_tree(self, deliverable):
        item = QTreeWidgetItem(self.deliverables_tree)
        item.setText(0, deliverable.title)
        item.setText(1, deliverable.status)
        item.setText(2, deliverable.due_date)


    def remove_deliverable(self):
        selected_items = self.deliverables_tree.selectedItems()
        if not selected_items:
            return
        for item in selected_items:
            # The selected item is a top-level deliverable
            # We can remove it with takeTopLevelItem
            index = self.deliverables_tree.indexOfTopLevelItem(item)
            self.deliverables_tree.takeTopLevelItem(index)

    def nextId(self):
        return 6

class Page7(QWizardPage):
    def __init__(self, db_manager, parent=None):
        super(Page7, self).__init__(parent)

        layout = QVBoxLayout(self)


        self.milestones_group_box = QGroupBox('Milestones', self)
        self.milestones_layout = QVBoxLayout(self.milestones_group_box)

        # use a QTreeWidget instead of a QTableWidget
        self.milestones_tree = QTreeWidget()
        self.milestones_tree.setColumnCount(3)
        self.milestones_tree.setHeaderLabels(['Name', 'Status', 'Due Date'])
        self.milestones_layout.addWidget(self.milestones_tree)
        
        add_button = QPushButton('Add Milestone')
        remove_button = QPushButton('Remove Milestone')
        add_button.clicked.connect(self.add_milestone)
        remove_button.clicked.connect(self.remove_milestone)
        
        button_layout = QHBoxLayout()
        button_layout.addWidget(add_button)
        button_layout.addWidget(remove_button)
        self.milestones_layout.addLayout(button_layout)
        
        layout.addWidget(self.milestones_group_box)
        
        self.setLayout(layout)

    def initializePage(self):
        # fill the tree with milestones when the page is shown
        for milestone in self.wizard().get_milestones():
            self.add_milestone_to_tree(milestone)

    def add_milestone(self):
        self.wizard().show_milestones_dialog()
        
    def add_milestone_to_tree(self, milestone):
        item = QTreeWidgetItem(self.milestones_tree)
        item.setText(0, milestone.title)


    def remove_milestone(self):
        selected_items = self.milestones_tree.selectedItems()
        if not selected_items:
            return
        for item in selected_items:
            # The selected item is a top-level milestone
            # We can remove it with takeTopLevelItem
            index = self.milestones_tree.indexOfTopLevelItem(item)
            self.milestones_tree.takeTopLevelItem(index)

    def nextId(self):
        return 7


class Page8(QWizardPage):
    def __init__(self, db_manager, parent=None):
        super(Page8, self).__init__(parent)

        layout = QVBoxLayout(self)

        self.notes_group_box = QGroupBox('Notes', self)
        self.notes_layout = QVBoxLayout(self.notes_group_box)
        
        self.notes_list = QListWidget()
        self.notes_layout.addWidget(self.notes_list)
        
        add_button = QPushButton('Add Note')
        remove_button = QPushButton('Remove Note')
        add_button.clicked.connect(self.add_note)
        remove_button.clicked.connect(self.remove_note)
        
        button_layout = QHBoxLayout()
        button_layout.addWidget(add_button)
        button_layout.addWidget(remove_button)
        self.notes_layout.addLayout(button_layout)
        
        layout.addWidget(self.notes_group_box)
        
        self.setLayout(layout)
        
    def add_note(self):
        print('add note')

    def remove_note(self):
        print('remove note')

    def nextId(self):
        return -1  # -1 means this is the last page
    
class NewProjectWizard(QWizard):
    def __init__(self, parent=None):
        super(NewProjectWizard, self).__init__(parent)

        self.db_manager = DatabaseManager('sqlite:///productivity_app/data/test.db')

        self.category_options, self.goal_verb_options, self.genre_options, self.use_case_options, self.status_options, self.priority_options, self.group_by_options, self.folder_directory = self.get_user_settings()
        
        self.project = Project()

        self.page1 = Page1(self.db_manager, self.folder_directory)
        self.page2 = Page2(self.db_manager, self.status_options, self.priority_options)
        self.page3 = Page3(self.db_manager)
        self.page4 = Page4(self.db_manager, self.category_options, self.goal_verb_options, self.genre_options, self.use_case_options)
        self.page5 = Page5(self.db_manager)
        self.page6 = Page6(self.db_manager)
        self.page7 = Page7(self.db_manager)
        self.page8 = Page8(self.db_manager)

        self.addPage(self.page1)
        self.addPage(self.page2)
        self.addPage(self.page3)
        self.addPage(self.page4)
        self.addPage(self.page5)
        self.addPage(self.page6)
        self.addPage(self.page7)
        self.addPage(self.page8)

        self.project_tasks = []
        self.project_milestones = []
        self.project_deliverables = []

        self.tasksDialog = NewTaskForm(self)
        self.deliverablesDialog = NewDeliverableForm(self)
        self.milestonesDialog = NewMilestoneForm(self.project_tasks.copy(), self.project_deliverables.copy(), self)



        self.tasksDialog.task_info_emitted.connect(self.add_task_to_project)
        self.deliverablesDialog.deliverable_info_emitted.connect(self.add_deliverable_to_project)
        self.milestonesDialog.milestone_info_emitted.connect(self.add_milestone_to_project)


    def get_user_settings(self):
        # create engine and session for the user_settings db
        engine = create_engine('sqlite:///productivity_app/user_settings/user_settings.db')
        Session = sessionmaker(bind=engine)
        session = Session()

        # check if the user_settings table exists
        inspector = inspect(engine)
        if 'user_settings' not in inspector.get_table_names():
            create_user_settings_db()

        # get the settings from the db
        category_options = json.loads(session.query(UserSettings).filter(UserSettings.name == 'category_options').first().options)
        goal_verb_options = json.loads(session.query(UserSettings).filter(UserSettings.name == 'goal_verb_options').first().options)
        genre_options = json.loads(session.query(UserSettings).filter(UserSettings.name == 'genre_options').first().options)
        use_case_options = json.loads(session.query(UserSettings).filter(UserSettings.name == 'use_case_options').first().options)
        status_options = json.loads(session.query(UserSettings).filter(UserSettings.name == 'status_options').first().options)
        priority_options = json.loads(session.query(UserSettings).filter(UserSettings.name == 'priority_options').first().options)
        group_by_options = json.loads(session.query(UserSettings).filter(UserSettings.name == 'group_by_options').first().options)

        folder_directory_db = session.query(UserSettings).filter(UserSettings.name == 'folder_directory').first()
        if folder_directory_db:
            folder_directory = folder_directory_db.options
        else:
            folder_directory = default_folder_directory  # from user_settings.user_defaults

        session.close()

        # return the options
        return category_options, goal_verb_options, genre_options, use_case_options, status_options, priority_options, group_by_options, folder_directory
    
    def add_task_to_project(self, task_title, task_description, task_status, task_priority, task_category, task_goal_verb, task_genre, task_use_case, task_estimated_time_checkbox, task_estimated_time, task_start_date_checkbox, task_start_date, task_due_date_checkbox, task_due_date, task_subtasks):
        # Create a new task and add it to the project's task list
        task = Task(title=task_title, description=task_description, status=task_status, priority=task_priority, category=task_category, goal_verb=task_goal_verb, genre=task_genre, use_case=task_use_case, estimated_time_to_complete_checkbox=task_estimated_time_checkbox, estimated_time_to_complete=task_estimated_time, no_start_date=task_start_date_checkbox, start_date=task_start_date, no_due_date=task_due_date_checkbox, due_date=task_due_date, subtasks=task_subtasks)

        self.project_tasks.append(task)

        # Add the task to the tree in Page5
        self.page5.add_task_to_tree(task)

        # Clear the dialog's fields
        self.tasksDialog.clear_fields()

    def add_deliverable_to_project(self, deliverable_title, deliverable_description, deliverable_status, deliverable_priority, deliverable_category, deliverable_goal_verb, deliverable_genre, deliverable_use_case, deliverable_due_date_checkbox, deliverable_due_date, deliverable_dependencies, deliverable_quality_criteria, deliverable_acceptance_criteria):
        # Create a new deliverable and add it to the project's deliverable list
        deliverable = Deliverable(title=deliverable_title, description=deliverable_description, status=deliverable_status, priority=deliverable_priority, category=deliverable_category, goal_verb=deliverable_goal_verb, genre=deliverable_genre, use_case=deliverable_use_case, no_due_date=deliverable_due_date_checkbox, due_date=deliverable_due_date, dependencies=deliverable_dependencies, quality_criteria=deliverable_quality_criteria, acceptance_criteria=deliverable_acceptance_criteria)

        self.project_deliverables.append(deliverable)

        # Add the deliverable to the tree in Page7
        self.page6.add_deliverable_to_tree(deliverable)

        # Clear the dialog's fields
        self.deliverablesDialog.clear_fields()

    def add_milestone_to_project(self, milestone_title, milestone_description, milestone_category, milestone_goal_verb, milestone_genre, milestone_use_case, milestone_dependencies):
        # Create a new milestone and add it to the project's milestone list
        milestone = Milestone(title=milestone_title, description=milestone_description, category=milestone_category, goal_verb=milestone_goal_verb, genre=milestone_genre, use_case=milestone_use_case, dependencies=milestone_dependencies)

        print(milestone.dependencies)

        self.project_milestones.append(milestone)

        # Add the milestone to the tree in Page6
        self.page7.add_milestone_to_tree(milestone)

        # Clear the dialog's fields
        self.milestonesDialog.clear_fields()


    def get_tasks(self):
        return self.project.tasks
    
    def get_milestones(self):
        return self.project.milestones
    
    def get_deliverables(self):
        return self.project.deliverables

    def accept(self):
        self.project.folder_dir = self.page1.get_folder()
        self.project.title = self.page1.get_project_title()
        self.project.description = self.page2.get_description()
        self.project.status = self.page2.get_status()
        self.project.priority = self.page2.get_priority()

        self.project.estimated_time_to_complete_checkbox = self.page3.get_no_estimated_time()
        self.project.estimated_time_to_complete = self.page3.get_estimated_time()
        self.project.no_start_date = self.page3.get_no_start_date()
        self.project.start_date = self.page3.get_start_date()
        self.project.no_due_date = self.page3.get_no_due_date()
        self.project.due_date = self.page3.get_due_date()

        self.project.category = self.page4.get_category()
        self.project.goal_verb = self.page4.get_goal_verb()
        self.project.genre = self.page4.get_genre()
        self.project.use_case = self.page4.get_use_case()

        self.project.tasks = self.project_tasks
        self.project.milestones = self.project_milestones
        self.project.deliverables = self.project_deliverables

        return super(NewProjectWizard, self).accept()
    
    def reject(self):
        return super(NewProjectWizard, self).reject()


    def show_tasks_dialog(self):
        self.tasksDialog.show()

    def show_milestones_dialog(self):
        self.milestonesDialog.show()

    def show_deliverables_dialog(self):
        self.deliverablesDialog.show()
