import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QListWidget
from PyQt6.QtCore import Qt
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Set up database
engine = create_engine('sqlite:///example.db', echo=True)
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    nickname = Column(String)

    def __repr__(self):
        return "<User(name='%s', fullname='%s', nickname='%s')>" % (
                            self.name, self.fullname, self.nickname)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.session = Session()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 800, 400)
        self.setWindowTitle('Streamlit Like App')

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Add a Button
        button = QPushButton("Add user")
        button.clicked.connect(self.on_button_clicked)
        layout.addWidget(button)

        # Add a ListWidget
        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)
        self.update_user_list()

    def on_button_clicked(self):
        # Add a user to the database
        new_user = User(name='new', fullname='New User', nickname='newbie')
        self.session.add(new_user)
        self.session.commit()
        self.update_user_list()

    def update_user_list(self):
        # Update the list widget with all users in the database
        self.list_widget.clear()
        for instance in self.session.query(User).order_by(User.id):
            self.list_widget.addItem(f"{instance.name}, {instance.fullname}, {instance.nickname}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec())
