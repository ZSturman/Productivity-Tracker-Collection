import os
import streamlit as st
from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
import numpy as np
import json
from create_project_module import Project, sections
from file_output import file_output, display_project_json
import uuid
import datetime
from datetime import date
from pathlib import Path
import time
import glob
from csv_file_creation import create_csvs
from administrative_funcs import CustomJSONEncoder, valid_value, conditional_date_input, formatted_options



# make streamlit wide
st.set_page_config(layout="wide")

### CSS
css_file = Path("gantt_and_proj_creation_v1/custom.css").read_text()
st.markdown(f"<style>{css_file}</style>", unsafe_allow_html=True)
st.markdown("<div class='custom-text'>Hello, Streamlit with custom CSS!</div>", unsafe_allow_html=True)

st.write("Click on 'Add Milestone'. -> Opens edit screen for milestone -> when save is clicked it brings you back to the previous page with the new milestone added")
st.write("If 'completed'==True add to csv. Remove from repo for additions like adding tasks")
st.write("If it is a project that is complete, have the option to mark tasks, deliverables and milestones as complete if they are not")
st.write("Add if new task, habit or whatever that the inputs are revealed to add the title, add due date or other stuff like that. Then the save button officially saves it")
st.write("Create new function for handling edit_milestone_btn and others like it. The current system of edit_mode, edit_tab won't work")
st.write("Finish edit_items_item. Make the save actually work")
st.write("For everything that is created, 'project','milestone','errand',etc., have the edit screen pop up for it. ")

# set directory
directory_path = "productivity"
if not os.path.exists(directory_path):
    os.makedirs(directory_path)

productivity_csv_path, relationships_csv_path, timeline_csv_path  = create_csvs(directory_path)


# Load Options Lists
with open("gantt_and_proj_creation_v1/options_lists.json", "r") as file:
    options_data = json.load(file)

options_lists = options_data





### Initialize session states
session_states = ["edit_mode", "edit_tab", "save_mode", "save_successful", "create_new_task", "folder_dir", "type", "is_parent", "parent_id", "parent_type", "is_child", "child_id", "child_type", "create_new_deliverable", "create_new_milestone"]
for state in session_states:
    if state not in st.session_state:
        st.session_state[state] = False

if st.session_state.save_successful:
    st.success(st.session_state.save_successful)




def success_func(txt="Success"):
    st.session_state.save_successful = txt
    st.experimental_rerun()
    st.success(st.session_state.save_successful)
    st.session_state.save_successful = False



relationships_csv = "productivity/relationships.csv"

# This function will add a new relationship
def add_relationship(parent_id, parent_type, child_id, child_type):
    # First, check if the relationship is valid
    if parent_id == child_id:
        raise ValueError('An item cannot be a parent or child of itself')

    # Load the current relationships
    try:
        df = pd.read_csv(relationships_csv)
    except pd.errors.EmptyDataError:
        # If the file is empty, create a new DataFrame
        df = pd.DataFrame(columns=['parent_id', 'parent_type', 'child_id', 'child_type'])

    # Check if this relationship will create a cycle
    if any((df['parent_id'] == child_id) & (df['child_id'] == parent_id)):
        raise ValueError('Cannot create a circular reference')

    # If the checks pass, add the relationship
    new_row = {'parent_id': parent_id, 'parent_type': parent_type, 'child_id': child_id, 'child_type': child_type}
    df = pd.DataFrame([new_row])
    df.to_csv(relationships_csv, mode='a', header=False, index=False)







def create_new_folder(folder_directory_path, item_name):
    today = datetime.datetime.now()
    today = pd.to_datetime(today.strftime("%Y-%m-%d %H:%M:%S"))
    new_folder_path = os.path.join(folder_directory_path, item_name)
    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)
        # add json_data folder to new folder
        json_data_path = os.path.join(new_folder_path, 'json_data')
        if not os.path.exists(json_data_path):
            os.makedirs(json_data_path)
        title = item_name
        data = {
            "id": uuid.uuid4(),
            "date_created": today.strftime("%Y-%m-%d %H:%M:%S"),
            "date_updated": today.strftime("%Y-%m-%d %H:%M:%S"),
            "folder_dir": new_folder_path,
            "identifying_type": 'folder',
            "title": title,
            "most_recently_selected": today.strftime("%Y-%m-%d %H:%M:%S")
        }
        safe_title = str(uuid.uuid4())
        safe_title = safe_title.replace(" ", "_")
        safe_title = safe_title.replace("-", "_")
        data["id"] = safe_title
        # add "data" row to productivity.csv file
        df = pd.DataFrame([data])
        df.to_csv(productivity_csv_path, mode='a', header=False, index=False)
        if "selected_folder" not in st.session_state:
            st.session_state.selected_folder = title
        create_new_item(json_data_path, 'project')
    else:
        st.sidebar.warning("Folder already exists. Please enter a different folder name.")
        return False



def create_new_item(item_directory_path, item_type, is_parent=False, parent_id=None, parent_type=None, is_child=False, child_id=None, child_type=None):
    try:
        productivity_df = pd.read_csv(productivity_csv_path)
        today = datetime.datetime.now()
        today = pd.to_datetime(today.strftime("%Y-%m-%d %H:%M:%S"))
        item_count = sum(productivity_df['identifying_type'] == item_type)
        item_title = item_type.capitalize()
        title = f"{item_title} {item_count + 1}"
        data = {
            "id": 00000000,
            "date_created": today.strftime("%Y-%m-%d %H:%M:%S"),
            "date_updated": today.strftime("%Y-%m-%d %H:%M:%S"),
            "folder_dir": item_directory_path,
            "identifying_type": item_type,
            "title": title,
            "most_recently_selected": today
        }
        new_project = Project()
        new_project.edit_title_and_identifying_type(title, item_type)
        if is_parent:
            add_relationship(new_project.id, item_type, child_id, child_type)
        elif is_child:
            add_relationship(parent_id, parent_type, new_project.id, item_type)
        data_json = {
            "id": new_project.id,
            "date_modified": new_project.date_modified,
            "date_created": new_project.date_created,
            "editable_data": {
                "required": new_project.editable_data["required"],
                "time": {
                    "completed": False,
                    "started": False,
                    "due": False
                },
                "scheduling": {
                    "is_recurring": False,
                }
            }
        }
        for key, value in options_lists["input_types"].items():
            if key not in data_json["editable_data"]:
                data_json["editable_data"][key] = {}
            for k, v in value.items():
                if k not in data_json["editable_data"][key]:
                    data_json["editable_data"][key][k] = v.get("default")

        safe_title = new_project.id.replace(" ", "_")
        safe_title = safe_title.replace("-", "_")
        data["id"] = str(safe_title)

        df = pd.DataFrame([data])
        df.to_csv(f"{directory_path}/productivity.csv", mode='a', header=False, index=False)

        if not os.path.exists(item_directory_path):
            os.makedirs(item_directory_path)

        filename = os.path.join(item_directory_path, f"{item_type}_{safe_title}.json")
        with open(filename, "w") as f:
            json.dump(data_json, f, indent=4)
        success_txt = f"'{title}' created."

        if "selected_item" not in st.session_state:
            st.session_state.selected_item = title

        success_func(success_txt)

        del st.session_state.create_new_task
        del st.session_state.create_new_deliverable
        del st.session_state.folder_dir
        del st.session_state.type
        del st.session_state.is_parent 
        del st.session_state.parent_id
        del st.session_state.parent_type
        del st.session_state.is_child 
        del st.session_state.child_id
        del st.session_state.child_type

    except FileNotFoundError:
        print(f"The file {productivity_csv_path} could not be found.")
    except PermissionError:
        print(f"Permission denied when accessing the file {productivity_csv_path}.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")



# set up sidebar
folder_name = st.sidebar.text_input("Folder Name")
create_folder_button = st.sidebar.button("Create Folder")
selected_folder = None

# replace create_new_item function calls with the respective new functions
if create_folder_button:
    if folder_name:
        folder_created = create_new_folder(directory_path, folder_name)
    else:
        st.sidebar.warning("Please enter a folder name.")




# add to existing folder
def save_comment_to_md_file(selected_folder, comment, item_id):
    directory = f"{directory_path}/{selected_folder}/comments/{item_id}"
    if not os.path.exists(directory):
        os.makedirs(directory)

    comment_id = str(uuid.uuid4())
    md_file_path = f"{directory}/{comment_id}.md"

    with open(md_file_path, "w") as f:
        f.write(comment)

    return md_file_path

def add_comment_to_project(projects, selected_folder, item_id, comment):
    md_file_path = save_comment_to_md_file(selected_folder, comment, item_id)

    for project in projects:
        if project["id"] == item_id:
            if "comments" not in project["editable_data"]["notes"]:
                project["notes"]["comments"] = []
            project["editable_data"]["notes"]["comments"].append({"id": str(uuid.uuid4()), "path": md_file_path})

    return projects

def handle_time_intervals(project_id, path, time, time_key, old_values, project_data):
    if not valid_value(old_values):
        old_values = {"days": 0, "hours": 0, "minutes": 0, "seconds": 0}

    input_types = options_lists["input_types"].get(f"time.{time_key}")

    if input_types:
        input_types_label = input_types.get("label")
        input_types_intervals = input_types.get("intervals")

        if input_types_intervals:
            st.write(input_types_label)
            interval_columns = st.columns(4)
            new_values = {}

            for idx, interval_key in enumerate(["days", "hours", "minutes", "seconds"]):
                interval_data = input_types_intervals.get(interval_key)

                if interval_data:
                    interval_label = interval_data.get("label")
                    interval_description = interval_data.get("description")

                    with interval_columns[idx]:
                        interval_value = st.number_input(interval_label, value=old_values[interval_key], help=interval_description)

                    if interval_value != old_values[interval_key]:
                        new_values[interval_key] = interval_value

            if new_values != old_values:
                new_values = {**old_values, **new_values}
                project_data["editable_data"]["time"][time_key] = new_values

                if st.button("Save", key=f"{project_id}_{time_key}"):
                    with open(f"{path}/project_{project_id}.json", "w") as f:
                        json.dump(project_data, f, indent=4, cls=CustomJSONEncoder)
                    st.session_state.edit_mode = False
                    st.experimental_rerun()

def handle_time_section(project_id, path, time, time_key, options_lists, project_data):
    current_value = time[time_key]
    input_types = options_lists["input_types"]["time"].get(time_key)
    if input_types:
        input_types_label = input_types.get("label")
        input_types_description = input_types.get("description")

    new_value = st.checkbox(input_types_label, value=current_value, help=input_types_description, key=f"{project_id}_{time_key}_checkbox")

    # find the project_id in the id column from the productivity.csv file
    # if the project_id is found, then save the value from that row's "folder_dir" column as the variable 'folder_path'
    productivity_df = pd.read_csv(productivity_csv_path)
    folder_path = productivity_df.loc[productivity_df['id'] == project_id, 'folder_dir'].values[0]

    if new_value != current_value and new_value == False:
        st.subheader(f"Remove {time_key} date?")
        project_data["editable_data"]["time"][time_key] = new_value
        project_data["editable_data"]["time"][f"date_{time_key}"] = None
        project_data["editable_data"]["time"][f"time_{time_key}"] = None
        if st.button("Save", key=f"{project_id}_{time_key}_save"): # appended '_save'
            with open(f"{folder_path}/project_{project_id}.json", "w") as f:
                json.dump(project_data, f, indent=4, cls=CustomJSONEncoder)
            st.session_state.edit_mode = False
            st.experimental_rerun()

    if new_value == current_value and new_value == True:
        st.header(time_key)
        date_col, time_col = st.columns(2)
        if f"date_{time_key}" in time:
            with date_col:
                date_value = time[f"date_{time_key}"]
                st.subheader(date_value)
        if f"time_{time_key}" in time:
            with time_col:
                time_value = time[f"time_{time_key}"]
                st.subheader(time_value)

    elif new_value:
        project_data["editable_data"]["time"][time_key] = new_value
        date_col, time_col = st.columns(2)
        for key_type in ["date", "time"]:
            with (date_col if key_type == "date" else time_col):
                input_types = options_lists["input_types"]["time"].get(f"{key_type}_{time_key}")
                if input_types:
                    label = input_types.get("label")
                    description = input_types.get("description")
                current_value = time[f"{key_type}_{time_key}"]
                if current_value in ["today", "Today", "now", "Now", None, "null", "Null", "NULL", "none", "NoneType", "NoneType", False]:
                    current_value = datetime.datetime.today() if key_type == "date" else datetime.datetime.now()
                value = st.date_input(label, value=current_value, help=description, max_value=datetime.datetime.today()) if key_type == "date" else st.time_input(label, help=description)
                project_data["editable_data"]["time"][f"{key_type}_{time_key}"] = value

        if st.button("Save", key=f"{project_id}_{time_key}"):
            with open(f"{folder_path}/project_{project_id}.json", "w") as f:
                json.dump(project_data, f, indent=4, cls=CustomJSONEncoder)
            st.session_state.edit_mode = False
            st.experimental_rerun()

def handle_recurring_section(project_id, path, scheduling, options_lists, project_data):
    current_value = scheduling["is_recurring"]
    input_types = options_lists["input_types"].get("scheduling.is_recurring")
    if input_types:
        input_types_label = input_types.get("label")
        input_types_description = input_types.get("description")
        input_types_options = input_types.get("options")
    recurrence_input_types = options_lists["input_types"].get("scheduling.recurrence_pattern")
    if recurrence_input_types:
        recurrence_input_types_label = recurrence_input_types.get("label")
        recurrence_input_types_description = recurrence_input_types.get("description")
        recurrence_input_types_options = recurrence_input_types.get("options")

    new_value = st.checkbox(input_types_label, value=current_value, help=input_types_description)

    if new_value != current_value and new_value == False:
        st.subheader(f"Remove recurrence?")
        project_data["editable_data"]["scheduling"]["is_recurring"] = new_value
        project_data["editable_data"]["scheduling"]["recurrence_pattern"] = None
        if st.button("Save", key=f"{project_id}_remove_recurring"):
            with open(f"{path}/project_{project_id}.json", "w") as f:
                json.dump(project_data, f, indent=4, cls=CustomJSONEncoder)
            st.session_state.edit_mode = False
            st.experimental_rerun()

    if new_value != current_value and new_value == True:
        project_data["editable_data"]["scheduling"]["is_recurring"] = new_value
        if new_value:
            st.subheader("Recurrence pattern")
            input_types = options_lists["input_types"].get("scheduling.recurrence_pattern")
            if input_types:
                input_types_label = input_types.get("label")
                input_types_description = input_types.get("description")
            current_value = scheduling["recurrence_pattern"]
            formatted_input_types_options = formatted_options(current_value, recurrence_input_types_options)
            value = st.selectbox(recurrence_input_types_label, formatted_input_types_options, help=recurrence_input_types_description, key=f"{project_id}_scheduling_recurrence_pattern")
            project_data["editable_data"]["scheduling"]["recurrence_pattern"] = value
        else:
            project_data["editable_data"]["scheduling"]["recurrence_pattern"] = None

        if st.button("Save", key=f"{project_id}_recurring"):
            with open(f"{path}/project_{project_id}.json", "w") as f:
                json.dump(project_data, f, indent=4, cls=CustomJSONEncoder)
            st.session_state.edit_mode = False
            st.experimental_rerun()

    else:
        if new_value:
            st.header("Recurrence pattern")
            recurrence_pattern = scheduling["recurrence_pattern"]
            st.write(recurrence_pattern)

title_placeholder = st.empty()
date_modified_placeholder = st.empty()
date_created_placeholder = st.empty()
identifying_type_placeholder = st.empty()
folder_name_placeholder = st.empty()
folder_dir_placeholder = st.empty()
completed_placeholder = st.empty()
started_placeholder = st.empty()
due_placeholder = st.empty()
date_completed_placeholder = st.empty()
time_completed_placeholder = st.empty()
date_started_placeholder = st.empty()
time_started_placeholder = st.empty()
date_due_placeholder = st.empty()
time_due_placeholder = st.empty()
time_period_placeholder = st.empty()
time_estimate_placeholder = st.empty()
time_spent_placeholder = st.empty()
is_recurring_placeholder = st.empty()
recurrence_pattern_placeholder = st.empty()

def cancel_func():
    st.session_state.edit_mode = False
    st.session_state.edit_tab = None
    st.session_state.save_successful = False

def edit_mode(tab, project_data):
    st.session_state.edit_mode = True
    st.session_state.edit_tab = tab

def get_field_type(section_string, section_key, options_lists):
    section_dict = options_lists["input_types"].get(section_string)
    if section_dict:
        field_info = section_dict.get(section_key)
        if field_info:
            return field_info['type']
    return None

def save_btn_clicked(project_id, project_data, path, change_dict, options_lists):
    changes_made = False  # Flag to track whether any changes have been made
    original_identifying_type = project_data["editable_data"]["required"]["identifying_type"]
    original_title = project_data["editable_data"]["required"]["title"]
    for key, new_value in st.session_state.items():
        if key.startswith(f"{project_id}_"):
            split_key = key[len(project_id)+1:].split("_", 1)
            if len(split_key) < 2:
                continue
            section_string, section_key = split_key
            field_type = get_field_type(section_string, section_key, options_lists)
            if field_type is None:
                continue
            old_value = change_dict.get(key, {}).get('old_value')
            if field_type == "required":
                if new_value is not None and new_value.strip() and new_value != old_value:
                    project_data["editable_data"][section_string][section_key] = new_value
                    changes_made = True
            elif field_type == "self_made_list":
                if new_value != old_value:
                    project_data["editable_data"][section_string][section_key] = new_value
                    changes_made = True
            elif field_type == "self_made_list_comments":
                existing_comments = project_data["editable_data"][section_string][section_key]
                if not valid_value(existing_comments):
                    existing_comments = []
                existing_comments.append(new_value)
                project_data["editable_data"][section_string][section_key] = existing_comments
                changes_made = True
            elif field_type == "self_made_list_attachments":
                existing_attachments = project_data["editable_data"][section_string][section_key]
                if not valid_value(existing_attachments):
                    existing_attachments = []
                for uploaded_file_obj in new_value:
                    file_path = os.path.join(path, uploaded_file_obj.name)
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file_obj.getvalue())
                    existing_attachments.append(file_path)
                project_data["editable_data"][section_string][section_key] = existing_attachments
                changes_made = True
            else:
                if new_value != old_value:
                    project_data["editable_data"][section_string][section_key] = new_value
                    changes_made = True

    # Only update the file and session state if changes were made
    if changes_made:
        project_data["date_modified"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            # Check if the identifying_type or title has changed
            new_identifying_type = project_data["editable_data"]["required"]["identifying_type"]
            new_title = project_data["editable_data"]["required"]["title"]
            # Update CSV if identifying_type or title has changed
            if new_identifying_type != original_identifying_type or new_title != original_title:
                # Update identifying_type, title, and date_updated in CSV
                if os.path.isfile(productivity_csv_path):
                    productivity_csv = pd.read_csv(productivity_csv_path, index_col='id')
                    if project_id in productivity_csv.index:
                        if new_title != original_title:
                            productivity_csv.loc[project_id, 'title'] = new_title
                        if new_identifying_type != original_identifying_type:
                            productivity_csv.loc[project_id, 'identifying_type'] = new_identifying_type
                            new_path = f"{productivity_csv.loc[project_id, 'folder_dir']}/{(new_identifying_type).lower()}_{project_id}.json"
                            os.rename(path, new_path)
                            path = new_path
                        productivity_csv.loc[project_id, 'date_updated'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        productivity_csv.to_csv(productivity_csv_path)
            # Save the JSON
            with open(path, "w") as f:
                json.dump(project_data, f, indent=4, cls=CustomJSONEncoder)
            st.session_state.edit_mode = False
            st.session_state.edit_tab = None
            st.session_state.save_successful = "Saved successfully!"
            st.experimental_rerun()
        except Exception as e:
            print("Error occurred while saving to JSON: ", str(e))
    else:
        print("No changes made")

def edit_tab(tab_name, project_data, project_id, path):
    change_dict = {}
    for key, value in options_lists["input_types"].items():
        for k, v in value.items():
            if v['tab'] == tab_name:
                input_disabled = False
                if not valid_value(project_data['editable_data'][key][k]):
                    old_value = v.get("default")
                else:
                    old_value = project_data['editable_data'][key][k]
                if 'conditional' in v:
                    conditional = v['conditional'].split(".")
                    conditional_section = conditional[0]
                    conditional_field = conditional[1]
                    session_key = f"{project_id}_{conditional_section}_{conditional_field}"
                    if session_key not in st.session_state:
                        st.session_state[session_key] = project_data["editable_data"][conditional_section][conditional_field]
                    input_disabled = not st.session_state[session_key]
                input_key = f"{project_id}_{key}_{k}"
                if v['type'] == "text":
                    if k == "description":
                        new_value = st.text_area(v['label'], value=old_value, disabled=input_disabled, help=v['description'], key=input_key)
                    else:
                        new_value = st.text_input(v['label'], value=old_value, disabled=input_disabled, help=v['description'], key=input_key)
                elif v['type'] == "date":
                    if valid_value(old_value):
                        old_value = datetime.date.today()
                    new_value = st.date_input(v['label'], value=old_value, help=v['description'], disabled = input_disabled, key=input_key)
                elif v['type'] == "time":
                    if valid_value(old_value):
                        old_value = datetime.datetime.now()
                    new_value = st.time_input(v['label'], value=old_value, help=v['description'], disabled = input_disabled, key=input_key)
                elif v['type'] == "list":
                    formatted_input_types_options = formatted_options(old_value, v['options'])
                    new_value = st.selectbox(v['label'], formatted_input_types_options, help=v['description'], disabled = input_disabled, key=input_key)
                elif v['type'] == "boolean":
                    if valid_value(old_value):
                        old_value = False
                    if v == "completed":
                        handle_time_section(project_id, path, project_data["editable_data"]["time"], "completed", options_lists, project_data)
                    elif v == "started":
                        handle_time_section(project_id, path, project_data["editable_data"]["time"], "started", options_lists, project_data)
                    elif v == "due":
                        handle_time_section(project_id, path, project_data["editable_data"]["time"], "due", options_lists, project_data)
                    elif v == "is_recurring":
                        handle_recurring_section(project_id, path, project_data["editable_data"]["scheduling"], options_lists, project_data)
                    else:
                        new_value = st.checkbox(v['label'], value=old_value, help=v['description'], key=input_key)
                elif v['type'] == "currency":
                    if not valid_value(old_value):
                        old_value = 0
                    new_value = st.number_input(v['label'], value=old_value, help=v['description'], disabled = input_disabled, key=input_key)
                elif v['type'] == "self_made_list":
                    if not valid_value(old_value):
                        old_value = None
                    new_value = st.text_input(v['label'], value=old_value, help=v['description'], disabled = input_disabled, key=input_key)
                    if new_value:
                        new_value = new_value.split(', ')
                elif v['type'] == "percentage":
                    if not valid_value(old_value):
                        old_value = 0
                    new_value = st.slider(v['label'], min_value=0, max_value=100, value=old_value, help=v['description'], format="%i", disabled = input_disabled, key=input_key)
                elif v['type'] == "self_made_list_comments":
                    old_value = ""
                    new_value = st.text_area(v['label'], value=old_value, help=v['description'], disabled = input_disabled, key=input_key)
                    if new_value:
                        new_value = new_value.split('\n')
                elif v['type'] == "self_made_list_attachments":
                    # directly assign the list of UploadedFile objects to new_value
                    uploaded_files = st.file_uploader(v['label'], type=['png', 'jpg', 'jpeg', 'pdf', 'doc', 'docx', 'txt'], accept_multiple_files=True, help=v['description'], disabled = input_disabled, key=input_key)
                    new_value = []
                    for uploaded_file in uploaded_files:
                        st.write("filename:", uploaded_file.name)
                        new_value.append(uploaded_file)
                else:
                    new_value = None

                change_dict[input_key] = {'old_value': old_value, 'new_value': new_value}
    if st.button('Save'):
        save_btn_clicked(project_id, project_data, path, change_dict, options_lists)
    if st.button('Cancel'):
        cancel_func()
        st.experimental_rerun()



def get_data_from_id(id):
    productivity_csv = pd.read_csv(productivity_csv_path)
    # find id in the csv
    item_directory = None
    for _, row in productivity_csv.iterrows():
        if row["id"] == id:
            item_directory = str(row["folder_dir"]) + "/" + str(row["identifying_type"]) + "_" + str(row["id"]) + ".json"
            break
    return item_directory




def edit_items_item(selected_item, items_item):
    selected_item_id = selected_item["id"]
    items_item_id = items_item["id"]
    relationships_csv = "productivity/relationships.csv"
    # check if the selected item in the relationships csv
    try:
        df = pd.read_csv(relationships_csv)
    except pd.errors.EmptyDataError:
        df = pd.DataFrame(columns=['parent_id', 'parent_type', 'child_id', 'child_type'])
    if selected_item_id in df["parent_id"].values and items_item_id in df["child_id"].values:
        change_dict = {}
        for key, value in options_lists["input_types"].items():
            for k, v in value.items():
                input_disabled = False
                if not valid_value(items_item['editable_data'][key][k]):
                    old_value = v.get("default")
                else:
                    old_value = items_item['editable_data'][key][k]
                if 'conditional' in v:
                    conditional = v['conditional'].split(".")
                    conditional_section = conditional[0]
                    conditional_field = conditional[1]
                    session_key = f"{items_item}_{conditional_section}_{conditional_field}"
                    if session_key not in st.session_state:
                        st.session_state[session_key] = items_item["editable_data"][conditional_section][conditional_field]
                    input_disabled = not st.session_state[session_key]
                input_key = f"{items_item}_{key}_{k}"
                if v['type'] == "text":
                    if k == "description":
                        new_value = st.text_area(v['label'], value=old_value, disabled=input_disabled, help=v['description'], key=input_key)
                    else:
                        new_value = st.text_input(v['label'], value=old_value, disabled=input_disabled, help=v['description'], key=input_key)
                elif v['type'] == "date":
                    if valid_value(old_value):
                        old_value = datetime.date.today()
                    new_value = st.date_input(v['label'], value=old_value, help=v['description'], disabled = input_disabled, key=input_key)
                elif v['type'] == "time":
                    if valid_value(old_value):
                        old_value = datetime.datetime.now()
                    new_value = st.time_input(v['label'], value=old_value, help=v['description'], disabled = input_disabled, key=input_key)
                elif v['type'] == "list":
                    formatted_input_types_options = formatted_options(old_value, v['options'])
                    new_value = st.selectbox(v['label'], formatted_input_types_options, help=v['description'], disabled = input_disabled, key=input_key)
                elif v['type'] == "boolean":
                    if valid_value(old_value):
                        old_value = False
                    if v == "completed":
                        handle_time_section(items_item['id'], path, items_item["editable_data"]["time"], "completed", options_lists, items_item)
                    elif v == "started":
                        handle_time_section(items_item['id'], path, items_item["editable_data"]["time"], "started", options_lists, items_item)
                    elif v == "due":
                        handle_time_section(items_item['id'], path, items_item["editable_data"]["time"], "due", options_lists, items_item)
                    elif v == "is_recurring":
                        handle_recurring_section(items_item['id'], path, items_item["editable_data"]["scheduling"], options_lists, items_item)
                    else:
                        new_value = st.checkbox(v['label'], value=old_value, help=v['description'], key=input_key)
                elif v['type'] == "currency":
                    if not valid_value(old_value):
                        old_value = 0
                    new_value = st.number_input(v['label'], value=old_value, help=v['description'], disabled = input_disabled, key=input_key)
                elif v['type'] == "self_made_list":
                    if not valid_value(old_value):
                        old_value = None
                    new_value = st.text_input(v['label'], value=old_value, help=v['description'], disabled = input_disabled, key=input_key)
                    if new_value:
                        new_value = new_value.split(', ')
                elif v['type'] == "percentage":
                    if not valid_value(old_value):
                        old_value = 0
                    new_value = st.slider(v['label'], min_value=0, max_value=100, value=old_value, help=v['description'], format="%i", disabled = input_disabled, key=input_key)
                elif v['type'] == "self_made_list_comments":
                    old_value = ""
                    new_value = st.text_area(v['label'], value=old_value, help=v['description'], disabled = input_disabled, key=input_key)
                    if new_value:
                        new_value = new_value.split('\n')
                elif v['type'] == "self_made_list_attachments":
                    # directly assign the list of UploadedFile objects to new_value
                    uploaded_files = st.file_uploader(v['label'], type=['png', 'jpg', 'jpeg', 'pdf', 'doc', 'docx', 'txt'], accept_multiple_files=True, help=v['description'], disabled = input_disabled, key=input_key)
                    new_value = []
                    for uploaded_file in uploaded_files:
                        st.write("filename:", uploaded_file.name)
                        new_value.append(uploaded_file)
                else:
                    new_value = None
                change_dict[input_key] = {'old_value': old_value, 'new_value': new_value}
        if st.button('Save'):
            save_btn_clicked(items_item['id'], items_item, path, change_dict, options_lists)
        if st.button('Cancel'):
            cancel_func()
            st.experimental_rerun()


def create_new_items_item(button_pressed, folder_dir, item_type, project_id, parent_type):
    if button_pressed:
        st.session_state['folder_dir'] = folder_dir
        st.session_state['type'] = item_type
        st.session_state['is_parent'] = False
        st.session_state['parent_id'] = project_id
        st.session_state['parent_type'] = parent_type
        st.session_state['is_child'] = True
        st.session_state['child_id'] = None
        st.session_state['child_type'] = item_type.capitalize()
        st.session_state[f'create_new_{item_type}'] = True

        if st.session_state[f'create_new_{item_type}']:
            create_new_item(st.session_state.folder_dir, st.session_state.type, st.session_state.is_parent, st.session_state.parent_id, st.session_state.parent_type, st.session_state.is_child, st.session_state.child_id, st.session_state.child_type)


project_item_types = ["task", "deliverable", "milestone"]
goal_item_types = ["task", "habit", "milestone"]

def selected_project_tabs(path, project_data):
    if project_data is None or "id" not in project_data:
        print("Error: Invalid project_data")
        return
    project_id = project_data["id"]
    editable_data = project_data.get("editable_data", {})
    required = editable_data.get("required", {})
    time = editable_data.get("time", {})
    tools = editable_data.get("tools", {})
    descriptors = editable_data.get("descriptors", {})
    people = editable_data.get("people", {})
    progress = editable_data.get("progress", {})
    resources = editable_data.get("resources", {})
    notes = editable_data.get("notes", {})
    scheduling = editable_data.get("scheduling", {})


    title_placeholder.title(required.get("title", "Untitled Project"))
    identifying_type = required.get("identifying_type", "Project").capitalize()
    identifying_type_placeholder.write(identifying_type)

    basic_info_tab, time_tab, contraints_tab, tools_tab, resources_tab = st.tabs(["Basic Info", "Time Management", "Constraints", "Tools", "Resources"])

    

    with basic_info_tab:
        if st.session_state.edit_mode == True:
            if st.session_state.edit_tab == "basic info":
                title_placeholder.empty()
                identifying_type_placeholder.empty()
                edit_tab("basic info", project_data, project_id, path)
            else:
                st.write(f"To edit General Preferences please save or cancel the changes in {st.session_state.edit_tab} Preferences first.")
        else:
            if identifying_type == "Project":
                parent_type = "Project"
                st.write("It is a project")
                
                if "completed" in time:
                    handle_time_section(project_id, path, time, "completed", options_lists, project_data)
                if "completion_percentage" in progress:
                    completion_percentage = progress["completion_percentage"]
                    if not valid_value(completion_percentage):
                        pass
                    else:
                        if st.session_state.edit_mode == False:
                            progress_bar = st.progress(completion_percentage)
                            st.caption(f"{completion_percentage}% Complete")
                if "description" in descriptors:
                    description = descriptors["description"]
                    if not valid_value(description):
                        pass
                    else:
                        if st.session_state.edit_mode == False:
                            st.write(f"Description: {description}")

                st.button("Edit Basic Info", on_click=edit_mode, args=("basic info", project_data,))

                st.write("---")

                tasks_col, deliverable_col, milestone_col = st.columns(3)

                productivity_csv = pd.read_csv("productivity/productivity.csv")
                folder_dir = None
                productivity_csv = pd.read_csv("productivity/productivity.csv")
                folder_dir = None
                existing_items = {item_type: {} for item_type in project_item_types}
                for _, row in productivity_csv.iterrows():
                    if row["id"] == project_id:
                        folder_dir = row["folder_dir"]
                    for item_type in project_item_types:
                        if row["identifying_type"] == item_type:
                            item_title = row["title"]
                            item_id = row["id"]
                            existing_items[item_type][item_id] = item_title
                try:
                    relationships = pd.read_csv(relationships_csv)
                except:
                    print("Error: relationships.csv not found")
                    return
                
                columns = [tasks_col, deliverable_col, milestone_col]
                for col, item_type in zip(columns, project_item_types):
                    with col:
                        st.write(f"### {item_type.capitalize()}s")
                        items = relationships[(relationships["parent_id"] == project_id) & (relationships["child_type"] == item_type)]["child_id"].tolist()

                        for item in items:
                            item_data = get_data_from_id(item)
                            item_data = json.load(open(item_data))
                            item_title = item_data["editable_data"]["required"]["title"]
                            st.write(item_title)

                        add_item_btn = st.button(f"Add New {item_type.capitalize()}", key=f"{project_id}_add_{item_type}")
                    if add_item_btn:
                        create_new_items_item(add_item_btn, folder_dir, item_type, project_id, parent_type)
                        
                    

    
            elif identifying_type =="Goal":
                st.write("It's a Goal")

                st.write("---")

                tasks_col, habit_col, milestone_col = st.columns(3)

                productivity_csv = pd.read_csv("productivity/productivity.csv")
                folder_dir = None
                productivity_csv = pd.read_csv("productivity/productivity.csv")
                folder_dir = None
                existing_items = {item_type: {} for item_type in goal_item_types}
                for _, row in productivity_csv.iterrows():
                    if row["id"] == project_id:
                        folder_dir = row["folder_dir"]
                    for item_type in goal_item_types:
                        if row["identifying_type"] == item_type:
                            item_title = row["title"]
                            item_id = row["id"]
                            existing_items[item_type][item_id] = item_title
                try:
                    relationships = pd.read_csv(relationships_csv)
                except:
                    print("Error: relationships.csv not found")
                    return
                
                columns = [tasks_col, habit_col, milestone_col]
                for col, item_type in zip(columns, goal_item_types):
                    with col:
                        st.write(f"### {item_type.capitalize()}s")
                        items = relationships[(relationships["parent_id"] == project_id) & (relationships["child_type"] == item_type)]["child_id"].tolist()

                        for item in items:
                            item_data = get_data_from_id(item)
                            item_data = json.load(open(item_data))
                            item_title = item_data["editable_data"]["required"]["title"]
                            st.write(item_title)

                        add_item_btn = st.button(f"Add New {item_type.capitalize()}", key=f"{project_id}_add_{item_type}")
                    if add_item_btn:
                        create_new_items_item(add_item_btn, folder_dir, item_type, project_id, parent_type)
            elif identifying_type == "Task":
                st.write("It's a Task")

                st.write("---")
            

    with time_tab:
        if st.session_state.edit_mode == True:
            if st.session_state.edit_tab == "time management":
                edit_tab("time management", project_data, project_id, path)
            else:
                st.write(f"To edit Time Preferences please save or cancel the changes in {st.session_state.edit_tab} Preferences first.")
        else:
            st.button("Edit Time Management", on_click=edit_mode, args=("time management", project_data, ))

    with contraints_tab:
        if st.session_state.edit_mode == True:
            if st.session_state.edit_tab == "constraints":
               edit_tab("constraints", project_data, project_id, path)
            else:
                st.write(f"To edit Constraints please save or cancel the changes in {st.session_state.edit_tab} Preferences first.")
        else:
            st.button("Edit Constraints", on_click=edit_mode, args=("constraints", project_data, ))
    
    with tools_tab:
        if st.session_state.edit_mode == True:
            if st.session_state.edit_tab == "tools":
                edit_tab("tools", project_data, project_id, path)
            else:
                st.write(f"To edit Tools please save or cancel the changes in {st.session_state.edit_tab} Preferences first.")
        else:
            st.button("Edit Tools", on_click=edit_mode, args=("tools", project_data, ))

    with resources_tab:
        if st.session_state.edit_mode == True:
            if st.session_state.edit_tab == "resources":
                edit_tab("resources", project_data, project_id, path)
            else:
                st.write(f"To edit Resources please save or cancel the changes in {st.session_state.edit_tab} Preferences first.")
        else:
            st.button("Edit Resources", on_click=edit_mode, args=("resources", project_data, ))




def create_df_from_unique_types(productivity_csv_path, sort_by=None, ascending=True):
    # Get unique identifying types
    df = pd.read_csv(productivity_csv_path)
    unique_types = df['identifying_type'].unique()

    # Create dictionary to hold the dataframes
    dfs_dict = {}

    # Iterate through unique types
    for type in unique_types:
        # Create a dataframe for each type
        type_df = df[df['identifying_type'] == type]

        dfs_dict[f"{type}_df"] = type_df

    return dfs_dict

dfs_dict = create_df_from_unique_types(productivity_csv_path)

def select_folder_and_item():
    # User options for sorting
    sort_option_mapping = {
        'Date Created': 'date_created', 
        'Date Updated': 'date_updated', 
        'Most Recently Selected': 'most_recently_selected', 
        'Title': 'title'
    }
    default_sort_option = 'Most Recently Selected'


    if 'folder_df' in dfs_dict:
        # Create a selectbox for the folders
        folder_df = dfs_dict['folder_df']

        # User choice for sorting folders
        folder_sort_option = st.sidebar.selectbox("Sort folders by", list(sort_option_mapping.keys()), index=list(sort_option_mapping.keys()).index(default_sort_option))
        folder_df = folder_df.sort_values(by=sort_option_mapping[folder_sort_option], ascending=False)

        selected_folder = st.sidebar.selectbox("Choose a folder", folder_df['title'], index=0)
        selected_folder_id = folder_df[folder_df['title'] == selected_folder]['id'].values[0]


        # Filter the items based on the selected folder
        folder_dir = folder_df[folder_df['title'] == selected_folder]['folder_dir'].values[0]

        # Get all the items for the selected folder
        item_df_filtered = pd.concat([dfs_dict[df_key] for df_key in dfs_dict.keys() if df_key not in ['folder_df']])
        item_df_filtered = item_df_filtered[item_df_filtered['folder_dir'].str.startswith(folder_dir)]

        # Get the unique identifying types for the items in the selected folder
        unique_types = item_df_filtered['identifying_type'].unique()

        # Create a checkbox for each unique identifying type and store the checked types in a list
        checked_types = [item_type for index, item_type in enumerate(unique_types) if st.sidebar.checkbox(f"{(item_type).capitalize()}s", value=True, key=f"checkbox_{index}")]


        # Filter the items based on the checked checkboxes
        item_df_filtered = item_df_filtered[item_df_filtered['identifying_type'].isin(checked_types)]

        # User choice for sorting items
        item_sort_option = st.sidebar.selectbox("Sort items by", list(sort_option_mapping.keys()), index=list(sort_option_mapping.keys()).index(default_sort_option))
        item_df_filtered = item_df_filtered.sort_values(by=sort_option_mapping[item_sort_option], ascending=False)


        # Prepare dictionaries for mapping the "{identifying_type}_{id}" with "title" and its path
        item_mapping = {}
        path_mapping = {}
        for _, row in item_df_filtered.iterrows():
            item_key = f"{row['identifying_type']}_{row['id']}"
            item_mapping[item_key] = row['title']
            path_mapping[row['title']] = f"{row['folder_dir']}/{item_key}.json"

        # Create a selectbox for the items in the selected folder
        selected_item = st.sidebar.selectbox("Choose an item", list(item_mapping.values()), index=0) if item_mapping else None
        item_path = path_mapping[selected_item] if selected_item else None

        # update most recently selected
        if selected_item:
            # You need to find the row in the original DataFrame, not the filtered one
            original_df = pd.read_csv(productivity_csv_path)
            for key, title in item_mapping.items():
                if title == selected_item:
                    identifying_type, id = key.split('_', 1)
                    original_df.loc[(original_df['identifying_type'] == identifying_type) & (original_df['id'] == id), 'most_recently_selected'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            original_df.to_csv(productivity_csv_path, index=False)

        if selected_folder:
            original_df = pd.read_csv(productivity_csv_path)
            original_df.loc[(original_df['identifying_type'] == 'folder') & (original_df['id'] == selected_folder_id), 'most_recently_selected'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            original_df.to_csv(productivity_csv_path, index=False)


        return selected_folder, selected_item, item_path

           

if dfs_dict is None or len(dfs_dict) == 0:
    st.sidebar.write("No items available.")
    st.sidebar.write("Please create a folder to get started")
    st.stop()

selected_folder, selected_item, item_path = select_folder_and_item()

if "selected_folder" not in st.session_state:
    st.session_state.selected_folder = selected_folder
elif selected_folder != st.session_state.selected_folder:
    st.session_state.selected_folder = selected_folder

if "selected_item" not in st.session_state:
    st.session_state.selected_item = selected_item
elif selected_item != st.session_state.selected_item:
    st.session_state.selected_item = selected_item

if "item_path" not in st.session_state:
    st.session_state.item_path = item_path
elif item_path != st.session_state.item_path:
    st.session_state.item_path = item_path


path = item_path


items = ["Project", "Task", "Errand", "Deliverable", "Goal", "Habit", "Milestone", "Routine"]

if selected_folder and selected_item:
    if os.path.exists(path):
        try:
            with open(path, "r") as file:
                data = json.load(file)
                selected_project_tabs(path, data)
        except Exception as e:
            st.write("Error: ", str(e))
        item_directory_path = f"{directory_path}/{selected_folder}/json_data"
        if st.sidebar.button("Create New Project"):
            create_new_item(item_directory_path, "project")
        if st.sidebar.button("Create New Task"):
            create_new_item(item_directory_path, "task")
        if st.sidebar.button("Create New Errand"):
            create_new_item(item_directory_path, "errand")
        if st.sidebar.button("Create New Goal"):
            create_new_item(item_directory_path, "goal")
        if st.sidebar.button("Create New Routine"):
            create_new_item(item_directory_path, "routine")
            
