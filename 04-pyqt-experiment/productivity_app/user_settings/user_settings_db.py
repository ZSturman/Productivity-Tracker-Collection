import os
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json

Base = declarative_base()

class UserSettings(Base):
    __tablename__ = 'user_settings'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    options = Column(Text)  # We will store the list as a JSON string

    def get_options(self):
        return json.loads(self.options)

    def set_options(self, options):
        self.options = json.dumps(options)

def create_user_settings_db():
    engine = create_engine('sqlite:///productivity_app/user_settings/user_settings.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    # Convert the options in your combo_lists.py file to UserSettings objects
    from user_settings.combo_lists import category_options, goal_verb_options, genre_options, use_case_options,status_options, priority_options, group_by_options
    default_folder_directory = "/Users/zacharysturman/Library/Mobile Documents/com~apple~CloudDocs"
    settings = [
        UserSettings(name='category_options', options=json.dumps(category_options)),
        UserSettings(name='goal_verb_options', options=json.dumps(goal_verb_options)),
        UserSettings(name='genre_options', options=json.dumps(genre_options)),
        UserSettings(name='use_case_options', options=json.dumps(use_case_options)),
        UserSettings(name='status_options', options=json.dumps(status_options)),
        UserSettings(name='priority_options', options=json.dumps(priority_options)),
        UserSettings(name='group_by_options', options=json.dumps(group_by_options)),
        UserSettings(name='folder_directory', options=default_folder_directory)
    ]
    session.add_all(settings)
    session.commit()

# Now we can use this function to create the database:
create_user_settings_db()