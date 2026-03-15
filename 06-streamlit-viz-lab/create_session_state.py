import streamlit as st
import pandas as pd

class StateManager:
    def __init__(self, create_screen_template, edit_screen_template, delete_screen_template, view_screen_template):
        self.actions = ['create', 'edit', 'delete', 'view']
        self.items = ['folder', 'project', 'task', 'milestone', 'deliverable']
        self.extra_states = ['selected_id', 'selected_name']
        self.screen_templates = {
            'create': create_screen_template,
            'edit': edit_screen_template,
            'delete': delete_screen_template,
            'view': view_screen_template
        }
        self.initialize_states()

    def initialize_states(self):
        for action in self.actions:
            for item in self.items:
                st.session_state[f"{action}_{item}"] = False
        for extra in self.extra_states:
            for item in self.items:
                st.session_state[f"{extra}_{item}"] = None

home_screen_template = st.empty()
create_screen_template = st.empty()
edit_screen_template = st.empty()
delete_screen_template = st.empty()
view_screen_template = st.empty()

state_manager = StateManager(create_screen_template, edit_screen_template, delete_screen_template, view_screen_template)

def check_states():
    # For each action, check if any of the items have this action set to True.
    # If so, set all other actions for all items to False.
    for action in state_manager.actions:
        if any([st.session_state[f"{action}_{item}"] for item in state_manager.items]):
            for other_action in [a for a in state_manager.actions if a != action]:
                for item in state_manager.items:
                    st.session_state[f"{other_action}_{item}"] = False
        else:
            for template in state_manager.screen_templates.values():
                template.empty()

    # For each action and item, check if it's True.
    # If so, set some specific 'extra' states depending on the action and item.
    for action in state_manager.actions:
        for item in state_manager.items:
            if st.session_state[f"{action}_{item}"]:
                if action == 'create':
                    for other_action in [a for a in state_manager.actions if a != action]:
                        home_screen_template.empty()
                        state_manager.screen_templates[other_action].empty()
                    if item == 'folder':
                        for extra in state_manager.extra_states:
                            for other_item in state_manager.items:
                                st.session_state[f"{extra}_{other_item}"] = None

                    elif item == 'project':
                        st.session_state["selected_id_folder"] = "value"
                        st.session_state["selected_name_folder"] = "value"
                    elif item in ['task', 'milestone', 'deliverable']:
                        for extra in state_manager.extra_states:
                            for other_item in ['folder', 'project']:
                                st.session_state[f"{extra}_{other_item}"] = "value"

    # For each action in edit, delete and view, check if any of the items have this action set to True.
    # If so, set the 'extra' states in the corresponding column to "value".
    for action in ['edit', 'delete', 'view']:
        for item in state_manager.items:
            if st.session_state[f"{action}_{item}"]:
                st.session_state["selected_id_" + item] = "value"
                st.session_state["selected_name_" + item] = "value"
                if item == 'project':
                    for extra in state_manager.extra_states:
                        for other_item in ['folder', 'project']:
                            st.session_state[f"{extra}_{other_item}"] = "value"
                elif item in ['task', 'milestone', 'deliverable']:
                    for extra in state_manager.extra_states:
                        for other_item in ['folder', 'project', item]:
                            st.session_state[f"{extra}_{other_item}"] = "value"


def display_states():
    for state in st.session_state.keys():
        if st.session_state[state] not in [None, False]:
            st.write(f"{state}: {st.session_state[state]}")
            print(f"{state}: {st.session_state[state]}")
            
def read_csv():
    df = pd.read_csv('productivity/csvs/productivity.csv')
    for _, row in df.iterrows():
        st.session_state[f"selected_id_{row['identifying_type']}"] = row['id']
        st.session_state[f"selected_name_{row['identifying_type']}"] = row['title']
    return df

def reset_states():
    for action in state_manager.actions:
        for item in state_manager.items:
            st.session_state[f"{action}_{item}"] = False
    for extra in state_manager.extra_states:
        for item in state_manager.items:
            st.session_state[f"{extra}_{item}"] = None

def update_state(action, item):
    # Ensure the action and item are valid
    if action not in state_manager.actions or item not in state_manager.items:
        st.warning(f"Invalid action '{action}' or item '{item}'.")
        return

    # Set the action_item state
    st.session_state[f"{action}_{item}"] = True

    # Set the selected_id and selected_name states
    if action == "create":
        if item == "folder":
            for other_item in state_manager.items:
                st.session_state[f"selected_id_{other_item}"] = None
                st.session_state[f"selected_name_{other_item}"] = None
        elif item in ["project", "task", "milestone", "deliverable"]:
            st.session_state["selected_id_folder"] = "value"
            st.session_state["selected_name_folder"] = "value"
            if item in ["task", "milestone", "deliverable"]:
                st.session_state["selected_id_project"] = "value"
                st.session_state["selected_name_project"] = "value"
    elif action in ["edit", "delete", "view"]:
        st.session_state[f"selected_id_{item}"] = "value"
        st.session_state[f"selected_name_{item}"] = "value"

    st.experimental_rerun()


check_states()
display_states()

# Main code
productivity_csv = read_csv()

folders = {}
projects = {}
tasks = {}
milestones = {}
deliverables = {}
attachments = {}
comments = {}

for index, row in productivity_csv.iterrows():
    if row['identifying_type'] == "folder":
        folders[row['id']] = row['title']
    elif row['identifying_type'] == "project":
        projects[row['id']] = row['title']
    elif row['identifying_type'] == "task":
        tasks[row['id']] = row['title']
    elif row['identifying_type'] == "milestone":
        milestones[row['id']] = row['title']
    elif row['identifying_type'] == "deliverable":
        deliverables[row['id']] = row['title']
    elif row['identifying_type'] == "attachment":
        attachments[row['id']] = row['title']
    elif row['identifying_type'] == "comment":
        comments[row['id']] = row['title']








with home_screen_template.container():
    st.title("Home")
    create_folder_button = st.button("Create a new folder")
    if len(folders) > 0:
        selected_folder = st.selectbox('Select a folder', list(folders.values()))
        st.session_state["selected_id_folder"] = list(folders.keys())[list(folders.values()).index(selected_folder)]
        st.session_state["selected_name_folder"] = selected_folder
        view_folder_button = st.button("View folder")
        if view_folder_button:
            update_state("view", "folder")
    if create_folder_button:
        update_state("create", "folder")





with edit_screen_template.container():
    st.title("Edit a folder")
    input_fields_placeholder = st.empty()
    save_button_placeholder = st.empty()
    cancel_button_placeholder = st.empty()

with delete_screen_template.container():
    st.title("Delete a folder")
    warning_placeholder = st.empty()
    delete_button_placeholder = st.empty()
    cancel_button_placeholder = st.empty()


with view_screen_template.container():
    st.title("View a folder")
    home_button_placeholder = st.empty()
    edit_button_placeholder = st.empty()
    delete_button_placeholder = st.empty()
    create_button_placeholder = st.empty()
    view_project_button_placeholder = st.empty()




create_screen_template_title = st.empty()

if st.session_state.create_folder:
    with create_screen_template.container():
        create_screen_template_title = st.empty()
        

check_states()

if st.session_state.create_folder:
    back_btn = st.button("Back")
    if back_btn:
        reset_states()
        check_states()
    create_title = st.title("Create a new folder")
    input_fields = st.text_input("Enter a name for the folder")
    save_button = st.button("Save")
    cancel_button = st.button("Cancel")
    if cancel_button:
        reset_states()
        check_states()
    if save_button:
        st.success(f"Folder '{input_fields}' created.")

if st.session_state.view_folder:
    back_btn = st.button("Back")
    if back_btn:
        reset_states()
        check_states()
    view_title = st.title("View folder")
    edit_button = st.button("Edit Folder")
    delete_button = st.button("Delete Folder")
    if edit_button:
        update_state("edit", "folder")
        check_states()
    if delete_button:
        update_state("delete", "folder")
        check_states()