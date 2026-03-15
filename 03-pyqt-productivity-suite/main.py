import datetime
from PyQt6.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QPushButton, QFileDialog, QWidget, QVBoxLayout, QLabel, QFrame, QCheckBox, QListWidget, QListWidgetItem, QHBoxLayout
from PyQt6.QtCore import Qt
from PyQt6 import uic
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from application.models.models import Base, Task
from application.custom_widgets.additional_widgets import UpcomingListItem

def create_session():
    engine = create_engine('sqlite:///productivity.db')
    Session = sessionmaker(bind=engine)
    session = Session()
    return session, engine

class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()

        # Create a session
        self.session = create_session()


        # Query the database using the session
        upcoming_items = self.session.query(Task).filter(Task.due_date > datetime.date.today()).all()

        ui_file = 'main.ui'
        
        # Load the UI file
        uic.loadUi(ui_file, self)


        # define widget
        self.layout = QVBoxLayout(self.centralwidget)


        # sidebar
        upcoming_sidebar = self.findChild(QFrame, 'upcomingSideBar')
        upcoming_list = upcoming_sidebar.findChild(QListWidget, 'upcomingList')

        if upcoming_items != []:
            for item in upcoming_items:
                upcomingItem = UpcomingListItem(item)
                listItem = QListWidgetItem()
                listItem.setSizeHint(upcomingItem.sizeHint())
                upcoming_list.addItem(listItem)
                upcoming_list.setItemWidget(listItem, upcomingItem)


        # toolbars
        main_toolbar = self.findChild(QFrame, 'mainToolBar')

        # Define dictionary to hold all layouts
        self.main_layouts = {
            'home': self.findChild(QFrame, 'home_layout'),
            'dashboard': self.findChild(QFrame, 'dashboard_layout'),
            'productivity': self.findChild(QFrame, 'productivity_layout'),
            'data_collection': self.findChild(QFrame, 'data_collection_layout'),
            'settings': self.findChild(QFrame, 'settings_layout'),
        }
        
        self.secondary_layouts = {
            'kanban': self.findChild(QFrame, 'kanban_layout'),
            'gannt': self.findChild(QFrame, 'gannt_layout'),
            'calendar': self.findChild(QFrame, 'calendar_layout'),
            'table': self.findChild(QFrame, 'table_layout'),
            'directory_view': self.findChild(QFrame, 'directory_view_layout'),
        }

        self.layouts = {**self.main_layouts, **self.secondary_layouts}
        
        self.set_all_layouts_hidden()
        self.main_layouts['home'].show()

        productivity_toolbar = self.findChild(QFrame, 'productivityToolBar')
        productivity_toolbar.hide()

        self.toolbar_buttons = {
            'home': main_toolbar.findChild(QPushButton, 'mainHomeBtn'),
            'dashboard': main_toolbar.findChild(QPushButton, 'mainDashboardBtn'),
            'productivity': main_toolbar.findChild(QPushButton, 'mainProductivityBtn'),
            'data_collection': main_toolbar.findChild(QPushButton, 'mainDataCollectionBtn'),
            'settings': main_toolbar.findChild(QPushButton, 'mainSettingsBtn'),
            'kanban': productivity_toolbar.findChild(QPushButton, 'productivityKanbanBtn'),
            'gannt': productivity_toolbar.findChild(QPushButton, 'productivityGanntBtn'),
            'calendar': productivity_toolbar.findChild(QPushButton, 'productivityCalendarBtn'),
            'table': productivity_toolbar.findChild(QPushButton, 'productivityTableBtn'),
            'directory_view': productivity_toolbar.findChild(QPushButton, 'productivityDirectoryViewBtn'),
        }

        for layout_name, button in self.toolbar_buttons.items():
            button.clicked.connect(lambda checked, layout_name=layout_name: self.handle_button_click(layout_name))

        self.productivity_toolbar = productivity_toolbar
        self.productivity_layout = self.main_layouts['productivity']

        self.show()

    def closeEvent(self, event):
        self.session.close()
        event.accept()

    def handle_button_click(self, layout_name):
        if layout_name in self.main_layouts:
            self.set_all_layouts_hidden()
            self.layouts[layout_name].show()
            self.set_secondary_toolbar()

        elif self.productivity_layout.isVisible():
            self.set_all_secondary_layouts_hidden()
            self.layouts[layout_name].show()
            self.set_secondary_toolbar()

    def set_all_layouts_hidden(self):
        for layout in self.layouts.values():
            layout.hide()

    def set_all_secondary_layouts_hidden(self):
        for layout_name, layout in self.secondary_layouts.items():
            layout.hide()

    def set_secondary_toolbar(self):
        if self.productivity_layout.isVisible():
            self.productivity_toolbar.show()
        else:
            self.productivity_toolbar.hide()

app = QApplication(sys.argv)
UIWindow = UI()
app.exec()
