import os
import streamlit as st
from app.csv_creation import create_csvs
import pandas as pd
import json
import datetime
from app.administrative import make_safe, valid_value, CustomJSONEncoder, formatted_options, comment_safe

directory_path = "productivity"
if not os.path.exists(directory_path):
    os.makedirs(directory_path)

csv_folder = "csvs"
if not os.path.exists(os.path.join(directory_path, csv_folder)):
    os.makedirs(os.path.join(directory_path, csv_folder))

productivity_csv_path, timeline_csv_path = create_csvs(directory_path, csv_folder)
productivity_csv = pd.read_csv(productivity_csv_path)
timeline_csv = pd.read_csv(timeline_csv_path)

if "save_successful" not in st.session_state:
    st.session_state.save_successful = False

if st.session_state.save_successful:
    st.success(st.session_state.save_successful)


def success_func(txt="Success"):
    success_txt = txt
    st.session_state.clear()
    if "save_successful" not in st.session_state:
        st.session_state.save_successful = success_txt
    st.experimental_rerun()
    st.success(st.session_state.save_successful)
    st.session_state.save_successful = False




def check_if_folders_exist():
    # Filter by identifying_type for folder
    folder_data = productivity_csv[productivity_csv['identifying_type'] == 'folder'].sort_values(by=['date_updated'], ascending=False)

    # Create a dictionary of folder titles and ids from the csv file
    folders = {row["title"]: row["id"] for _, row in folder_data.iterrows()}

    # If no folder in the csv, selected_folder will be None
    if len(folder_data) == 0:
        st.session_state.selected_folder = None
        st.session_state.edit_folder = False
        st.session_state.delete_folder = False
        st.session_state.view_folder = False

        st.session_state.create_project = False
        st.session_state.edit_project = False
        st.session_state.delete_project = False

        st.session_state.create_task = False
        st.session_state.edit_task = False
        st.session_state.delete_task = False

        st.session_state.create_milestone = False
        st.session_state.edit_milestone = False
        st.session_state.delete_milestone = False

        st.session_state.create_deliverable = False
        st.session_state.edit_deliverable = False
        st.session_state.delete_deliverable = False
    else:
        st.session_state.edit_folder = True
        st.session_state.delete_folder = True
        st.session_state.create_project = True
        st.session_state.view_folder = True

        st.session_state.selected_folder = folder_data.iloc[0]['id']
        st.session_state.selected_folder_name = folder_data.iloc[0]['title']
            
    return folders, folder_data

folders, folder_data = check_if_folders_exist()



def add_new_folder_data():
    title = st.text_input("Folder Title")
    if savebtn:
        if not valid_value(title):
            st.warning("Please enter a valid title")
        else:
            try:
                add_folder(title)
                success_func("Folder created successfully.")
            except Exception as e:
                st.write(f"An error occurred: {e}")


def add_folder(title):
    # check if title already exists and check if title is valid
    if title in folders:
        st.error(f"Error: Folder with title '{title}' already exists")
        return
    elif not valid_value(title):
        st.error(f"Error: Invalid folder title '{title}'")
        return
    else:
        today = datetime.datetime.now()
        today = pd.to_datetime(today.strftime("%Y-%m-%d %H:%M:%S"))
        new_folder_path = os.path.join(directory_path, title)
        if not os.path.exists(new_folder_path):
            os.makedirs(new_folder_path)
        new_folder_json_data_path = os.path.join(new_folder_path, 'json_data')
        if not os.path.exists(new_folder_json_data_path):
            os.makedirs(new_folder_json_data_path)
        new_folder_data = {
            "id": [make_safe()],
            "date_created": [today],
            "date_updated": [today],
            "folder_dir": [directory_path],
            "file_name": [title],
            "identifying_type": ["folder"],
            "title": [title],
            "parent": [""]
        }
        new_folder = pd.DataFrame(new_folder_data)
        new_folder.to_csv(productivity_csv_path, mode="a", header=False, index=False)





















class ModeContainer:
    def __init__(self, name):
        self.container = st.container()
        self.elements = {}

    def add_element(self, element_name):
        self.elements[element_name] = self.container.button(f"{element_name} placeholder")

    def add_view_components(self, components):
        for component in components:
            self.add_element(component)

class StreamlitApp:
    def __init__(self, modes, view_objects, components):
        self.modes = self.init_modes(modes)
        self.buttons_row = self.init_buttons_row()
        self.view_objects = self.init_view_objects(view_objects, components)
        self.current_mode = None

    def init_modes(self, modes):
        mode_containers = {}
        for mode in modes:
            mode_containers[mode] = ModeContainer(mode)
        return mode_containers

    def init_buttons_row(self):
        btn_cols = st.columns(5)
        buttons_row = [col.empty() for col in btn_cols]
        return buttons_row

    def init_view_objects(self, view_objects, components):
        view_obj_containers = {}
        for obj in view_objects:
            view_obj_containers[obj] = ModeContainer(obj)
            view_obj_containers[obj].add_view_components(components)
        return view_obj_containers

    def handle_button_clicks(self):
        for mode in self.modes:
            if self.modes[mode].container.button(f"{mode} button"):
                self.current_mode = mode
                if mode == "create":
                    if self.buttons_row[0].button("Save Folder"):
                        add_new_folder_data()

modes = ['home', 'view', 'create', 'edit', 'delete']
view_objects = ['folder', 'project', 'task', 'milestone', 'deliverable']
components = ['title', 'description', 'tasks', 'milestones', 'deliverables']

app = StreamlitApp(modes, view_objects, components)

while True:
    app.handle_button_clicks()

