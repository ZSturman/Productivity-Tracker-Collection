import os
import json
import time
from datetime import datetime, timedelta
import csv
import pandas as pd
from sqlalchemy import or_, create_engine, inspect
from PyQt6.QtWidgets import QFrame, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QApplication, QLabel, QListWidget, QListWidgetItem, QScrollArea, QWidget, QComboBox, QLineEdit, QCheckBox, QGroupBox, QSpacerItem, QSizePolicy, QDialog, QDialogButtonBox, QTextEdit, QMenu, QStackedWidget, QSpinBox, QDateTimeEdit, QToolButton, QFileDialog, QLayout, QMessageBox, QTreeView, QTreeWidget, QTableView, QTreeWidgetItem
from PyQt6.QtCore import QTimer, Qt, QAbstractTableModel
from PyQt6 import uic, QtGui
from PyQt6.QtGui import QAction, QPalette, QColor, QStandardItemModel, QStandardItem
from games.reaction_time import ReactionTimeGameWidget



from database.database import DatabaseManager
from custom_widgets.custom_widgets import UpcomingListItem, KanbanListItem, NewTaskForm, NewDeliverableForm, NewMilestoneForm, NewSubTaskForm, NewToDoForm, MyTableModel
from custom_widgets.new_project_wizard import NewProjectWizard
from dialog_box.new_item import NewItemDialog
from models.models import Folder, Project, Task, Deliverable, Milestone, Note, Attachment, SubTask, ToDo
from data_collection.data_categories import data_categories
from user_settings.user_settings_db import UserSettings, create_user_settings_db, sessionmaker
from user_settings.user_defaults import folder_directory as default_folder_directory



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.current_layout = 'home'
        self.current_productivity_layout = None
        self.current_data_collection_layout = None
        self.sidebar_message = None

        self.category_options, self.goal_verb_options, self.genre_options, self.use_case_options, self.status_options, self.priority_options, self.group_by_options, self.folder_directory = self.get_user_settings()

        self.db_manager = DatabaseManager('sqlite:///productivity_app/data/test.db')

        # read data from test.db
        self.session = self.db_manager.session

        # Load the main UI
        self.main_ui = uic.loadUi('productivity_app/ui/main.ui', self)

        self.main_layout = self.main_ui.findChild(QVBoxLayout, 'verticalLayout')

        # toolbars
        self.main_toolbar = self.findChild(QFrame, 'mainToolBar')

        self.add_new_item = self.main_toolbar.findChild(QToolButton, 'addNewItem')
        self.add_new_item.clicked.connect(self.handle_add_new_item)
        
        self.productivity_toolbar = self.findChild(QFrame, 'productivityToolBar')
        self.productivity_toolbar.hide()

        self.data_collection_toolbar = self.findChild(QFrame, 'dataCollectionToolBar')
        self.data_collection_toolbar.hide()

        self.show()

        self.toolbar_buttons = {
            'home': self.main_toolbar.findChild(QToolButton, 'mainHomeBtn'),
            'dashboard': self.main_toolbar.findChild(QToolButton, 'mainDashboardBtn'),
            'productivity': self.main_toolbar.findChild(QToolButton, 'mainProductivityBtn'),
            'data_collection': self.main_toolbar.findChild(QToolButton, 'mainDataCollectionBtn'),
            'settings': self.main_toolbar.findChild(QToolButton, 'mainSettingsBtn'),
            'kanban': self.productivity_toolbar.findChild(QToolButton, 'productivityKanbanBtn'),
            'gannt': self.productivity_toolbar.findChild(QToolButton, 'productivityGanntBtn'),
            'calendar': self.productivity_toolbar.findChild(QToolButton, 'productivityCalendarBtn'),
            'table': self.productivity_toolbar.findChild(QToolButton, 'productivityTableBtn'),
            'directory_view': self.productivity_toolbar.findChild(QToolButton, 'productivityDirectoryViewBtn'),
            'overview': self.data_collection_toolbar.findChild(QToolButton, 'dataCollectionToolBarOverviewBtn'),
            'physical_health': self.data_collection_toolbar.findChild(QToolButton, 'dataCollectionToolBarPhysicalBtn'),
            'mental_health': self.data_collection_toolbar.findChild(QToolButton, 'dataCollectionToolBarMeantlBtn'),
            'financial': self.data_collection_toolbar.findChild(QToolButton, 'dataCollectionToolBarFinancialBtn'),
            'relationship': self.data_collection_toolbar.findChild(QToolButton, 'dataCollectionToolBarRelationshipsBtn'),
            'other': self.data_collection_toolbar.findChild(QToolButton, 'dataCollectionToolBarOtherBtn'),
            'collection_techniques': self.data_collection_toolbar.findChild(QToolButton, 'dataCollectionToolBarCollectionBtn'),
        }

        for layout_name, button in self.toolbar_buttons.items():
            button.clicked.connect(lambda checked, layout_name=layout_name: self.handle_button_click(layout_name))

        # Keeping track of the currently loaded UI
        self.current_ui = None

        # if no button is pressed then load the home UI
        self.load_home_tab_ui()


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




    def handle_add_new_item(self):
        dialog = NewProjectWizard()
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # check for dialog.project.folder_dir in session and create if not found
            folder = self.session.query(Folder).filter(Folder.folder_dir == dialog.project.folder_dir).first()
            if folder is None:
                # if dialog.project.folder_dir doesn't contain '/' then add the folder to self.folder_directory
                if '/' not in dialog.project.folder_dir:
                    dialog.project.folder_dir = self.folder_directory + "/" + dialog.project.folder_dir
                    folder_title = dialog.project.folder_dir.split('/')[-1]
                else:
                    folder_title = dialog.project.folder_dir.split('/')[-1]
                # if the folder exists in the os directory then create a duplicate folder with a number appended to the end
                if os.path.exists(dialog.project.folder_dir):
                    folder_title = folder_title + " 1"
                    dialog.project.folder_dir = dialog.project.folder_dir + " 1"
                    while os.path.exists(dialog.project.folder_dir):
                        folder_title = folder_title[:-1] + str(int(folder_title[-1]) + 1)
                        dialog.project.folder_dir = dialog.project.folder_dir[:-1] + str(int(dialog.project.folder_dir[-1]) + 1)
                # create folder
                folder = Folder(folder_dir=dialog.project.folder_dir, title=folder_title)
                self.session.add(folder)
                try:
                    self.session.commit()
                except Exception as e:
                    self.session.rollback()
                    raise e
            
            if dialog.project.priority == "" or dialog.project.priority == "None" or dialog.project.priority == "All Priorities":
                dialog.project.priority = None
            if dialog.project.status == "" or dialog.project.status == "None" or dialog.project.status == "All Statuses":
                dialog.project.status = None
            if dialog.project.category == "" or dialog.project.category == "None" or dialog.project.category == "All Categories":
                dialog.project.category = None
            if dialog.project.goal_verb == "" or dialog.project.goal_verb == "None" or dialog.project.goal_verb == "All Goal Verbs":
                dialog.project.goal_verb = None
            if dialog.project.genre == "" or dialog.project.genre == "None" or dialog.project.genre == "All Genres":
                dialog.project.genre = None
            if dialog.project.use_case == "" or dialog.project.use_case == "None" or dialog.project.use_case == "All Use Cases":
                dialog.project.use_case = None

            project = Project(identifying_type='project', 
                            completed=False, 
                            datetime_completed=None, 
                            actual_time_to_complete=None, 
                            folder_dir=dialog.project.folder_dir, 
                            title=dialog.project.title, 
                            priority=dialog.project.priority, 
                            description=dialog.project.description, 
                            category=dialog.project.category, 
                            goal_verb=dialog.project.goal_verb, 
                            genre=dialog.project.genre, 
                            use_case=dialog.project.use_case, 
                            status=dialog.project.status, 
                            folder_id=folder.id, 
                            estimated_time_to_complete_checkbox=dialog.project.estimated_time_to_complete_checkbox, 
                            estimated_time_to_complete=dialog.project.estimated_time_to_complete, 
                            no_start_date=dialog.project.no_start_date, 
                            no_due_date=dialog.project.no_due_date,
                            due_date=dialog.project.due_date,
                            start_date=dialog.project.start_date
                            )

            self.session.add(project)
            try:
                self.session.flush()
                self.session.commit()
            except Exception as e:
                self.session.rollback()
                raise e


            # create tasks
            for task in dialog.project.tasks:
                if task.estimated_time_to_complete is not None:
                    task.estimated_time_to_complete = timedelta(minutes=task.estimated_time_to_complete)
                if task.start_date is not None:
                    task.start_date = datetime.strptime(task.start_date, "%m/%d/%y %I:%M %p")
                if task.due_date is not None:
                    task.due_date = datetime.strptime(task.due_date, "%m/%d/%y %I:%M %p")

                if task.estimated_time_to_complete is not None:
                    # convert from datetime.timedelta to int 
                    task.estimated_time_to_complete = task.estimated_time_to_complete.total_seconds() / 60

                if task.priority == "" or task.priority == "None" or task.priority == "All Priorities":
                    task.priority = None
                if task.status == "" or task.status == "None" or task.status == "All Statuses":
                    task.status = None
                if task.category == "" or task.category == "None" or task.category == "All Categories":
                    task.category = None
                if task.goal_verb == "" or task.goal_verb == "None" or task.goal_verb == "All Goal Verbs":
                    task.goal_verb = None
                if task.genre == "" or task.genre == "None" or task.genre == "All Genres":
                    task.genre = None
                if task.use_case == "" or task.use_case == "None" or task.use_case == "All Use Cases":
                    task.use_case = None
                task = Task(folder_dir=dialog.project.folder_dir, title=task.title, project_id=project.id, description=task.description, category=task.category, goal_verb=task.goal_verb, genre=task.genre, use_case=task.use_case, status=task.status, priority=task.priority, no_start_date=task.no_start_date, start_date=task.start_date, estimated_time_to_complete_checkbox=task.estimated_time_to_complete_checkbox, estimated_time_to_complete=task.estimated_time_to_complete, no_due_date=task.no_due_date, due_date=task.due_date)
                self.session.add(task)
                try:
                    self.session.commit()
                except Exception as e:
                    self.session.rollback()
                    raise e

                for subtask in task.subtasks:
                    if subtask.priority == "" or subtask.priority == "None" or subtask.priority == "All Priorities":
                        subtask.priority = None
                    if subtask.status == "" or subtask.status == "None" or subtask.status == "All Statuses":
                        subtask.status = None
                    if subtask.category == "" or subtask.category == "None" or subtask.category == "All Categories":
                        subtask.category = None
                    if subtask.goal_verb == "" or subtask.goal_verb == "None" or subtask.goal_verb == "All Goal Verbs":
                        subtask.goal_verb = None
                    if subtask.genre == "" or subtask.genre == "None" or subtask.genre == "All Genres":
                        subtask.genre = None
                    if subtask.use_case == "" or subtask.use_case == "None" or subtask.use_case == "All Use Cases":
                        subtask.use_case = None
                    subtask = SubTask(folder_dir=dialog.project.folder_dir, title=subtask.title, task_id=task.id, priority=subtask.priority, status=subtask.status, no_due_date=subtask.no_due_date, due_date=subtask.due_date, category=subtask.category, goal_verb=subtask.goal_verb, genre=subtask.genre, use_case=subtask.use_case)
                    self.session.add(subtask)
                    try:
                        self.session.commit()
                    except Exception as e:
                        self.session.rollback()
                        raise e

            # load the dashboard
            self.handle_button_click('dashboard')


    def handle_button_click(self, layout_name):
        if self.current_layout == layout_name:
            return
        self.current_layout = layout_name
        if layout_name == 'home':
            self.load_home_tab_ui()
        elif layout_name == 'dashboard':
            self.load_dashboard_tab_ui()
        elif layout_name == 'productivity':
            self.productivity_toolbar.show()
            if self.current_productivity_layout is None:
                self.load_kanban_tab_ui()
            else:
                self.load_productivity_layout()
        elif layout_name == 'data_collection':
            self.data_collection_toolbar.show()
            if self.current_data_collection_layout is None:
                self.load_collection_techniques_tab_ui()
            else:
                self.load_data_collection_layout()
        elif layout_name == 'settings':
            self.load_settings_tab_ui()
        elif layout_name == 'kanban':
            self.load_kanban_tab_ui()
            self.current_productivity_layout = 'kanban'
        elif layout_name == 'gannt':
            self.load_gannt_tab_ui()
            self.current_productivity_layout = 'gannt'
        elif layout_name == 'calendar':
            self.load_calendar_tab_ui()
            self.current_productivity_layout = 'calendar'
        elif layout_name == 'table':
            self.load_table_tab_ui()
            self.current_productivity_layout = 'table'
        elif layout_name == 'directory_view':
            self.load_directory_view_tab_ui()
            self.current_productivity_layout = 'directory_view'
        elif layout_name == 'overview':
            self.load_overview_tab_ui()
            self.current_data_collection_layout = 'overview'
        elif layout_name == 'physical_health':
            self.load_physical_health_tab_ui()
            self.current_data_collection_layout = 'physical_health'
        elif layout_name == 'mental_health':
            self.load_mental_health_tab_ui()
            self.current_data_collection_layout = 'mental_health'
        elif layout_name == 'financial':
            self.load_financial_tab_ui()
            self.current_data_collection_layout = 'financial'
        elif layout_name == 'relationship':
            self.load_relationship_tab_ui()
            self.current_data_collection_layout = 'relationship'
        elif layout_name == 'other':
            self.load_other_tab_ui()
            self.current_data_collection_layout = 'other'
        elif layout_name == 'collection_techniques':
            self.load_collection_techniques_tab_ui()
            self.current_data_collection_layout = 'collection_techniques'

            

    def _remove_current_ui(self):
        if self.current_ui:
            # Remove the currently loaded UI from layout
            self.main_layout.removeWidget(self.current_ui)
            self.show_all_projects = None
            self.show_all_tasks = None
            self.show_all_deliverables = None
            self.show_all_milestones = None
            self.show_all_notes = None
            self.show_all_attachments = None
            self.show_all_sub_tasks = None
            self.show_all_to_dos = None
            self.current_ui.deleteLater()
            self.current_ui = None

    def _load_ui(self, ui_file):
        self.current_ui = uic.loadUi(ui_file)
        self.show_all_projects = self.current_ui.findChild(QCheckBox, 'show_all_projects')
        self.main_layout.addWidget(self.current_ui)

    def load_ui(self, ui_file):
        self._remove_current_ui()
        self._load_ui(ui_file)

    def load_home_tab_ui(self):
        self.productivity_toolbar.hide()
        self.data_collection_toolbar.hide()
        self.load_ui('productivity_app/ui/home_tab.ui')
        self.current_layout = 'home'




    def load_dashboard_tab_ui(self):
        try:
            self.productivity_toolbar.hide()
            self.data_collection_toolbar.hide()
            self.load_ui('productivity_app/ui/dashboard_ui.ui')
            self.current_layout = 'dashboard'


            self.sidebar_massage_area = self.current_ui.findChild(QLabel, 'sidebarMessage')
            if not self.sidebar_massage_area:
                raise Exception("Unable to find 'sidebarMessage' QLabel")

            self.add_new_item = self.main_ui.findChild(QPushButton, 'addNewItem')
            if not self.add_new_item:
                raise Exception("Unable to find 'addNewItem' QPushButton")
            self.add_new_item.clicked.connect(self.handle_add_new_todo)

            if self.sidebar_message:
                self.sidebar_massage_area.setText(self.sidebar_message.text())
                self.sidebar_massage_area.show()
                self.sidebar_message = None
            else:
                self.sidebar_massage_area.hide()

            self.refresh_todos()
            QTimer.singleShot(100, self.update_dashboard_widgets)
        except Exception as e:
            print(f"Error in load_dashboard_tab_ui: {e}")

    def update_dashboard_widgets(self):
        try:
            self.upcoming_items_incomplete, self.upcoming_items_complete = self.refresh_database()
            print("self.upcoming_items_incomplete", self.upcoming_items_incomplete)

            upcoming_sidebar = self.findChild(QFrame, 'upcomingSideBar')
            if not upcoming_sidebar:
                raise Exception("Unable to find 'upcomingSideBar' QFrame")

            upcoming_list = upcoming_sidebar.findChildren(QListWidget, 'upcomingList')
            if not upcoming_list:
                raise Exception("Unable to find 'upcomingList' QListWidget")
            
            # get all the todo items from the database
            self.upcoming_items = self.session.query(ToDo).all()
            # sort the todo items by date_modified
            self.upcoming_items.sort(key=lambda x: x.date_modified, reverse=True)
            # get the first 5 items
            self.upcoming_items = self.upcoming_items[:5]
            # clear the list
            upcoming_list[0].clear()
            # add the items to the list
            for item in self.upcoming_items:
                # add a checkbox and todo title
                checkbox = QCheckBox()
                checkbox.setChecked(item.complete)
                checkbox.setText(item.title)
                checkbox.stateChanged.connect(lambda state, item=item: self.handle_todo_complete(item, state))
                upcoming_list[0].addItem(checkbox)

            


        

        


        except Exception as e:
            print(f"Error in update_dashboard_widgets: {e}")


    def handle_todo_complete(self, item, state):
        item.complete = state
        self.session.commit()
        self.reload_dashboard_tab(item, state)


    def reload_dashboard_tab(self, item, status):
        # add a label to the sidebar for the item and it's status
        if status == True:
            status = 'Complete'
        else:
            status = 'Incomplete'
        self.sidebar_message = QLabel(f"{item.title} marked as {status}")

        QTimer.singleShot(100, self.load_dashboard_tab_ui)


    def fetch_upcoming_items(self):
        self.upcoming_items = self.session.query(Project).filter(or_(Project.start_date != None, Project.due_date != None)).all()
        self.upcoming_items += self.session.query(Task).filter(or_(Task.start_date != None, Task.due_date != None)).all()
        self.upcoming_items += self.session.query(SubTask).filter(or_(SubTask.due_date != None)).all()
        self.upcoming_items += self.session.query(Deliverable).filter(or_(Deliverable.due_date != None)).all()
        self.upcoming_items += self.session.query(ToDo).filter(or_(ToDo.due_date != None)).all()

    def sort_upcoming_items(self):
        def sorting_key(x):
            due_date = x.due_date if x.due_date is not None else datetime.min
            priority = x.priority if x.priority is not None else ''
            return (due_date, priority)

        self.upcoming_items_incomplete = sorted(
            [item for item in self.upcoming_items if not item.completed],
            key=sorting_key,
            reverse=True
        )
        self.upcoming_items_complete = sorted(
            [item for item in self.upcoming_items if item.completed],
            key=sorting_key,
            reverse=True
        )


    def refresh_database(self):
        self.fetch_upcoming_items()
        self.sort_upcoming_items()
        return self.upcoming_items_incomplete, self.upcoming_items_complete



    def load_productivity_layout(self):
        self.productivity_toolbar.show()
        self.data_collection_toolbar.hide()

        if self.current_productivity_layout == 'kanban':
            self.load_kanban_tab_ui()
        elif self.current_productivity_layout == 'gannt':
            self.load_gannt_tab_ui()
        elif self.current_productivity_layout == 'calendar':
            self.load_calendar_tab_ui()
        elif self.current_productivity_layout == 'table':
            self.load_table_tab_ui()
        elif self.current_productivity_layout == 'directory_view':
            self.load_directory_view_tab_ui()

    def handle_add_new_todo(self):
        self.sidebar_message = QLabel("Add new todo")
        print("Adding new to do")
        to_do_input = self.current_ui.findChild(QLineEdit, 'todoLineEdit')
        print(to_do_input.text())
        if to_do_input.text():
            new_todo = ToDo(
                title=to_do_input.text(),
                completed=False
            )
            self.session.add(new_todo)
            self.session.commit()
            self.reload_dashboard_tab(new_todo, False)





    def load_kanban_tab_ui(self):
        self.data_collection_toolbar.hide()
        self.current_productivity_layout = 'kanban'
        self.load_ui('productivity_app/ui/kanban_ui.ui')

        self.search_bar = self.findChild(QLineEdit, 'searchManual')

        # sort by toolbar
        self.sort_by_toolbar = self.findChild(QFrame, 'sortByOptions')

        # checkboxes
        self.show_all_projects = self.sort_by_toolbar.findChild(QCheckBox, 'showAllProjects')
        self.show_all_tasks = self.sort_by_toolbar.findChild(QCheckBox, 'showAllTasks')
        self.show_all_subtasks = self.sort_by_toolbar.findChild(QCheckBox, 'showAllSubTasks')
        self.show_all_deliverables = self.sort_by_toolbar.findChild(QCheckBox, 'showAllDeliverables')
        self.show_all_milestones = self.sort_by_toolbar.findChild(QCheckBox, 'showAllMilestones')
        self.show_all_todos = self.sort_by_toolbar.findChild(QCheckBox, 'showAllToDos')

        self.group_by_checkbox = self.sort_by_toolbar.findChild(QCheckBox, 'groupByCheckbox')
        self.group_by_option = self.sort_by_toolbar.findChild(QComboBox, 'groupByDropdown')
        self.group_by_option.addItems(self.group_by_options)
        
        self.descriptors_toolbar = self.findChild(QFrame, 'descriptorsOptions')
        self.categories_dropdown = self.descriptors_toolbar.findChild(QComboBox, 'categoriesDropdown')
        # add "All Categories" option the tops of category_options
        temp_category_options = self.category_options
        temp_category_options.insert(0, 'All Categories')
        self.categories_dropdown.addItems(temp_category_options)

        self.status_dropdown = self.descriptors_toolbar.findChild(QComboBox, 'statusDropdown')
        # add "All Statuses" option the tops of status_options
        temp_status_options = self.status_options
        temp_status_options.insert(0, 'All Statuses')
        self.status_dropdown.addItems(temp_status_options)

        self.goal_verb_dropdown = self.descriptors_toolbar.findChild(QComboBox, 'goalVerbDropdown')
        # add "All Goal Verbs" option the tops of goal_verb_options
        temp_goal_verb_options = self.goal_verb_options
        temp_goal_verb_options.insert(0, 'All Goal Verbs')
        self.goal_verb_dropdown.addItems(temp_goal_verb_options)

        self.use_case_dropdown = self.descriptors_toolbar.findChild(QComboBox, 'useCaseDropdown')
        # add "All Use Cases" option the tops of use_case_options
        temp_use_case_options = self.use_case_options
        temp_use_case_options.insert(0, 'All Use Cases')
        self.use_case_dropdown.addItems(temp_use_case_options)

        self.genre_dropdown = self.descriptors_toolbar.findChild(QComboBox, 'genreDropdown')
        # add "All Genres" option the tops of genre_options
        temp_genre_options = self.genre_options
        temp_genre_options.insert(0, 'All Genres')
        self.genre_dropdown.addItems(temp_genre_options)

        self.show_all_projects.stateChanged.connect(self.reload_kanban_tab)
        self.show_all_tasks.stateChanged.connect(self.reload_kanban_tab)
        self.show_all_subtasks.stateChanged.connect(self.reload_kanban_tab)
        self.show_all_deliverables.stateChanged.connect(self.reload_kanban_tab)
        self.show_all_milestones.stateChanged.connect(self.reload_kanban_tab)
        self.show_all_todos.stateChanged.connect(self.reload_kanban_tab)
        self.group_by_checkbox.stateChanged.connect(self.group_by_updated)

        self.group_by_option.currentIndexChanged.connect(self.reload_kanban_tab)
        self.categories_dropdown.currentIndexChanged.connect(self.reload_kanban_tab)
        self.status_dropdown.currentIndexChanged.connect(self.reload_kanban_tab)
        self.goal_verb_dropdown.currentIndexChanged.connect(self.reload_kanban_tab)
        self.use_case_dropdown.currentIndexChanged.connect(self.reload_kanban_tab)
        self.genre_dropdown.currentIndexChanged.connect(self.reload_kanban_tab)


        QTimer.singleShot(100, self.reload_kanban_tab)

        scroll_area = self.current_ui.findChild(QScrollArea, 'scrollArea')

        # Create a QWidget object to hold items and set it as the widget of the QScrollArea
        scroll_content = QWidget(scroll_area)
        scroll_area.setWidget(scroll_content)

        # Create a QVBoxLayout and set it as the layout of the scroll_content
        scroll_layout = QHBoxLayout(scroll_content)

        # This will make the scroll_content adjust its size according to the items in the scroll_layout
        scroll_content.setLayout(scroll_layout)
        scroll_area.setWidgetResizable(True)
    
    def group_by_updated(self):
        if self.group_by_checkbox.isChecked():
            self.group_by_option.setEnabled(True)
        else:
            self.group_by_option.setEnabled(False)
        self.reload_kanban_tab()

    def reload_kanban_tab(self):
        # Access the scroll_content layout
        scroll_area = self.current_ui.findChild(QScrollArea, 'scrollArea')
        scroll_content = scroll_area.widget()
        
        # If scroll_content does not have a layout, set a new QHBoxLayout
        if scroll_content.layout() is None:
            scroll_layout = QHBoxLayout(scroll_content)
            scroll_content.setLayout(scroll_layout)
        else:
            scroll_layout = scroll_content.layout()

        # Clear existing widgets
        while scroll_layout.count():
            item = scroll_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        # Build the database query
        query = []
        if self.show_all_projects and self.show_all_projects.isChecked():
            query.extend(self.session.query(Project).all())
        if self.show_all_tasks and self.show_all_tasks.isChecked():
            query.extend(self.session.query(Task).all())
        if self.show_all_subtasks and self.show_all_subtasks.isChecked():
            query.extend(self.session.query(SubTask).all())
        if self.show_all_deliverables and self.show_all_deliverables.isChecked():
            query.extend(self.session.query(Deliverable).all())
        if self.show_all_milestones and self.show_all_milestones.isChecked():
            query.extend(self.session.query(Milestone).all())
        # Existing checks in your code
        if self.categories_dropdown.currentText() != 'All Categories':
            query = [item for item in query if item.category == self.categories_dropdown.currentText()]

        if self.status_dropdown.currentText() != 'All Statuses':
            query = [item for item in query if item.status == self.status_dropdown.currentText()]

        if self.goal_verb_dropdown.currentText() != 'All Goal Verbs':
            query = [item for item in query if item.goal_verb == self.goal_verb_dropdown.currentText()]

        if self.use_case_dropdown.currentText() != 'All Use Cases':
            query = [item for item in query if item.use_case == self.use_case_dropdown.currentText()]

        if self.genre_dropdown.currentText() != 'All Genres':
            query = [item for item in query if item.genre == self.genre_dropdown.currentText()]


        if self.group_by_checkbox.isChecked():
            query = sorted(query, key=lambda x: getattr(x, self.group_by_option.currentText()))
        else:
            # sort by folder_dir
            query = sorted(query, key=lambda x: x.folder_dir)


        # get a list of all unique values for the group_by_option
        group_by_options = []
        for item in query:
            if getattr(item, self.group_by_option.currentText()) not in group_by_options:
                group_by_options.append(getattr(item, self.group_by_option.currentText()))

        
        if query != []:
            # for each unique value, create a new QVBox and add it to the scroll_layout
            for option in group_by_options:
                # create a custom group box without a title
                group_box = QGroupBox()
                group_box.setStyleSheet("QGroupBox {border: 0px; background-color: rgba(0,0,0,0);}")

                # create a QVBoxLayout inside a QScrollArea inside the group box
                scroll_area = QScrollArea()
                scroll_area.setWidgetResizable(True)
                # disable horizontal scrolling
                scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
                group_box_layout = QVBoxLayout()
                scroll_content = QWidget()
                scroll_content.setLayout(group_box_layout)
                scroll_area.setWidget(scroll_content)

                group_box_layout_inside_group_box = QVBoxLayout(group_box)
                group_box.setLayout(group_box_layout_inside_group_box)
                group_box_layout_inside_group_box.addWidget(scroll_area)

                scroll_layout.addWidget(group_box)

                group_box.setFixedWidth(350)  # Set minimum and maximum width to 300

               # Add a label for the title
                if isinstance(option, datetime):
                    label_option = option.strftime('%Y-%m-%d %H:%M:%S')
                    title_label = QLabel(str(label_option))
                else:
                    title_label = QLabel(option)

                group_box_layout.addWidget(title_label)

                # for each item in the query that matches the unique value, create a new KanbanListItem and add it to the group_box_layout
                for item in query:
                    if getattr(item, self.group_by_option.currentText()) == option:
                        kanbanItem = KanbanListItem(item)
                        # add the kanbanItem to the group_box_layout
                        group_box_layout.addWidget(kanbanItem)

                        kanbanItem.checkbox_toggled.connect(self.handle_checkbox_toggled)
                        kanbanItem.editClicked.connect(self.handle_edit_clicked)
                        kanbanItem.deleteClicked.connect(self.handle_delete_clicked)
                        
                # Add stretch to push all KanbanListItems to the top
                group_box_layout.addStretch(1)





    def load_gannt_tab_ui(self):
        self.data_collection_toolbar.hide()
        self.current_productivity_layout = 'gannt'
        self.load_ui('productivity_app/ui/gannt_ui.ui')

    def load_calendar_tab_ui(self):
        self.data_collection_toolbar.hide()
        self.current_productivity_layout = 'calendar'
        self.load_ui('productivity_app/ui/calendar_ui.ui')

    def load_table_tab_ui(self):
        self.data_collection_toolbar.hide()
        self.current_productivity_layout = 'table'
        self.load_ui('productivity_app/ui/table_ui.ui')

    def load_directory_view_tab_ui(self):
        self.data_collection_toolbar.hide()
        self.current_productivity_layout = 'directory_view'
        self.load_ui('productivity_app/ui/directory_view_ui.ui')
        



    def load_data_collection_layout(self):
        self.productivity_toolbar.hide()
        self.data_collection_toolbar.show()

        if self.current_data_collection_layout == 'overview':
            self.load_overview_tab_ui()
        elif self.current_data_collection_layout == 'physical_health':
            self.load_physical_health_tab_ui()
        elif self.current_data_collection_layout == 'mental_health':
            self.load_mental_health_tab_ui()
        elif self.current_data_collection_layout == 'financial':
            self.load_financial_tab_ui()
        elif self.current_data_collection_layout == 'relationship':
            self.load_relationship_tab_ui()
        elif self.current_data_collection_layout == 'other':
            self.load_other_tab_ui()
        elif self.current_data_collection_layout == 'collection_techniques':
            self.load_collection_techniques_tab_ui()


    def load_overview_tab_ui(self):
        self.productivity_toolbar.hide()
        self.current_data_collection_layout = 'overview'
        self.load_ui('productivity_app/ui/overview_ui.ui')

    def load_physical_health_tab_ui(self):
        self.productivity_toolbar.hide()
        self.current_data_collection_layout = 'physical_health'
        self.load_ui('productivity_app/ui/physical_health_ui.ui')

    def load_mental_health_tab_ui(self):
        self.productivity_toolbar.hide()
        self.current_data_collection_layout = 'mental_health'
        self.load_ui('productivity_app/ui/mental_health_ui.ui')

    def load_financial_tab_ui(self):
        self.productivity_toolbar.hide()
        self.current_data_collection_layout = 'financial'
        self.load_ui('productivity_app/ui/financial_ui.ui')

    def load_relationship_tab_ui(self):
        self.productivity_toolbar.hide()
        self.current_data_collection_layout = 'relationship'
        self.load_ui('productivity_app/ui/relationship_ui.ui')

    def load_other_tab_ui(self):
        self.productivity_toolbar.hide()
        self.current_data_collection_layout = 'other'
        self.load_ui('productivity_app/ui/other_ui.ui')

        self.reaction_game_btn = self.findChild(QPushButton, 'reactionGameBtn')
        self.reaction_game_btn.clicked.connect(self.handle_reaction_game_btn_clicked)

    def handle_reaction_game_btn_clicked(self):
        self.game_widget = ReactionTimeGameWidget(self)
        self.game_widget.game_over.connect(self.handle_game_over)
        self.main_layout.addWidget(self.game_widget)
        self.reaction_game_btn.setDisabled(True)

    def handle_game_over(self):
        self.main_layout.removeWidget(self.game_widget)
        self.game_widget.deleteLater()
        self.game_widget = None
        self.reaction_game_btn.setDisabled(False)




    def load_collection_techniques_tab_ui(self):
        self.productivity_toolbar.hide()
        self.current_data_collection_layout = 'collection_techniques'
        self.load_ui('productivity_app/ui/collection_techniques_ui.ui')

        # load in data_categories.csv
        data_file_path = 'productivity_app/data/data_categories.csv'

        # using pandas, get all the data from the csv file and separate it into active == "Yes" and inactive == "No" or "N/A"
        df = pd.read_csv(data_file_path)
        active_df = df[df['active'] == 'Yes']
        inactive_df = df[df['active'] != 'Yes']

        # create a list of all the active data categories
        active_data_categories = []
        for index, row in active_df.iterrows():
            active_data_categories.append(row['category'])

        # create a list of all the inactive data categories
        inactive_data_categories = []
        for index, row in inactive_df.iterrows():
            inactive_data_categories.append(row['category'])

        # create a list of all the data categories
        data_categories = active_data_categories + inactive_data_categories
        
        # read the csv file
        with open(data_file_path, 'r') as file:
            csv_reader = csv.reader(file)
            headers = next(csv_reader)  # get the headers
            data = []  # create a list to store the data
            for row in csv_reader:
                data.append(row)


        # Create the model and set it to the view
        model = MyTableModel(data, headers)
        self.table_widget = self.findChild(QTableView, 'dataTableView')
        self.table_widget.setModel(model)


    def load_settings_tab_ui(self):
        self.productivity_toolbar.hide()
        self.data_collection_toolbar.hide()
        self.load_ui('productivity_app/ui/settings_ui.ui')


    def handle_edit_clicked(self, item):
        # Handle when the edit button of an item has been clicked.
        print("edit clicked")
        print(item)
        



    def handle_delete_clicked(self, item):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setText(f"Are you sure you want to delete {item.title}?")
        msg.setWindowTitle("Delete Item")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
        retval = msg.exec()
        if retval == QMessageBox.StandardButton.Ok:
            self.session.delete(item)
            self.session.commit()
            self.reload_kanban_tab()


    def handle_checkbox_toggled(self, item, status):
        item.completed = status
        self.session.commit()
        if self.current_layout == 'kanban' and self.current_productivity_layout == 'kanban':
            self.reload_kanban_tab()
        elif self.current_layout == 'table' and self.current_productivity_layout == 'table':
            self.reload_table_tab()
        elif self.current_layout == 'calendar' and self.current_productivity_layout == 'calendar':
            self.reload_calendar_tab()
        elif self.current_layout == 'gannt' and self.current_productivity_layout == 'gannt':
            self.reload_gannt_tab()
        elif self.current_layout == 'directory_view' and self.current_productivity_layout == 'directory_view':
            self.reload_directory_view_tab()
        elif self.current_layout == 'dashboard':
            self.reload_dashboard_tab(item, status)
        elif self.current_layout == 'data_collection':
            self.reload_data_collection_tab()
        elif self.current_layout == 'settings':
            self.reload_settings_tab()
        elif self.current_layout == 'home':
            self.reload_home_tab()



app = QApplication([])
window = MainWindow()
app.exec()