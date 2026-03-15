import os
import json
from sqlalchemy import create_engine, inspect
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QCheckBox, QLabel, QWidget, QFrame, QListWidget, QListWidgetItem, QPushButton, QScrollArea, QSizePolicy, QGraphicsOpacityEffect, QMessageBox, QComboBox, QDateEdit, QTimeEdit, QSpinBox, QLineEdit, QTextEdit, QGroupBox, QToolButton, QDateTimeEdit, QFileDialog, QGridLayout, QApplication, QCalendarWidget, QDialog, QTableWidgetItem, QTableWidget, QCompleter
from PyQt6.QtGui import QFont, QIntValidator
from PyQt6.QtCore import Qt, pyqtSignal, QDate, QTime, QObject, QAbstractTableModel, QDateTime, QStringListModel
from PyQt6 import QtWidgets, QtCore, QtGui

from user_settings.user_settings_db import UserSettings, create_user_settings_db, sessionmaker
from user_settings.user_defaults import folder_directory as default_folder_directory
from models.models import SubTask, Project, Task, Deliverable, Milestone
from database.database import DatabaseManager

class UpcomingListItem(QWidget):
    checkbox_toggled = pyqtSignal(object, bool)

    def __init__(self, item):
        super().__init__()

        # Save the item as an instance attribute
        self.item = item

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Create the checkbox
        self.checkbox = QCheckBox(self.item.title)
        self.checkbox.setChecked(self.item.completed)

        # Create the labels
        self.tableLabel = QLabel(self.item.__class__.__name__)

        # Convert the date to a string
        item_due_date = self.item.due_date.strftime("%m/%d/%Y")
        self.dueDateLabel = QLabel(item_due_date)

        # Add them to the layout
        self.layout.addWidget(self.checkbox, alignment=Qt.AlignmentFlag.AlignLeft)
        self.layout.addWidget(self.tableLabel, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.dueDateLabel, alignment=Qt.AlignmentFlag.AlignRight)

        self.checkbox.stateChanged.connect(self.emit_checkbox_toggled)

    def emit_checkbox_toggled(self, state):
        # We emit our own signal, converting the state to a bool (checked = True, unchecked = False)
        self.checkbox_toggled.emit(self.item, bool(state))

class KanbanListItem(QWidget):
    checkbox_toggled = pyqtSignal(object, bool)
    editClicked = pyqtSignal(object)
    deleteClicked = pyqtSignal(object)

    def __init__(self, item):
        super().__init__()

        self.item = item

        # Create a main layout for this widget
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        # Create a frame that will contain the actual item and apply the border to it
        self.item_frame = QFrame(self)
        self.item_frame.setStyleSheet("QFrame {border: 1px solid black; border-radius: 5px;}")
        self.main_layout.addWidget(self.item_frame)

        # Set layout for the frame
        self.layout = QVBoxLayout(self.item_frame)

        self.type_label = QLabel('identifying type', self)
        self.type_label.setStyleSheet('border: none; width: auto; height: auto;')
        self.type_label.setAlignment(Qt.AlignmentFlag.AlignLeading | Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.layout.addWidget(self.type_label)

        self.title_label = QLabel('Title', self)
        self.title_label.setStyleSheet('border: none; width: auto; height: auto;')
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignLeading | Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.title_label.setFont(QFont("", 30))
        self.layout.addWidget(self.title_label)

        self.folder_label = QLabel('Folder', self)
        self.folder_label.setStyleSheet('border: none; width: auto; height: auto;')
        self.folder_label.setAlignment(Qt.AlignmentFlag.AlignLeading | Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.layout.addWidget(self.folder_label)

        # Status
        self.status_frame = QFrame(self)
        self.status_frame.setStyleSheet('border: none; width: auto; height: auto;')
        self.status_layout = QHBoxLayout(self.status_frame)
        self.status_layout.setSpacing(12)
        self.status_label = QLabel('Status:', self.status_frame)
        self.status_label.setStyleSheet('border: none; width: auto; height: auto;')
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignLeading | Qt.AlignmentFlag.AlignLeft)
        self.current_status_label = QLabel('current_status', self.status_frame)
        self.current_status_label.setStyleSheet('border: none; width: auto; height: auto;')
        self.status_layout.addWidget(self.status_label)
        self.status_layout.addWidget(self.current_status_label)
        self.layout.addWidget(self.status_frame)

        # Priority
        self.priority_frame = QFrame(self)
        self.priority_frame.setStyleSheet('border: none; width: auto; height: auto;')
        self.priority_layout = QHBoxLayout(self.priority_frame)
        self.priority_layout.setSpacing(12)
        self.priority_label = QLabel('Priority:', self.priority_frame)
        self.priority_label.setStyleSheet('border: none; width: auto; height: auto;')
        self.item_priority_label = QLabel('item_priority', self.priority_frame)
        self.item_priority_label.setStyleSheet('border: none; width: auto; height: auto;')
        self.priority_layout.addWidget(self.priority_label)
        self.priority_layout.addWidget(self.item_priority_label)
        self.layout.addWidget(self.priority_frame)

        # Due date
        self.due_date_frame = QFrame(self)
        self.due_date_frame.setStyleSheet('border: none; width: auto; height: auto;')
        self.due_date_layout = QHBoxLayout(self.due_date_frame)
        self.due_date_layout.setSpacing(12)
        self.due_date_label = QLabel('Due Date:', self.due_date_frame)
        self.due_date_label.setStyleSheet('border: none; width: auto; height: auto;')
        self.item_due_date_label = QLabel('item_due_date', self.due_date_frame)
        self.item_due_date_label.setStyleSheet('border: none; width: auto; height: auto;')
        self.due_date_layout.addWidget(self.due_date_label)
        self.due_date_layout.addWidget(self.item_due_date_label)
        self.layout.addWidget(self.due_date_frame)

        item_id = str(item.id) if hasattr(item, 'id') else "undefined"

        # Complete, edit, delete
        self.action_frame = QFrame(self)
        self.action_frame.setStyleSheet('border: none; width: auto; height: auto;')
        self.action_layout = QHBoxLayout(self.action_frame)
        # remove margins
        self.action_layout.setContentsMargins(0, 0, 0, 0)
        self.action_layout.setSpacing(6)
        self.complete_check = QCheckBox(f'Complete', self.action_frame)
        self.edit_button = QPushButton(f'Edit', self.action_frame)
        self.delete_button = QPushButton(f'Delete', self.action_frame)
        self.action_layout.addWidget(self.complete_check)
        self.action_layout.addWidget(self.edit_button)
        self.action_layout.addWidget(self.delete_button)

        self.complete_check.stateChanged.connect(self.emit_checkbox_toggled)
        self.edit_button.clicked.connect(self.emit_edit_clicked)
        self.delete_button.clicked.connect(self.emit_delete_clicked)

        # make edit and delete buttons smaller
        self.edit_button.setFixedWidth(50)
        self.delete_button.setFixedWidth(50)
        # make edit and delete buttons look like buttons
        self.edit_button.setStyleSheet('border: 1px solid black; border-radius: 5px;')
        self.delete_button.setStyleSheet('border: 1px solid black; border-radius: 5px;')

        self.layout.addWidget(self.action_frame)

        # get the item class name and set that to the type label
        self.type_label.setText(item.__class__.__name__)
        self.title_label.setText(item.title)

        # if item has attribute folder_dir set the folder label to that
        if hasattr(item, 'folder_dir') and item.folder_dir is not None:
            # get the last folder name from the folder_dir
            folder_name = item.folder_dir.split('/')[-1]
            self.folder_label.setText(folder_name)

        # if item has attribute status set the current status label to that
        if hasattr(item, 'status') and item.status is not None:
            self.current_status_label.setText(item.status)

        # if item has attribute priority set the item priority label to that
        if hasattr(item, 'priority') and item.priority is not None:
            # if the priority is high set the text color to red
            if item.priority == 'High':
                self.item_priority_label.setStyleSheet('color: red; border: none; width: auto; height: auto;')
            # if the priority is medium set the text color to orange
            elif item.priority == 'Medium':
                self.item_priority_label.setStyleSheet('color: orange; border: none; width: auto; height: auto;')
            # if the priority is low set the text color to green
            elif item.priority == 'Low':
                self.item_priority_label.setStyleSheet('color: green; border: none; width: auto; height: auto;')

            self.item_priority_label.setText(item.priority)

        # if item has attribute due_date set the item due date label to that
        if hasattr(item, 'due_date') and item.due_date is not None:
            self.item_due_date_label.setText(item.due_date.strftime("%m/%d/%Y"))

        # if item has attribute completed set the checkbox to that
        if hasattr(item, 'completed') and item.completed is not None:
            self.complete_check.setChecked(item.completed)

    def emit_checkbox_toggled(self, state):
        # We emit our own signal, converting the state to a bool (checked = True, unchecked = False)
        self.checkbox_toggled.emit(self.item, bool(state))

    def emit_edit_clicked(self):
        self.editClicked.emit(self.item)

    def emit_delete_clicked(self):
        self.deleteClicked.emit(self.item)
 
class MyTableModel(QAbstractTableModel):

    def __init__(self, data, headers):
        super(MyTableModel, self).__init__()
        self._data = data
        self._headers = headers

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return len(self._data[0])

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            return self._data[index.row()][index.column()]

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return self._headers[section]
        return super().headerData(section, orientation, role)





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

class NewTaskForm(QtWidgets.QDialog, QObject):
    task_info_emitted = pyqtSignal(str, str, str, str, str, str, str, str, bool, int, bool, str, bool, str, list)

    def __init__(self, parent=None):
        super(NewTaskForm, self).__init__()

        self.layout = QtWidgets.QVBoxLayout(self)

        self.category_options, self.goal_verb_options, self.genre_options, self.use_case_options, self.status_options, self.priority_options = self.get_user_settings()

        self.scrollArea = QtWidgets.QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 380, 247))

        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.scrollAreaWidgetContents.setLayout(self.verticalLayout)  

        # add a title for the dialog box
        self.title_label = QLabel('New Task', self.scrollAreaWidgetContents)
        self.title_label.setStyleSheet('border: none; width: auto; height: auto;')
        self.title_label.setFont(QFont('Arial', 20))
        self.verticalLayout.addWidget(self.title_label)

        # add a label and line edit for the task name
        self.title_group_box = QGroupBox('Task Title', self.scrollAreaWidgetContents)
        self.title_layout = QVBoxLayout(self.title_group_box)
        self.task_title_line_edit = QLineEdit(self.title_group_box)
        self.title_layout.addWidget(self.task_title_line_edit)
        self.verticalLayout.addWidget(self.title_group_box)

        # add a label and text edit for the task description
        self.description_group_box = QGroupBox('Task Description', self.scrollAreaWidgetContents)
        self.description_layout = QVBoxLayout(self.description_group_box)
        self.task_description_text_edit = QTextEdit(self.description_group_box)
        self.description_layout.addWidget(self.task_description_text_edit)
        self.verticalLayout.addWidget(self.description_group_box)




        # add a label and combo box for the task status and priority and put them in a horizontal layout
        self.status_priority_container = QGroupBox('Task Status and Priority', self.scrollAreaWidgetContents)

        # create a vertical layout for priority label and priority combo box
        self.priority_container = QVBoxLayout()
        self.task_priority_label = QLabel('Task Priority')
        self.task_priority_combo_box = QComboBox()
        self.task_priority_combo_box.addItems(self.priority_options)
        self.task_priority_combo_box.setCurrentIndex(-1)
        self.priority_container.addWidget(self.task_priority_label)
        self.priority_container.addWidget(self.task_priority_combo_box)
        
        # create a vertical layout for status label and status combo box
        self.status_container = QVBoxLayout()
        self.task_status_label = QLabel('Task Status')
        self.status_line_edit = MyLineEdit()
        self.status_line_edit.setCompleter(QCompleter(self.status_options))
        self.status_line_edit.focused.connect(self.show_completer)
        self.status_line_edit.editingFinished.connect(lambda: self.update_options(self.status_line_edit, self.status_options))
        self.status_container.addWidget(self.task_status_label)
        self.status_container.addWidget(self.status_line_edit)



        # add the status and priority layouts to the horizontal layout
        self.status_priority_layout = QHBoxLayout(self.status_priority_container)
        self.status_priority_layout.addLayout(self.priority_container)
        self.status_priority_layout.addLayout(self.status_container)

        # add the status and priority container to the vertical layout
        self.verticalLayout.addWidget(self.status_priority_container)


        # create a group box for the task descriptors
        self.descriptors_container = QGroupBox('Task Descriptors', self.scrollAreaWidgetContents)

        # create a grid layout for the task descriptors
        self.descriptors_layout = QGridLayout(self.descriptors_container)

        # create a vertical layout for the task category label and combo box
        self.task_category_container = QVBoxLayout()
        self.task_category_label = QLabel('Task Category')
        self.task_category_line_edit = MyLineEdit()
        self.task_category_line_edit.setCompleter(QCompleter(self.category_options))
        self.task_category_line_edit.focused.connect(self.show_completer)
        self.task_category_line_edit.editingFinished.connect(lambda: self.update_options(self.task_category_line_edit, self.category_options))
        self.task_category_container.addWidget(self.task_category_label)
        self.task_category_container.addWidget(self.task_category_line_edit)

        # Task Goal Verb
        self.task_goal_verb_container = QVBoxLayout()
        self.task_goal_verb_label = QLabel('Task Goal Verb')
        self.task_goal_verb_line_edit = MyLineEdit()
        self.task_goal_verb_line_edit.setCompleter(QCompleter(self.goal_verb_options))
        self.task_goal_verb_line_edit.focused.connect(self.show_completer)
        self.task_goal_verb_line_edit.editingFinished.connect(lambda: self.update_options(self.task_goal_verb_line_edit, self.goal_verb_options))
        self.task_goal_verb_container.addWidget(self.task_goal_verb_label)
        self.task_goal_verb_container.addWidget(self.task_goal_verb_line_edit)

        # Task Genre
        self.task_genre_container = QVBoxLayout()
        self.task_genre_label = QLabel('Task Genre')
        self.task_genre_line_edit = MyLineEdit()
        self.task_genre_line_edit.setCompleter(QCompleter(self.genre_options))
        self.task_genre_line_edit.focused.connect(self.show_completer)
        self.task_genre_line_edit.editingFinished.connect(lambda: self.update_options(self.task_genre_line_edit, self.genre_options))
        self.task_genre_container.addWidget(self.task_genre_label)
        self.task_genre_container.addWidget(self.task_genre_line_edit)

        # Task Use Case
        self.task_use_case_container = QVBoxLayout()
        self.task_use_case_label = QLabel('Task Use Case')
        self.task_use_case_line_edit = MyLineEdit()
        self.task_use_case_line_edit.setCompleter(QCompleter(self.use_case_options))
        self.task_use_case_line_edit.focused.connect(self.show_completer)
        self.task_use_case_line_edit.editingFinished.connect(lambda: self.update_options(self.task_use_case_line_edit, self.use_case_options))
        self.task_use_case_container.addWidget(self.task_use_case_label)
        self.task_use_case_container.addWidget(self.task_use_case_line_edit)


        # add the task category, goal verb, genre and use case layouts to the grid layout
        self.descriptors_layout.addLayout(self.task_category_container, 0, 0)
        self.descriptors_layout.addLayout(self.task_goal_verb_container, 0, 1)
        self.descriptors_layout.addLayout(self.task_genre_container, 1, 0)
        self.descriptors_layout.addLayout(self.task_use_case_container, 1, 1)

        # add the descriptors container to the vertical layout
        self.verticalLayout.addWidget(self.descriptors_container)



        # create a horizontal layout for the estimated time, start date, and due date
        self.estimated_time_start_due_layout = QHBoxLayout(self.scrollAreaWidgetContents)

        # Estimated time to complete
        self.estimated_time_group_box = QGroupBox('Task Estimated Time', self)
        self.estimated_time_layout = QVBoxLayout(self.estimated_time_group_box)
        self.no_estimated_time_checkbox = QCheckBox("No Estimated Time", self.estimated_time_group_box)
        self.no_estimated_time_checkbox.setChecked(False)
        self.no_estimated_time_checkbox.stateChanged.connect(self.estimatedTimeCheckboxChanged)
        self.estimated_time_layout.addWidget(self.no_estimated_time_checkbox)
        self.task_estimated_time_spin_box = QSpinBox(self.estimated_time_group_box)
        self.task_estimated_time_spin_box.setMinimum(1)
        self.task_estimated_time_spin_box.setMaximum(1000)
        self.task_estimated_time_combo_box = QComboBox(self.estimated_time_group_box)
        self.task_estimated_time_combo_box.addItems(['Minutes', 'Hours', 'Days', 'Weeks', 'Months', 'Years'])
        self.estimated_time_layout.addWidget(self.task_estimated_time_spin_box)
        self.estimated_time_layout.addWidget(self.task_estimated_time_combo_box)

        # Start Date
        self.start_date_group_box = QGroupBox('Start Date', self)
        self.start_date_layout = QVBoxLayout(self.start_date_group_box)
        self.no_start_date_checkbox = QCheckBox('No start date', self.start_date_group_box)
        self.no_start_date_checkbox.setChecked(False)
        self.no_start_date_checkbox.stateChanged.connect(self.startDateCheckboxChanged)
        self.task_start_date_button = QPushButton('Select Date', self)
        self.task_start_date_button.clicked.connect(self.show_calendar_start_date)
        self.task_start_date_edit = QDateTimeEdit(self.start_date_group_box)
        self.start_date_layout.addWidget(self.no_start_date_checkbox)
        self.start_date_layout.addWidget(self.task_start_date_edit)
        self.start_date_layout.addWidget(self.task_start_date_button)

        # Due Date
        self.due_date_group_box = QGroupBox('Due Date', self)
        self.due_date_layout = QVBoxLayout(self.due_date_group_box)
        self.no_due_date_checkbox = QCheckBox('No due date', self.due_date_group_box)
        self.no_due_date_checkbox.setChecked(False)
        self.no_due_date_checkbox.stateChanged.connect(self.dueDateCheckboxChanged)
        self.task_due_date_button = QPushButton('Select Date', self)
        self.task_due_date_button.clicked.connect(self.show_calendar_due_date)
        self.task_due_date_edit = QDateTimeEdit(self.due_date_group_box)
        self.due_date_layout.addWidget(self.no_due_date_checkbox)
        self.due_date_layout.addWidget(self.task_due_date_edit)
        self.due_date_layout.addWidget(self.task_due_date_button)

        # add the estimated time, start date, and due date layouts to the horizontal layout
        self.estimated_time_start_due_layout.addWidget(self.estimated_time_group_box)
        self.estimated_time_start_due_layout.addWidget(self.start_date_group_box)
        self.estimated_time_start_due_layout.addWidget(self.due_date_group_box)

        # add the estimated time, start date, and due date container to the vertical layout
        self.verticalLayout.addLayout(self.estimated_time_start_due_layout)

        # add ability to add a task, milestone or deliverable to the task
        # each of which will be a separate form that will be added to the task
        self.task_subtask_button = QPushButton('Add SubTask', self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.task_subtask_button)
        # set a max width for the button
        self.task_subtask_button.setMaximumWidth(200)
        self.task_subtask_button.clicked.connect(self.add_subtask)

        # add a table to the form that will show the subtasks
        self.subtask_table = QTableWidget(self.scrollAreaWidgetContents)
        self.subtask_table.setColumnCount(2)
        self.subtask_table.setHorizontalHeaderLabels(['Name', 'Due Date'])
        self.subtasks = []

        # add the table to the form's layout
        self.verticalLayout.addWidget(self.subtask_table)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.layout.addWidget(self.scrollArea)

        self.ok_button = QPushButton("OK", self)
        self.layout.addWidget(self.ok_button)
        self.layout.addWidget(self.ok_button, alignment=Qt.AlignmentFlag.AlignRight)

        self.ok_button.clicked.connect(self.emit_task_info)

        self.setLayout(self.layout)  # Set layout on the dialog

        screen = QApplication.primaryScreen().availableGeometry()
        self.setGeometry(0, 0, int(screen.width() * 0.5), int(screen.height() * 0.8)) # 80% of screen size


        self.setWindowTitle('New Task')

        self.setModal(True)

    def calulate_estimated_time(self):
        units = self.task_estimated_time_combo_box.currentText()
        if units == 'Minutes':
            return self.task_estimated_time_spin_box.value() * 60
        elif units == 'Hours':
            return self.task_estimated_time_spin_box.value() * 60 * 60
        elif units == 'Days':
            return self.task_estimated_time_spin_box.value() * 60 * 60 * 24
        elif units == 'Weeks':
            return self.task_estimated_time_spin_box.value() * 60 * 60 * 24 * 7
        elif units == 'Months':
            return self.task_estimated_time_spin_box.value() * 60 * 60 * 24 * 30
        elif units == 'Years':
            return self.task_estimated_time_spin_box.value() * 60 * 60 * 24 * 365
        else:
            return 0
        
    def show_completer(self):
        self.sender().completer().complete()

    def update_options(self, line_edit, options):
        text = line_edit.text()
        if text not in options:
            options.append(text)
            line_edit.setCompleter(QCompleter(options))


    def emit_task_info(self):
        # Retrieve the data entered by the user, e.g.
        task_title = self.task_title_line_edit.text()
        task_description = self.task_description_text_edit.toPlainText()
        task_status = self.status_line_edit.text()
        task_priority = self.task_priority_combo_box.currentText()
        task_category = self.task_category_line_edit.text()
        task_goal_verb = self.task_goal_verb_line_edit.text()
        task_genre = self.task_genre_line_edit.text()
        task_use_case = self.task_use_case_line_edit.text()
        task_estimated_time_checkbox = self.no_estimated_time_checkbox.isChecked()
        task_estimated_time = self.calulate_estimated_time()
        task_start_date_checkbox = self.no_start_date_checkbox.isChecked()
        task_start_date = self.task_start_date_edit.text()
        task_due_date_checkbox = self.no_due_date_checkbox.isChecked()
        task_due_date = self.task_due_date_edit.text()
        task_subtasks = self.subtasks

        # Emit the data
        self.task_info_emitted.emit(task_title, task_description, task_status, task_priority, task_category, task_goal_verb, task_genre, task_use_case, task_estimated_time_checkbox, task_estimated_time, task_start_date_checkbox, task_start_date, task_due_date_checkbox, task_due_date, task_subtasks)

        # close the dialog
        self.close()


    def dueDateCheckboxChanged(self):
        if self.no_due_date_checkbox.isChecked():
            self.task_due_date_edit.setEnabled(False)
            self.task_due_date_button.setEnabled(False)
        else:
            self.task_due_date_edit.setEnabled(True)
            self.task_due_date_button.setEnabled(True)

    def startDateCheckboxChanged(self):
        if self.no_start_date_checkbox.isChecked():
            self.task_start_date_edit.setEnabled(False)
            self.task_start_date_button.setEnabled(False)
        else:
            self.task_start_date_edit.setEnabled(True)
            self.task_start_date_button.setEnabled(True)

    def estimatedTimeCheckboxChanged(self):
        if self.no_estimated_time_checkbox.isChecked():
            self.task_estimated_time_spin_box.setEnabled(False)
            self.task_estimated_time_combo_box.setEnabled(False)
        else:
            self.task_estimated_time_spin_box.setEnabled(True)
            self.task_estimated_time_combo_box.setEnabled(True)

    def center_on_screen(self):
        '''Centers the window on the screen.'''
        resolution = QApplication.primaryScreen().availableGeometry()
        self.move((resolution.width() / 2) - (self.frameGeometry().width() / 2),
                  (resolution.height() / 2) - (self.frameGeometry().height() / 2))
        
    def show_calendar_start_date(self):
        self.datetime_dialog = DateTimeDialog()
        self.datetime_dialog.date_selected.connect(self.update_start_date)
        self.datetime_dialog.exec()

    def show_calendar_due_date(self):
        self.datetime_dialog = DateTimeDialog()
        self.datetime_dialog.date_selected.connect(self.update_due_date)
        self.datetime_dialog.exec()

    def update_start_date(self, datetime):
        self.task_start_date_edit.setDateTime(datetime)

    def update_due_date(self, datetime):
        self.task_due_date_edit.setDateTime(datetime)

    def add_subtask(self):
        self.subtask_form = NewSubTaskForm()
        self.subtask_form.subtask_info_emitted.connect(self.add_subtask_to_table)
        self.subtask_form.exec()

    def add_subtask_to_table(self, subtask_title, subtask_priority, subtask_status, subtask_category, subtask_goal_verb, subtask_genre, subtask_use_case, no_due_date, subtask_due_date):
        subtask = SubTask(title=subtask_title, priority=subtask_priority, status=subtask_status, category=subtask_category, genre=subtask_genre, goal_verb=subtask_goal_verb, use_case=subtask_use_case, no_due_date=no_due_date, due_date=subtask_due_date)
        self.subtasks.append(subtask)
        row = self.subtask_table.rowCount()
        self.subtask_table.insertRow(row)
        self.subtask_table.setItem(row, 0, QTableWidgetItem(subtask_title))
        self.subtask_table.setItem(row, 1, QTableWidgetItem(subtask_due_date))

        # make sure the table is shown
        self.subtask_table.show()

    def clear_fields(self):
        self.task_title_line_edit.clear()
        self.status_line_edit.clear()
        self.task_start_date_edit.clear()
        self.task_due_date_edit.clear()
        self.task_estimated_time_spin_box.setValue(0)
        self.task_estimated_time_combo_box.setCurrentIndex(0)
        self.task_description_text_edit.clear()
        self.subtask_table.clear()
        self.subtasks = []
        self.no_due_date_checkbox.setChecked(False)
        self.no_start_date_checkbox.setChecked(False)
        self.no_estimated_time_checkbox.setChecked(False)
        self.subtask_table.clear()
        self.subtask_table.setRowCount(0)
        self.task_category_line_edit.clear()
        self.task_priority_combo_box.setCurrentIndex(0)
        self.task_goal_verb_line_edit.clear()
        self.task_genre_line_edit.clear()
        self.task_use_case_line_edit.clear()
        self.task_description_text_edit.clear()
        self.task_due_date_edit.clear()

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

        session.close()

        # return the options
        return category_options, goal_verb_options, genre_options, use_case_options, status_options, priority_options

class NewSubTaskForm(QtWidgets.QDialog):
    subtask_info_emitted = pyqtSignal(str, str, str, str, str, str, str, bool, str)
    def __init__(self, parent=None):
        super(NewSubTaskForm, self).__init__()

        self.layout = QtWidgets.QVBoxLayout(self)

        self.category_options, self.goal_verb_options, self.genre_options, self.use_case_options, self.status_options, self.priority_options = self.get_user_settings()

        self.scrollArea = QtWidgets.QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 380, 247))

        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.scrollAreaWidgetContents.setLayout(self.verticalLayout)  

        # add a title for the dialog box
        self.title_label = QLabel('New SubTask', self.scrollAreaWidgetContents)
        self.title_label.setStyleSheet('border: none; width: auto; height: auto;')
        self.title_label.setFont(QFont('Arial', 20))
        self.verticalLayout.addWidget(self.title_label)

        # add a label and line edit for the task name
        self.title_group_box = QGroupBox('SubTask Title', self.scrollAreaWidgetContents)
        self.title_layout = QVBoxLayout(self.title_group_box)
        self.subtask_title_line_edit = QLineEdit(self.title_group_box)
        self.title_layout.addWidget(self.subtask_title_line_edit)
        self.verticalLayout.addWidget(self.title_group_box)


        # add a label and combo box for the task status and priority and put them in a horizontal layout
        self.status_priority_container = QGroupBox('SubTask Status and Priority', self.scrollAreaWidgetContents)
        # create a vertical layout for priority label and priority combo box
        self.priority_container = QVBoxLayout()
        self.subtask_priority_label = QLabel('SubTask Priority')
        self.subtask_priority_combo_box = QComboBox()
        self.subtask_priority_combo_box.addItems(self.priority_options)
        self.subtask_priority_combo_box.setCurrentIndex(-1)
        self.priority_container.addWidget(self.subtask_priority_label)
        self.priority_container.addWidget(self.subtask_priority_combo_box)
        
        # create a vertical layout for status label and status combo box
        self.status_container = QVBoxLayout()
        self.subtask_status_label = QLabel('SubTask Status')
        self.status_line_edit = MyLineEdit()
        self.status_line_edit.setCompleter(QCompleter(self.status_options))
        self.status_line_edit.focused.connect(self.show_completer)
        self.status_line_edit.editingFinished.connect(lambda: self.update_options(self.status_line_edit, self.status_options))
        self.status_container.addWidget(self.subtask_status_label)
        self.status_container.addWidget(self.status_line_edit)

        # add the status and priority layouts to the horizontal layout
        self.status_priority_layout = QHBoxLayout(self.status_priority_container)
        self.status_priority_layout.addLayout(self.priority_container)
        self.status_priority_layout.addLayout(self.status_container)

        # add the status and priority container to the vertical layout
        self.verticalLayout.addWidget(self.status_priority_container)


        # create a group box for the subtask descriptors
        self.descriptors_container = QGroupBox('SubTask Descriptors', self.scrollAreaWidgetContents)

        # create a grid layout for the subtask descriptors
        self.descriptors_layout = QGridLayout(self.descriptors_container)

        # create a vertical layout for the task category label and combo box
        self.subtask_category_container = QVBoxLayout()
        self.subtask_category_label = QLabel('Task Category')
        self.subtask_category_line_edit = MyLineEdit()
        self.subtask_category_line_edit.setCompleter(QCompleter(self.category_options))
        self.subtask_category_line_edit.focused.connect(self.show_completer)
        self.subtask_category_line_edit.editingFinished.connect(lambda: self.update_options(self.subtask_category_line_edit, self.category_options))
        self.subtask_category_container.addWidget(self.subtask_category_label)
        self.subtask_category_container.addWidget(self.subtask_category_line_edit)

        # SubTask Goal Verb
        self.subtask_goal_verb_container = QVBoxLayout()
        self.subtask_goal_verb_label = QLabel('SubTask Goal Verb')
        self.subtask_goal_verb_line_edit = MyLineEdit()
        self.subtask_goal_verb_line_edit.setCompleter(QCompleter(self.goal_verb_options))
        self.subtask_goal_verb_line_edit.focused.connect(self.show_completer)
        self.subtask_goal_verb_line_edit.editingFinished.connect(lambda: self.update_options(self.subtask_goal_verb_line_edit, self.goal_verb_options))
        self.subtask_goal_verb_container.addWidget(self.subtask_goal_verb_label)
        self.subtask_goal_verb_container.addWidget(self.subtask_goal_verb_line_edit)

        # SubTask Genre
        self.subtask_genre_container = QVBoxLayout()
        self.subtask_genre_label = QLabel('SubTask Genre')
        self.subtask_genre_line_edit = MyLineEdit()
        self.subtask_genre_line_edit.setCompleter(QCompleter(self.genre_options))
        self.subtask_genre_line_edit.focused.connect(self.show_completer)
        self.subtask_genre_line_edit.editingFinished.connect(lambda: self.update_options(self.subtask_genre_line_edit, self.genre_options))
        self.subtask_genre_container.addWidget(self.subtask_genre_label)
        self.subtask_genre_container.addWidget(self.subtask_genre_line_edit)

        # SubTask Use Case
        self.subtask_use_case_container = QVBoxLayout()
        self.subtask_use_case_label = QLabel('SubTask Use Case')
        self.subtask_use_case_line_edit = MyLineEdit()
        self.subtask_use_case_line_edit.setCompleter(QCompleter(self.use_case_options))
        self.subtask_use_case_line_edit.focused.connect(self.show_completer)
        self.subtask_use_case_line_edit.editingFinished.connect(lambda: self.update_options(self.subtask_use_case_line_edit, self.use_case_options))
        self.subtask_use_case_container.addWidget(self.subtask_use_case_label)
        self.subtask_use_case_container.addWidget(self.subtask_use_case_line_edit)

        # add the subtask category, goal verb, genre and use case layouts to the grid layout
        self.descriptors_layout.addLayout(self.subtask_category_container, 0, 0)
        self.descriptors_layout.addLayout(self.subtask_goal_verb_container, 0, 1)
        self.descriptors_layout.addLayout(self.subtask_genre_container, 1, 0)
        self.descriptors_layout.addLayout(self.subtask_use_case_container, 1, 1)

        # add the descriptors container to the vertical layout
        self.verticalLayout.addWidget(self.descriptors_container)


        # create a horizontal layout for the estimated time, start date, and due date
        self.estimated_time_start_due_layout = QHBoxLayout(self.scrollAreaWidgetContents)

        # Due Date
        self.due_date_group_box = QGroupBox('Due Date', self)
        self.due_date_layout = QVBoxLayout(self.due_date_group_box)
        self.no_due_date_checkbox = QCheckBox('No due date', self.due_date_group_box)
        self.no_due_date_checkbox.setChecked(False)
        self.no_due_date_checkbox.stateChanged.connect(self.dueDateCheckboxChanged)
        self.subtask_due_date_button = QPushButton('Select Date', self)
        self.subtask_due_date_button.clicked.connect(self.show_calendar_due_date)
        self.subtask_due_date_edit = QDateTimeEdit(self.due_date_group_box)
        self.due_date_layout.addWidget(self.no_due_date_checkbox)
        self.due_date_layout.addWidget(self.subtask_due_date_edit)
        self.due_date_layout.addWidget(self.subtask_due_date_button)

        # due date layouts to the horizontal layout
        self.estimated_time_start_due_layout.addWidget(self.due_date_group_box)

        # add due date container to the vertical layout
        self.verticalLayout.addLayout(self.estimated_time_start_due_layout)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.layout.addWidget(self.scrollArea)


        self.ok_button = QPushButton("OK", self)
        self.layout.addWidget(self.ok_button, alignment=Qt.AlignmentFlag.AlignRight)
        self.ok_button.setMaximumWidth(200)


        self.ok_button.clicked.connect(self.emit_subtask_info)

        self.setLayout(self.layout)  # Set layout on the dialog


        screen = QApplication.primaryScreen().availableGeometry()
        self.setGeometry(100, 0, int(screen.width() * 0.25), int(screen.height() * 0.5)) # 80% of screen size

        self.setWindowTitle('New SubTask')

        self.setModal(True)

    def show_completer(self):
        self.sender().completer().complete()

    def update_options(self, line_edit, options):
        text = line_edit.text()
        if text not in options:
            options.append(text)
            line_edit.setCompleter(QCompleter(options))




    def dueDateCheckboxChanged(self):
        if self.no_due_date_checkbox.isChecked():
            self.subtask_due_date_edit.setEnabled(False)
            self.subtask_due_date_button.setEnabled(False)
        else:
            self.subtask_due_date_edit.setEnabled(True)
            self.subtask_due_date_button.setEnabled(True)


    def center_on_screen(self):
        '''Centers the window on the screen.'''
        resolution = QApplication.primaryScreen().availableGeometry()
        self.move((resolution.width() / 2) - (self.frameGeometry().width() / 2),
                  (resolution.height() / 2) - (self.frameGeometry().height() / 2))
        

    def show_calendar_due_date(self):
        self.datetime_dialog = DateTimeDialog()
        self.datetime_dialog.date_selected.connect(self.update_due_date)
        self.datetime_dialog.exec()


    def update_due_date(self, datetime):
        self.subtask_due_date_edit.setDateTime(datetime)

    def prepare_and_emit_subtask_info(self):
        subtask_title = self.subtask_title_line_edit.text()
        subtask_priority = self.subtask_priority_combo_box.currentText()
        subtask_status = self.status_line_edit.text()
        subtask_category = self.subtask_category_line_edit.text()
        subtask_goal_verb = self.subtask_goal_verb_line_edit.text()
        subtask_genre = self.subtask_genre_line_edit.text()
        subtask_use_case = self.subtask_use_case_line_edit.text()
        no_due_date = self.no_due_date_checkbox.isChecked()
        subtask_due_date = self.subtask_due_date_edit.text()

        # Emit the data
        self.subtask_info_emitted.emit(subtask_title, subtask_priority, subtask_status, subtask_category, 
            subtask_goal_verb, subtask_genre, subtask_use_case, no_due_date, subtask_due_date)
    

    def emit_subtask_info(self):
        self.prepare_and_emit_subtask_info()
        self.close()

    def accept(self):
        self.prepare_and_emit_subtask_info()
        super().accept()

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

        session.close()

        # return the options
        return category_options, goal_verb_options, genre_options, use_case_options, status_options, priority_options


class NewDeliverableForm(QtWidgets.QDialog, QObject):
    deliverable_info_emitted = pyqtSignal(str, str, str, str, str, str, str, str, str, str, str, bool, str)

    def __init__(self, parent=None):
        super(NewDeliverableForm, self).__init__()

        self.layout = QtWidgets.QVBoxLayout(self)

        self.category_options, self.goal_verb_options, self.genre_options, self.use_case_options, self.status_options, self.priority_options = self.get_user_settings()

        self.scrollArea = QtWidgets.QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 380, 247))

        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.scrollAreaWidgetContents.setLayout(self.verticalLayout)  

        # add a title for the dialog box
        self.title_label = QLabel('New Deliverable', self.scrollAreaWidgetContents)
        self.title_label.setStyleSheet('border: none; width: auto; height: auto;')
        self.title_label.setFont(QFont('Arial', 20))
        self.verticalLayout.addWidget(self.title_label)

        # add a label and line edit for the deliverable name
        self.title_group_box = QGroupBox('Deliverable Title', self.scrollAreaWidgetContents)
        self.title_layout = QVBoxLayout(self.title_group_box)
        self.deliverable_title_line_edit = QLineEdit(self.title_group_box)
        self.title_layout.addWidget(self.deliverable_title_line_edit)
        self.verticalLayout.addWidget(self.title_group_box)

        # add a label and text edit for the deliverable description
        self.description_group_box = QGroupBox('Deliverable Description', self.scrollAreaWidgetContents)
        self.description_layout = QVBoxLayout(self.description_group_box)
        self.deliverable_description_text_edit = QTextEdit(self.description_group_box)
        self.description_layout.addWidget(self.deliverable_description_text_edit)
        self.verticalLayout.addWidget(self.description_group_box)




        # add a label and combo box for the deliverable status and priority and put them in a horizontal layout
        self.status_priority_container = QGroupBox('Deliverable Status and Priority', self.scrollAreaWidgetContents)

        # create a vertical layout for priority label and priority combo box
        self.priority_container = QVBoxLayout()
        self.deliverable_priority_label = QLabel('Deliverable Priority')
        self.deliverable_priority_combo_box = QComboBox()
        self.deliverable_priority_combo_box.addItems(self.priority_options)
        self.deliverable_priority_combo_box.setCurrentIndex(-1)
        self.priority_container.addWidget(self.deliverable_priority_label)
        self.priority_container.addWidget(self.deliverable_priority_combo_box)
        
        # create a vertical layout for status label and status combo box
        self.status_container = QVBoxLayout()
        self.deliverable_status_label = QLabel('Deliverable Status')
        self.status_line_edit = MyLineEdit()
        self.status_line_edit.setCompleter(QCompleter(self.status_options))
        self.status_line_edit.focused.connect(self.show_completer)
        self.status_line_edit.editingFinished.connect(lambda: self.update_options(self.status_line_edit, self.status_options))
        self.status_container.addWidget(self.deliverable_status_label)
        self.status_container.addWidget(self.status_line_edit)



        # add the status and priority layouts to the horizontal layout
        self.status_priority_layout = QHBoxLayout(self.status_priority_container)
        self.status_priority_layout.addLayout(self.priority_container)
        self.status_priority_layout.addLayout(self.status_container)

        # add the status and priority container to the vertical layout
        self.verticalLayout.addWidget(self.status_priority_container)

        # add a label and text box for Deliverable Dependencies
        self.dependencies_group_box = QGroupBox('Deliverable Dependencies', self.scrollAreaWidgetContents)
        self.dependencies_layout = QVBoxLayout(self.dependencies_group_box)
        self.deliverable_dependencies_text_edit = QTextEdit(self.dependencies_group_box)
        self.dependencies_layout.addWidget(self.deliverable_dependencies_text_edit)
        self.verticalLayout.addWidget(self.dependencies_group_box)

        # add a label and text box for Deliverable Quality Criteria
        self.quality_criteria_group_box = QGroupBox('Deliverable Quality Criteria', self.scrollAreaWidgetContents)
        self.quality_criteria_layout = QVBoxLayout(self.quality_criteria_group_box)
        self.deliverable_quality_criteria_text_edit = QTextEdit(self.quality_criteria_group_box)
        self.quality_criteria_layout.addWidget(self.deliverable_quality_criteria_text_edit)
        self.verticalLayout.addWidget(self.quality_criteria_group_box)

        # add a label and text box for Deliverable Acceptance Criteria
        self.acceptance_criteria_group_box = QGroupBox('Deliverable Acceptance Criteria', self.scrollAreaWidgetContents)
        self.acceptance_criteria_layout = QVBoxLayout(self.acceptance_criteria_group_box)
        self.deliverable_acceptance_criteria_text_edit = QTextEdit(self.acceptance_criteria_group_box)
        self.acceptance_criteria_layout.addWidget(self.deliverable_acceptance_criteria_text_edit)
        self.verticalLayout.addWidget(self.acceptance_criteria_group_box)



        # create a group box for the deliverable descriptors
        self.descriptors_container = QGroupBox('Deliverable Descriptors', self.scrollAreaWidgetContents)

        # create a grid layout for the deliverable descriptors
        self.descriptors_layout = QGridLayout(self.descriptors_container)

        # create a vertical layout for the deliverable category label and combo box
        self.deliverable_category_container = QVBoxLayout()
        self.deliverable_category_label = QLabel('Deliverable Category')
        self.deliverable_category_line_edit = MyLineEdit()
        self.deliverable_category_line_edit.setCompleter(QCompleter(self.category_options))
        self.deliverable_category_line_edit.focused.connect(self.show_completer)
        self.deliverable_category_line_edit.editingFinished.connect(lambda: self.update_options(self.deliverable_category_line_edit, self.category_options))
        self.deliverable_category_container.addWidget(self.deliverable_category_label)
        self.deliverable_category_container.addWidget(self.deliverable_category_line_edit)

        # Deliverable Goal Verb
        self.deliverable_goal_verb_container = QVBoxLayout()
        self.deliverable_goal_verb_label = QLabel('Deliverable Goal Verb')
        self.deliverable_goal_verb_line_edit = MyLineEdit()
        self.deliverable_goal_verb_line_edit.setCompleter(QCompleter(self.goal_verb_options))
        self.deliverable_goal_verb_line_edit.focused.connect(self.show_completer)
        self.deliverable_goal_verb_line_edit.editingFinished.connect(lambda: self.update_options(self.deliverable_goal_verb_line_edit, self.goal_verb_options))
        self.deliverable_goal_verb_container.addWidget(self.deliverable_goal_verb_label)
        self.deliverable_goal_verb_container.addWidget(self.deliverable_goal_verb_line_edit)

        # Deliverable Genre
        self.deliverable_genre_container = QVBoxLayout()
        self.deliverable_genre_label = QLabel('Deliverable Genre')
        self.deliverable_genre_line_edit = MyLineEdit()
        self.deliverable_genre_line_edit.setCompleter(QCompleter(self.genre_options))
        self.deliverable_genre_line_edit.focused.connect(self.show_completer)
        self.deliverable_genre_line_edit.editingFinished.connect(lambda: self.update_options(self.deliverable_genre_line_edit, self.genre_options))
        self.deliverable_genre_container.addWidget(self.deliverable_genre_label)
        self.deliverable_genre_container.addWidget(self.deliverable_genre_line_edit)

        # Deliverable Use Case
        self.deliverable_use_case_container = QVBoxLayout()
        self.deliverable_use_case_label = QLabel('Deliverable Use Case')
        self.deliverable_use_case_line_edit = MyLineEdit()
        self.deliverable_use_case_line_edit.setCompleter(QCompleter(self.use_case_options))
        self.deliverable_use_case_line_edit.focused.connect(self.show_completer)
        self.deliverable_use_case_line_edit.editingFinished.connect(lambda: self.update_options(self.deliverable_use_case_line_edit, self.use_case_options))
        self.deliverable_use_case_container.addWidget(self.deliverable_use_case_label)
        self.deliverable_use_case_container.addWidget(self.deliverable_use_case_line_edit)


        # add the deliverable category, goal verb, genre and use case layouts to the grid layout
        self.descriptors_layout.addLayout(self.deliverable_category_container, 0, 0)
        self.descriptors_layout.addLayout(self.deliverable_goal_verb_container, 0, 1)
        self.descriptors_layout.addLayout(self.deliverable_genre_container, 1, 0)
        self.descriptors_layout.addLayout(self.deliverable_use_case_container, 1, 1)

        # add the descriptors container to the vertical layout
        self.verticalLayout.addWidget(self.descriptors_container)

        # Due Date
        self.due_date_group_box = QGroupBox('Due Date', self)
        self.due_date_layout = QVBoxLayout(self.due_date_group_box)
        self.no_due_date_checkbox = QCheckBox('No due date', self.due_date_group_box)
        self.no_due_date_checkbox.setChecked(False)
        self.no_due_date_checkbox.stateChanged.connect(self.dueDateCheckboxChanged)
        self.deliverable_due_date_button = QPushButton('Select Date', self)
        self.deliverable_due_date_button.clicked.connect(self.show_calendar_due_date)
        self.deliverable_due_date_edit = QDateTimeEdit(self.due_date_group_box)
        self.due_date_layout.addWidget(self.no_due_date_checkbox)
        self.due_date_layout.addWidget(self.deliverable_due_date_edit)
        self.due_date_layout.addWidget(self.deliverable_due_date_button)


        # add the estimated time, start date, and due date container to the vertical layout
        self.verticalLayout.addLayout(self.due_date_layout)


        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.layout.addWidget(self.scrollArea)

        self.ok_button = QPushButton("OK", self)
        self.layout.addWidget(self.ok_button)
        self.layout.addWidget(self.ok_button, alignment=Qt.AlignmentFlag.AlignRight)

        self.ok_button.clicked.connect(self.emit_deliverable_info)

        self.setLayout(self.layout)  # Set layout on the dialog

        screen = QApplication.primaryScreen().availableGeometry()
        self.setGeometry(0, 0, int(screen.width() * 0.5), int(screen.height() * 0.8)) # 80% of screen size


        self.setWindowTitle('New Deliverable')

        self.setModal(True)

        
    def show_completer(self):
        self.sender().completer().complete()

    def update_options(self, line_edit, options):
        text = line_edit.text()
        if text not in options:
            options.append(text)
            line_edit.setCompleter(QCompleter(options))


    def emit_deliverable_info(self):
        # Retrieve the data entered by the user, e.g.
        deliverable_title = self.deliverable_title_line_edit.text()
        deliverable_description = self.deliverable_description_text_edit.toPlainText()
        deliverable_status = self.status_line_edit.text()
        deliverable_priority = self.deliverable_priority_combo_box.currentText()
        deliverable_dependencies = self.deliverable_dependencies_text_edit.toPlainText()
        deliverable_quality_criteria = self.deliverable_quality_criteria_text_edit.toPlainText()
        deliverable_acceptance_criteria = self.deliverable_acceptance_criteria_text_edit.toPlainText()
        deliverable_category = self.deliverable_category_line_edit.text()
        deliverable_goal_verb = self.deliverable_goal_verb_line_edit.text()
        deliverable_genre = self.deliverable_genre_line_edit.text()
        deliverable_use_case = self.deliverable_use_case_line_edit.text()
        deliverable_due_date_checkbox = self.no_due_date_checkbox.isChecked()
        deliverable_due_date = self.deliverable_due_date_edit.text()


        # Emit the data
        self.deliverable_info_emitted.emit(deliverable_title, deliverable_description, deliverable_status, deliverable_priority, deliverable_dependencies, deliverable_quality_criteria, deliverable_acceptance_criteria,deliverable_category, deliverable_goal_verb, deliverable_genre, deliverable_use_case, deliverable_due_date_checkbox, deliverable_due_date)

        # close the dialog
        self.close()


    def dueDateCheckboxChanged(self):
        if self.no_due_date_checkbox.isChecked():
            self.deliverable_due_date_edit.setEnabled(False)
            self.deliverable_due_date_button.setEnabled(False)
        else:
            self.deliverable_due_date_edit.setEnabled(True)
            self.deliverable_due_date_button.setEnabled(True)


    def center_on_screen(self):
        '''Centers the window on the screen.'''
        resolution = QApplication.primaryScreen().availableGeometry()
        self.move((resolution.width() / 2) - (self.frameGeometry().width() / 2),
                  (resolution.height() / 2) - (self.frameGeometry().height() / 2))
        
    def show_calendar_start_date(self):
        self.datetime_dialog = DateTimeDialog()
        self.datetime_dialog.date_selected.connect(self.update_start_date)
        self.datetime_dialog.exec()

    def show_calendar_due_date(self):
        self.datetime_dialog = DateTimeDialog()
        self.datetime_dialog.date_selected.connect(self.update_due_date)
        self.datetime_dialog.exec()


    def update_due_date(self, datetime):
        self.deliverable_due_date_edit.setDateTime(datetime)



    def clear_fields(self):
        self.deliverable_title_line_edit.clear()
        self.status_line_edit.clear()
        self.deliverable_due_date_edit.clear()
        self.deliverable_description_text_edit.clear()
        self.no_due_date_checkbox.setChecked(False)
        self.deliverable_dependencies_text_edit.clear()
        self.deliverable_quality_criteria_text_edit.clear()
        self.deliverable_acceptance_criteria_text_edit.clear()
        self.deliverable_category_line_edit.clear()
        self.deliverable_priority_combo_box.setCurrentIndex(0)
        self.deliverable_goal_verb_line_edit.clear()
        self.deliverable_genre_line_edit.clear()
        self.deliverable_use_case_line_edit.clear()
        self.deliverable_description_text_edit.clear()
        self.deliverable_due_date_edit.clear()

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

        session.close()

        # return the options
        return category_options, goal_verb_options, genre_options, use_case_options, status_options, priority_options


class NewMilestoneForm(QtWidgets.QDialog, QObject):
    milestone_info_emitted = pyqtSignal(str, str, str, str, str, str, list)

    def __init__(self, project_tasks, project_deliverables, parent=None):
        super(NewMilestoneForm, self).__init__()

        self.layout = QtWidgets.QVBoxLayout(self)

        self.dependency_inputs = []



        self.project_tasks = project_tasks
        self.project_deliverables = project_deliverables

        self.db_manager = DatabaseManager('sqlite:///productivity_app/data/test.db')
        self.session = self.db_manager.session

        self.category_options, self.goal_verb_options, self.genre_options, self.use_case_options, self.status_options, self.priority_options = self.get_user_settings()

        self.scrollArea = QtWidgets.QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 380, 247))

        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.scrollAreaWidgetContents.setLayout(self.verticalLayout)  

        # add a title for the dialog box
        self.title_label = QLabel('New Milestone', self.scrollAreaWidgetContents)
        self.title_label.setStyleSheet('border: none; width: auto; height: auto;')
        self.title_label.setFont(QFont('Arial', 20))
        self.verticalLayout.addWidget(self.title_label)

        # add a label and line edit for the milestone name
        self.title_group_box = QGroupBox('Milestone Title', self.scrollAreaWidgetContents)
        self.title_layout = QVBoxLayout(self.title_group_box)
        self.milestone_title_line_edit = QLineEdit(self.title_group_box)
        self.title_layout.addWidget(self.milestone_title_line_edit)
        self.verticalLayout.addWidget(self.title_group_box)

        # add a label and text edit for the milestone description
        self.description_group_box = QGroupBox('Milestone Description', self.scrollAreaWidgetContents)
        self.description_layout = QVBoxLayout(self.description_group_box)
        self.milestone_description_text_edit = QTextEdit(self.description_group_box)
        self.description_layout.addWidget(self.milestone_description_text_edit)
        self.verticalLayout.addWidget(self.description_group_box)

        # create a group box for the milestone descriptors
        self.descriptors_container = QGroupBox('Milestone Descriptors', self.scrollAreaWidgetContents)

        # create a grid layout for the milestone descriptors
        self.descriptors_layout = QGridLayout(self.descriptors_container)

        # create a vertical layout for the milestone category label and combo box
        self.milestone_category_container = QVBoxLayout()
        self.milestone_category_label = QLabel('Milestone Category')
        self.milestone_category_line_edit = MyLineEdit()
        self.milestone_category_line_edit.setCompleter(QCompleter(self.category_options))
        self.milestone_category_line_edit.focused.connect(self.show_completer)
        self.milestone_category_container.addWidget(self.milestone_category_label)
        self.milestone_category_container.addWidget(self.milestone_category_line_edit)

        # Milestone Goal Verb
        self.milestone_goal_verb_container = QVBoxLayout()
        self.milestone_goal_verb_label = QLabel('Milestone Goal Verb')
        self.milestone_goal_verb_line_edit = MyLineEdit()
        self.milestone_goal_verb_line_edit.setCompleter(QCompleter(self.goal_verb_options))
        self.milestone_goal_verb_line_edit.focused.connect(self.show_completer)
        self.milestone_goal_verb_container.addWidget(self.milestone_goal_verb_label)
        self.milestone_goal_verb_container.addWidget(self.milestone_goal_verb_line_edit)

        # Milestone Genre
        self.milestone_genre_container = QVBoxLayout()
        self.milestone_genre_label = QLabel('Milestone Genre')
        self.milestone_genre_line_edit = MyLineEdit()
        self.milestone_genre_line_edit.setCompleter(QCompleter(self.genre_options))
        self.milestone_genre_line_edit.focused.connect(self.show_completer)
        self.milestone_genre_container.addWidget(self.milestone_genre_label)
        self.milestone_genre_container.addWidget(self.milestone_genre_line_edit)

        # Milestone Use Case
        self.milestone_use_case_container = QVBoxLayout()
        self.milestone_use_case_label = QLabel('Milestone Use Case')
        self.milestone_use_case_line_edit = MyLineEdit()
        self.milestone_use_case_line_edit.setCompleter(QCompleter(self.use_case_options))
        self.milestone_use_case_line_edit.focused.connect(self.show_completer)
        self.milestone_use_case_container.addWidget(self.milestone_use_case_label)
        self.milestone_use_case_container.addWidget(self.milestone_use_case_line_edit)


        # add the milestone category, goal verb, genre and use case layouts to the grid layout
        self.descriptors_layout.addLayout(self.milestone_category_container, 0, 0)
        self.descriptors_layout.addLayout(self.milestone_goal_verb_container, 0, 1)
        self.descriptors_layout.addLayout(self.milestone_genre_container, 1, 0)
        self.descriptors_layout.addLayout(self.milestone_use_case_container, 1, 1)

        # add the descriptors container to the vertical layout
        self.verticalLayout.addWidget(self.descriptors_container)

        # query the session for all Projects, Tasks, and Delivereables
        self.projects = self.session.query(Project).all()
        self.tasks = self.session.query(Task).all()
        self.deliverables = self.session.query(Deliverable).all()

        # add self.project_tasks to the self.tasks list
        for task in self.project_tasks:
            self.tasks.append(task)

        # add self.project_deliverables to the self.deliverables list
        for deliverable in self.project_deliverables:
            self.deliverables.append(deliverable)

        # create a mapping for project titles and project ids from self.projects
        self.project_titles = {}
        for project in self.projects:
            self.project_titles[project.title] = project.id

        # create a mapping for task titles and task ids from self.tasks
        self.task_titles = {}
        for task in self.tasks:
            self.task_titles[task.title] = task.id

        # create a mapping for deliverable titles and deliverable ids from self.deliverables
        self.deliverable_titles = {}
        for deliverable in self.deliverables:
            self.deliverable_titles[deliverable.title] = deliverable.id

        self.dependencies_ids = {}

        for project in self.projects:
            self.dependencies_ids['Project - ' + project.title] = project.id

        for task in self.tasks:
            self.dependencies_ids['Task - ' + task.title] = task.id

        for deliverable in self.deliverables:
            self.dependencies_ids['Deliverable - ' + deliverable.title] = deliverable.id



        self.dependencies_options = []


        # add a label, combobox and MyLineEdit for milestone dependencies
        self.dependencies_group_box = QGroupBox('Milestone Dependencies', self.scrollAreaWidgetContents)
        self.dependencies_layout = QHBoxLayout(self.dependencies_group_box)
        # add a combo box conaining "Complete", "Start"
        self.dependency_goal_combo_box = QComboBox()
        self.dependency_goal_combo_box.addItems(['Complete', 'Start'])
        self.dependency_goal_combo_box.setCurrentIndex(0)
        self.dependencies_layout.addWidget(self.dependency_goal_combo_box)
        # add a combo box containing "Project", "Task", and "Deliverable"
        self.dependency_type_combo_box = QComboBox()
        self.dependency_type_combo_box.addItems(['All', 'Projects', 'Tasks', 'Deliverables'])
        self.dependency_type_combo_box.setCurrentIndex(0)
        self.dependency_type_combo_box.currentTextChanged.connect(self.update_dependency_options)
        self.dependencies_layout.addWidget(self.dependency_type_combo_box)
        # add a line edit for the milestone dependencies
        self.milestone_dependencies_line_edit = MyLineEdit()
        self.milestone_dependencies_line_edit.setCompleter(QCompleter(self.dependencies_options))
        self.update_dependency_options()  # Call the method to update the options
        self.milestone_dependencies_line_edit.focused.connect(self.show_completer)

        self.dependencies_layout.addWidget(self.milestone_dependencies_line_edit)
        self.verticalLayout.addWidget(self.dependencies_group_box)

        self.add_more_button = QPushButton('Add More')
        self.add_more_button.clicked.connect(self.add_more_dependencies)
        self.dependencies_layout.addWidget(self.add_more_button)


        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.layout.addWidget(self.scrollArea)

        self.ok_button = QPushButton("OK", self)
        self.layout.addWidget(self.ok_button)
        self.layout.addWidget(self.ok_button, alignment=Qt.AlignmentFlag.AlignRight)

        self.ok_button.clicked.connect(self.emit_milestone_info)

        self.setLayout(self.layout)  # Set layout on the dialog

        screen = QApplication.primaryScreen().availableGeometry()
        self.setGeometry(0, 0, int(screen.width() * 0.5), int(screen.height() * 0.8)) # 80% of screen size


        self.setWindowTitle('New Milestone')

        self.setModal(True)

        original_dependency_input = {
            'group_box': self.dependencies_group_box,
            'goal_combo_box': self.dependency_goal_combo_box,
            'type_combo_box': self.dependency_type_combo_box,
            'line_edit': self.milestone_dependencies_line_edit,
        }
        self.dependency_inputs.append(original_dependency_input)

    def update_dependency_options(self):
        self.dependencies_options = ['Project - ' + title for title in self.project_titles.keys()] \
                                + ['Task - ' + title for title in self.task_titles.keys()] \
                                + ['Deliverable - ' + title for title in self.deliverable_titles.keys()]

        if self.dependency_type_combo_box.currentText() == 'Projects':
            self.dependencies_options = ['Project - ' + title for title in self.project_titles.keys()]
        elif self.dependency_type_combo_box.currentText() == 'Tasks':
            self.dependencies_options = ['Task - ' + title for title in self.task_titles.keys()]
        elif self.dependency_type_combo_box.currentText() == 'Deliverables':
            self.dependencies_options = ['Deliverable - ' + title for title in self.deliverable_titles.keys()]
        else:
            # All titles
            self.dependencies_options = ['Project - ' + title for title in self.project_titles.keys()] \
                                    + ['Task - ' + title for title in self.task_titles.keys()] \
                                    + ['Deliverable - ' + title for title in self.deliverable_titles.keys()]

        self.milestone_dependencies_line_edit.completer().setModel(QStringListModel(self.dependencies_options))

        for input_widgets in self.dependency_inputs:
            line_edit = input_widgets['line_edit']
            line_edit.completer().setModel(QStringListModel(self.dependencies_options))

    def get_dependency_id(self, title):
        id = self.dependencies_ids.get(title)
        return id





    def add_more_dependencies(self):
        # create new dependency inputs
        new_dependency_group_box = QGroupBox('Milestone Dependencies', self.scrollAreaWidgetContents)
        new_dependency_layout = QHBoxLayout(new_dependency_group_box)

        new_dependency_goal_combo_box = QComboBox()
        new_dependency_goal_combo_box.addItems(['Complete', 'Start'])
        new_dependency_goal_combo_box.setCurrentIndex(0)
        new_dependency_layout.addWidget(new_dependency_goal_combo_box)

        new_dependency_type_combo_box = QComboBox()
        new_dependency_type_combo_box.addItems(['All', 'Projects', 'Tasks', 'Deliverables'])
        new_dependency_type_combo_box.setCurrentIndex(0)
        new_dependency_type_combo_box.currentTextChanged.connect(self.update_dependency_options)
        new_dependency_layout.addWidget(new_dependency_type_combo_box)

        new_milestone_dependencies_line_edit = MyLineEdit()
        new_milestone_dependencies_line_edit.setCompleter(QCompleter(self.dependencies_options))
        self.update_dependency_options()  # Call the method to update the options
        new_milestone_dependencies_line_edit.focused.connect(self.show_completer)

        new_dependency_layout.addWidget(new_milestone_dependencies_line_edit)
        
        # add a remove button
        remove_button = QPushButton("Remove")
        remove_button.clicked.connect(lambda: self.remove_dependency(new_dependency_group_box))
        new_dependency_layout.addWidget(remove_button)
            
        # add the new dependency inputs to the layout
        self.verticalLayout.addWidget(new_dependency_group_box)

        # store the new inputs in the list
        self.dependency_inputs.append({
            'group_box': new_dependency_group_box,
            'goal_combo_box': new_dependency_goal_combo_box,
            'type_combo_box': new_dependency_type_combo_box,
            'line_edit': new_milestone_dependencies_line_edit,
        })
    def remove_dependency(self, group_box):
        # Remove from layout
        self.verticalLayout.removeWidget(group_box)
        # Delete from memory
        group_box.deleteLater()

        # Remove from dependency inputs
        self.dependency_inputs = [input_widgets for input_widgets in self.dependency_inputs if input_widgets['group_box'] != group_box]


    def show_completer(self):
        self.sender().completer().complete()


    def emit_milestone_info(self):
        # Retrieve the data entered by the user, e.g.
        milestone_title = self.milestone_title_line_edit.text()
        milestone_description = self.milestone_description_text_edit.toPlainText()
        milestone_category = self.milestone_category_line_edit.text()
        milestone_goal_verb = self.milestone_goal_verb_line_edit.text()
        milestone_genre = self.milestone_genre_line_edit.text()
        milestone_use_case = self.milestone_use_case_line_edit.text()

        # Retrieve the data from line edits in the dependency inputs
        dependencies = []
        for input_widgets in self.dependency_inputs:
            line_edit = input_widgets['line_edit']
            text = line_edit.text()
            action = input_widgets['goal_combo_box']
            action_text = action.currentText()

            if text not in self.dependencies_options:
                print(f"User input {text} is not in the options!")

            # If the text is empty or doesn't exist in the options, show an error message
            if text == '' or text not in self.dependencies_options:
                QMessageBox.critical(self, "Error", f"'{text}' doesn't exist!")
                return
            else:
                id = self.get_dependency_id(text)  # Convert title to ID
                if id is not None:
                    dependencies.append(action_text + "-" + str(id))  # If the ID exists, add it to the list of dependencies

        # Emit the data
        self.milestone_info_emitted.emit(milestone_title, milestone_description, milestone_category, milestone_goal_verb, milestone_genre, milestone_use_case, dependencies)

        # Close the dialog
        self.close()




    def center_on_screen(self):
        '''Centers the window on the screen.'''
        resolution = QApplication.primaryScreen().availableGeometry()
        self.move((resolution.width() / 2) - (self.frameGeometry().width() / 2),
                  (resolution.height() / 2) - (self.frameGeometry().height() / 2))
    



    def clear_fields(self):
        self.milestone_title_line_edit.clear()
        self.milestone_description_text_edit.clear()
        self.submilestones = []
        self.milestone_category_line_edit.clear()
        self.milestone_goal_verb_line_edit.clear()
        self.milestone_genre_line_edit.clear()
        self.milestone_use_case_line_edit.clear()
        self.milestone_description_text_edit.clear()

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

        session.close()

        # return the options
        return category_options, goal_verb_options, genre_options, use_case_options, status_options, priority_options

class NewToDoForm(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(NewToDoForm, self).__init__()

        self.layout = QtWidgets.QVBoxLayout(self)

        self.scrollArea = QtWidgets.QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 380, 247))

        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.scrollAreaWidgetContents.setLayout(self.verticalLayout) 

        # add a title for the dialog box
        self.title_label = QLabel('New To Do', self.scrollAreaWidgetContents)
        self.title_label.setStyleSheet('border: none; width: auto; height: auto;')
        self.title_label.setFont(QFont('Arial', 20))
        self.verticalLayout.addWidget(self.title_label)


        for i in range(50):
            self.lineEdit = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
            self.verticalLayout.addWidget(self.lineEdit)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.layout.addWidget(self.scrollArea)

        self.setLayout(self.layout)  # Set layout on the dialog
        self.setGeometry(500, 300, 400, 300)
        self.setWindowTitle('New To Do')