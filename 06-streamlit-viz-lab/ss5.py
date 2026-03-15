# Import Streamlit and other necessary libraries
import streamlit as st
from typing import Any
import json, csv

# Define the classes for your Objects
class Folder:
    def __init__(self):
        pass # add attributes and methods

    @staticmethod
    def create():
        title_area = st.title("Create New Folder")
        title = st.text_input('Enter folder title here')
        save_button = st.button("Save New Folder")
        cancel_button = st.button("Cancel")

        if save_button:
            st.success(f"Folder '{title}' created.")

        if cancel_button:
            st.info("Cancelled folder creation.")

    @staticmethod
    def view():
        pass # add Streamlit calls for view layout

    @staticmethod
    def edit():
        pass # add Streamlit calls for edit layout

    @staticmethod
    def delete():
        pass # add Streamlit calls for delete layout

class Project:
    def __init__(self):
        pass # add attributes and methods

    @staticmethod
    def create():
        pass # add Streamlit calls for create layout

    @staticmethod
    def view():
        pass # add Streamlit calls for view layout

    @staticmethod
    def edit():
        pass # add Streamlit calls for edit layout

    @staticmethod
    def delete():
        pass # add Streamlit calls for delete layout

class Task:
    def __init__(self):
        pass # add attributes and methods

    @staticmethod
    def create():
        pass # add Streamlit calls for create layout

    @staticmethod
    def view():
        pass # add Streamlit calls for view layout

    @staticmethod
    def edit():
        pass # add Streamlit calls for edit layout

    @staticmethod
    def delete():
        pass # add Streamlit calls for delete layout

class Milestone:
    def __init__(self):
        pass # add attributes and methods

    @staticmethod
    def create():
        pass # add Streamlit calls for create layout

    @staticmethod
    def view():
        pass # add Streamlit calls for view layout

    @staticmethod
    def edit():
        pass # add Streamlit calls for edit layout

    @staticmethod
    def delete():
        pass # add Streamlit calls for delete layout

class Deliverable:
    def __init__(self):
        pass # add attributes and methods

    @staticmethod
    def create():
        pass # add Streamlit calls for create layout

    @staticmethod
    def view():
        pass # add Streamlit calls for view layout

    @staticmethod
    def edit():
        pass # add Streamlit calls for edit layout

    @staticmethod
    def delete():
        pass # add Streamlit calls for delete layout

class Attachment:
    def __init__(self):
        pass # add attributes and methods

    @staticmethod
    def create():
        pass # add Streamlit calls for create layout

    @staticmethod
    def view():
        pass # add Streamlit calls for view layout

    @staticmethod
    def edit():
        pass # add Streamlit calls for edit layout

    @staticmethod
    def delete():
        pass # add Streamlit calls for delete layout

class ToDo:
    def __init__(self):
        pass # add attributes and methods

    @staticmethod
    def create():
        pass # add Streamlit calls for create layout

    @staticmethod
    def view():
        pass # add Streamlit calls for view layout

    @staticmethod
    def edit():
        pass # add Streamlit calls for edit layout

    @staticmethod
    def delete():
        pass # add Streamlit calls for delete layout




class SessionStateManager:
    def __init__(self):
        self.actions = ['create', 'edit', 'delete', 'view']
        self.items = ['folder', 'project', 'task', 'milestone', 'deliverable', 'home']
        self.extra_states = ['selected_id', 'selected_name']
        self.initialize_states()
        self.current_action = None
        self.current_item = None

    def initialize_states(self):
        for action in self.actions:
            for item in self.items:
                st.session_state[f"{action}_{item}"] = False
        for extra in self.extra_states:
            for item in self.items:
                st.session_state[f"{extra}_{item}"] = None

    def update_current_action_and_item(self, action, item):
        self.current_action = action
        self.current_item = item


# Define a class to encapsulate all your functionality
class StreamlitApp:
    def __init__(self):
        self.state_manager = SessionStateManager()

        self.objects = {
            'Folder': Folder(),
            'Project': Project(),
            'Task': Task(),
            'Milestone': Milestone(),
            'Deliverable': Deliverable(),
            'Attachment': Attachment(),
            'ToDo': ToDo(),
        }

        self.functions = {
            'Write_to_JSON': self.write_to_json,
            'Write_to_csv': self.write_to_csv,
            'handle_btn_clicks': self.handle_btn_clicks,
        }

    
    def create_components(self):

        btns = {"create_btn": st.empty()}

        return btns

    def view_components(self, item):
        st.write("View Components")
        
        self.components['view'] = st.button('View', key=f'view_{item}')

    def home_layout(self):
        st.write("Home Layout")
        self.btns = self.create_components()

        if self.btns['create_btn'].button("Create"):
            print("YESS")
    
    def create_components(self, item):
        self.components['create'] = st.button('Create', key=f'create_{item}')

    def write_to_json(self, obj: Any):
        # define your write_to_json function
        pass

    def write_to_csv(self, obj: Any):
        # define your write_to_csv function
        pass

    def handle_btn_clicks(self, details):
        # handle button clicks
        session_action = None
        session_item = None

        if details['item'] is not None:  # check if item is selected in the selectbox
            for key, value in details.items():
                if key != 'item' and value:  # process other keys (button presses)
                    session_action = key
                    session_item = details['item']

            if session_action:  # check if any button is pressed
                if self.state_manager.current_action == session_action:
                    pass
                else:
                    self.state_manager.update_current_action_and_item(session_action, session_item)
                    self.show_layout()


    def check_session_state(self):
        st.write("Check Session State")
        if self.state_manager.current_action is not None:
            action = str(self.state_manager.current_action)
            action = action.capitalize()
        if self.state_manager.current_item is not None:
            item = str(self.state_manager.current_item)
            item = item.capitalize()

    def show_layout(self):
        st.write("Show Layout")
        self.check_session_state()
        st.write(self.state_manager.current_action)
        st.write(self.state_manager.current_item)
        if self.state_manager.current_action and self.state_manager.current_item:
            layout = self.objects[self.state_manager.current_item]
            if self.state_manager.current_action == 'view':
                self.view_components(self.state_manager.current_item)
            elif self.state_manager.current_action == 'create':
                layout.create()
            elif self.state_manager.current_action == 'edit':
                layout.edit()
            elif self.state_manager.current_action == 'delete':
                layout.delete()
        else:
            self.home_layout()
            


if __name__ == "__main__":
    app = StreamlitApp()
    app.show_layout()

    for component in app.components:
        # Check if the button is clicked or selectbox is changed
        if st.session_state.get(component, False):
            app.functions['handle_btn_clicks'](app.components)

