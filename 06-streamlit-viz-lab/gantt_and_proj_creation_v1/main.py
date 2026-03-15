import re
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
from datetime import time, date
#from gantt_chart_streamlit import create_gantt_chart
from pathlib import Path
import time


# make streamlit wide
st.set_page_config(layout="wide")


### CSS
css_file = Path("gantt_and_proj_creation_v1/custom.css").read_text()
st.markdown(f"<style>{css_file}</style>", unsafe_allow_html=True)
st.markdown("<div class='custom-text'>Hello, Streamlit with custom CSS!</div>", unsafe_allow_html=True)


# set directory
directory_path = "productivity"
if not os.path.exists(directory_path):
        os.makedirs(directory_path)


# load csv file
csv_path = f"{directory_path}/productivity.csv"

try:
    if os.stat(csv_path).st_size == 0:
        raise ValueError("Empty CSV file")
    productivity_csv = pd.read_csv(csv_path)
    # Remove rows corresponding to missing folders and update the CSV
    updated_productivity_csv = productivity_csv[productivity_csv["folder_dir"].apply(lambda x: os.path.exists(x))]
    if not updated_productivity_csv.empty:
        updated_productivity_csv.to_csv(os.path.join(directory_path, "productivity.csv"), index=False)
except (FileNotFoundError, ValueError):
    df = pd.DataFrame(columns=["id", "date_created", "date_updated", "folder_dir", "folder_name", "identifying_type", "title", "most_recently_selected"])
    df.to_csv(os.path.join(directory_path, "productivity.csv"), index=False)

def valid_value(value):
    return value not in [None, "None", "null", "Null", "NULL", "none", "NoneType", False, "", 0, []]




# Administrative functions
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.time):
            return obj.strftime("%H:%M:%S")
        elif isinstance(obj, date):
            return obj.isoformat()
        return super(CustomJSONEncoder, self).default(obj)
    

def conditional_date_input(label, checked, help=None):
    if checked:
        return st.date_input(label, help=help)
    else:
        st.write(label)
        return None
    
def formatted_options(old_value, options):
    sorted_options = sorted(options)
    if old_value in sorted_options:
        sorted_options.remove(old_value)
    return [old_value] + sorted_options


# Load Options Lists
with open("gantt_and_proj_creation_v1/options_lists.json", "r") as file:
    options_data = json.load(file)

options_lists = options_data




### Initialize session states
session_states = ["edit_mode", "edit_tab", "save_mode", "save_successful"]
for state in session_states:
    if state not in st.session_state:
        st.session_state[state] = False

if st.session_state.save_successful:
    if st.session_state.save_successful == True:
        st.session_state.save_successful = "Success!"
    st.success(st.session_state.save_successful)
    st.session_state.save_successful = False
    






def update_productivity_csv(data, directory_path):
    csv_path = os.path.join(directory_path, 'productivity.csv')
    data_df = pd.DataFrame([data]).set_index('id')

    if os.path.isfile(csv_path):
        # If the file already exists, load it and append the new data
        df = pd.read_csv(csv_path, index_col='id')
        df = pd.concat([df, data_df])
    else:
        # If the file does not exist, the new data is the entire dataframe
        df = data_df

    df.to_csv(csv_path)




# Create Project
def create_new_project(directory_path, folder_name, identifying_type):
    productivity_df = pd.read_csv(os.path.join(directory_path, 'productivity.csv'))
    project_count = len(productivity_df[(productivity_df['folder_name'] == folder_name) & (productivity_df['identifying_type'] == identifying_type)])

    title = f"{identifying_type}_{project_count + 1}"

    today = datetime.datetime.now()
    today = pd.to_datetime(today.strftime("%Y-%m-%d %H:%M:%S"))
    data = {
        "date_created": today.strftime("%Y-%m-%d %H:%M:%S"),
        "date_updated": today.strftime("%Y-%m-%d %H:%M:%S"),
        "folder_dir": os.path.join(directory_path, folder_name),
        "folder_name": folder_name,
        "identifying_type": identifying_type,
        "title": title,
        "id": None,
        "most_recently_selected": today
    }
    new_project = Project()
    new_project.edit_title_and_identifying_type(title, identifying_type)
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

    # Initialize editable_data with default values from OPTIONS_LIST.JSON
    for key, value in options_lists["input_types"].items():
        if key not in data_json["editable_data"]:
            data_json["editable_data"][key] = {}
        for k, v in value.items():
            if k not in data_json["editable_data"][key]:
                data_json["editable_data"][key][k] = v.get("default")

    safe_title = new_project.id.replace(" ", "_")
    data["id"] = safe_title
    update_productivity_csv(data, directory_path)

    folder_path = os.path.join(directory_path, folder_name, "json_data")
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    filename = os.path.join(folder_path, f"{identifying_type}_{safe_title}.json")
    with open(filename, "w") as f:
        json.dump(data_json, f, indent=4)
    success_txt = f"Folder '{folder_name}' with {identifying_type} '{title}' created."
    st.session_state.save_successful = success_txt
    st.experimental_rerun()


def create_new_folder(directory_path, folder_name):
    new_folder_path = os.path.join(directory_path, folder_name)
    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)
    create_new_project(directory_path, folder_name, "Project")



### get files in a folder
def get_files(path):
    return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]


# get folders in a directory
def get_folders(directory_path):
    return [f for f in os.listdir(directory_path) if os.path.isdir(os.path.join(directory_path, f))]

folders = get_folders(directory_path)

st.sidebar.write(folders)

# set up sidebar
folder_name = st.sidebar.text_input("Folder Name")
create_folder_button = st.sidebar.button("Create Folder")

productivity_csv = productivity_csv.sort_values(by=['most_recently_selected'], ascending=False)
folder_list = productivity_csv["folder_name"].values.tolist()
selected_folder = None

st.sidebar.write("folder_list: ", folder_list)

existing_folders = [folder for folder in folder_list if os.path.exists(f"{directory_path}/{folder}")]

if set(folder_list) != set(existing_folders):
    folder_list = existing_folders
    updated_productivity_csv = productivity_csv[productivity_csv["folder_name"].isin(folder_list)]
    updated_productivity_csv.to_csv(os.path.join(directory_path, "productivity.csv"), index=False)




### get most recently selected folder
if not productivity_csv.empty:
    productivity_csv = productivity_csv.sort_values(by=['most_recently_selected'], ascending=False)
    # get the most recently selected folder
    most_recently_selected_folder = productivity_csv.loc[0, 'folder_name']

    productivity_csv['most_recently_selected'] = pd.to_datetime(productivity_csv['most_recently_selected'])
    most_recent_row = productivity_csv['most_recently_selected'].idxmax()
    most_recently_selected_folder = productivity_csv.loc[most_recent_row, 'folder_name']
else:
    most_recently_selected_folder = None


selected_folder = most_recently_selected_folder





### create new folder
if create_folder_button:
    if folder_name:
        folder_created = create_new_folder(directory_path, folder_name)
        if folder_created:
            selected_folder = folder_name
            files = get_files(directory_path)
            productivity_csv = pd.read_csv(f"{directory_path}/productivity.csv")
            folder_list = productivity_csv["folder_name"].values.tolist()
            st.experimental_rerun()
    else:
        st.sidebar.warning("Please enter a folder name.")

### select folder








# add to existing folder
def save_comment_to_md_file(selected_folder, comment, project_id):
    directory = f"{directory_path}/{selected_folder}/comments/{project_id}"
    if not os.path.exists(directory):
        os.makedirs(directory)

    comment_id = str(uuid.uuid4())
    md_file_path = f"{directory}/{comment_id}.md"

    with open(md_file_path, "w") as f:
        f.write(comment)

    return md_file_path



def add_comment_to_project(projects, selected_folder, project_id, comment):
    md_file_path = save_comment_to_md_file(selected_folder, comment, project_id)

    for project in projects:
        if project["id"] == project_id:
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

    if new_value != current_value and new_value == False:
        st.subheader(f"Remove {time_key} date?")
        project_data["editable_data"]["time"][time_key] = new_value
        project_data["editable_data"]["time"][f"date_{time_key}"] = None
        project_data["editable_data"]["time"][f"time_{time_key}"] = None
        if st.button("Save", key=f"{project_id}_{time_key}_save"): # appended '_save'
            with open(f"{path}/project_{project_id}.json", "w") as f:
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
            with open(f"{path}/project_{project_id}.json", "w") as f:
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
                if os.path.isfile(csv_path):
                    productivity_csv = pd.read_csv(csv_path, index_col='id')
                    if project_id in productivity_csv.index:
                        if new_identifying_type != original_identifying_type:
                            productivity_csv.loc[project_id, 'identifying_type'] = new_identifying_type
                            productivity_csv.loc[project_id, 'title'] = new_title
                        productivity_csv.loc[project_id, 'date_updated'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        productivity_csv.to_csv(csv_path)

                            # Rename the file if identifying_type has changed
                if new_identifying_type != original_identifying_type:
                    os.rename(f"{path}/{original_identifying_type}_{project_id}.json", f"{path}/{new_identifying_type}_{project_id}.json")

            # Save the JSON
            with open(f"{path}/{new_identifying_type}_{project_id}.json", "w") as f:
                json.dump(project_data, f, indent=4, cls=CustomJSONEncoder)
            st.session_state.edit_mode = False
            st.session_state.edit_tab = None
            st.session_state.save_successful = True
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
                    print("old_value: ", old_value)
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




def selected_project_tabs(path, project_data):
    if project_data is None or "id" not in project_data:
        print("Error: Invalid project_data")
        return
    project_id = project_data["id"]
    # rest of your code
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
    identifying_type_placeholder.write(required.get("identifying_type", "Project"))

    general_tab, time_tab, contraints_tab, tools_tab, resources_tab = st.tabs(["General", "Time", "Constraints", "Tools", "Resources"])

    with general_tab:
        if st.session_state.edit_mode == True:
            if st.session_state.edit_tab == "general":
                title_placeholder.empty()
                identifying_type_placeholder.empty()

                edit_tab("general", project_data, project_id, path)
                
            else:
                st.write(f"To edit General Preferences please save or cancel the changes in {st.session_state.edit_tab} Preferences first.")
        else:
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




            st.button("Edit General", on_click=edit_mode, args=("general", project_data,))

    with time_tab:
        if st.session_state.edit_mode == True:
            if st.session_state.edit_tab == "time":
                edit_tab("time", project_data, project_id, path)
            else:
                st.write(f"To edit Time Preferences please save or cancel the changes in {st.session_state.edit_tab} Preferences first.")
        else:
            st.button("Edit Time", on_click=edit_mode, args=("time", project_data, ))

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




def selected_task_tabs(path, task_data):
    st.write("Task Data: ", task_data)




















if selected_folder:
    st.sidebar.title("Select Folder")
    selected_folder = st.sidebar.selectbox("Choose a folder", folder_list, index=folder_list.index(selected_folder) if selected_folder else 0)

    if selected_folder:
        st.sidebar.write(f"Selected folder: {selected_folder}")
        path = f"{directory_path}/{selected_folder}/json_data"

        df = pd.read_csv(csv_path)

        # Filter DataFrame to only include rows for the current folder
        df = df[df['folder_name'] == selected_folder]

        # Separate DataFrame into tasks and projects based on 'identifying_type' and sort by 'most_recently_selected' column
        task_df = df[df['identifying_type'] == 'Task']
        task_df = task_df.sort_values(by=['most_recently_selected'], ascending=False)

        project_df = df[df['identifying_type'] == 'Project']
        project_df = project_df.sort_values(by=['most_recently_selected'], ascending=False)

        tasks_and_projects_df = pd.concat([task_df, project_df])
        tasks_and_projects_df = tasks_and_projects_df.sort_values(by=['most_recently_selected'], ascending=False)

        # filter selectbox by checkbox buttons that filter by tasks and projects
        if task_df.empty:
            show_tasks = st.sidebar.checkbox("Show Tasks", value=False, disabled=True)
        else:
            show_tasks = st.sidebar.checkbox("Show Tasks", value=True, disabled=False)

        if project_df.empty:
            show_projects = st.sidebar.checkbox("Show Projects", value=False, disabled=True)
        else:
            show_projects = st.sidebar.checkbox("Show Projects", value=True, disabled=False)

        selected_item = None
        selected_item_id = None

        if show_tasks and show_projects:
            pass
        elif show_tasks:
            project_df = pd.DataFrame()
            if not task_df.empty:
                st.sidebar.title("Select Task")
                selected_item = st.sidebar.selectbox("Choose a Task", task_df['title'].tolist())
                selected_item_id = task_df.loc[task_df['title'] == selected_item, 'id'].values[0]
        elif show_projects:
            project_df = pd.DataFrame()
            if not project_df.empty:
                st.sidebar.title("Select Project")
                selected_item = st.sidebar.selectbox("Choose a Task", project_df['title'].tolist())
                selected_item_id = project_df.loc[project_df['title'] == selected_item, 'id'].values[0]
        else:
            task_df = pd.DataFrame()
            project_df = pd.DataFrame()
            

        if not tasks_and_projects_df.empty:
            st.sidebar.title("Select Item")
            selected_item = st.sidebar.selectbox("Choose an Item", tasks_and_projects_df['title'].tolist())
            selected_item_id = tasks_and_projects_df.loc[tasks_and_projects_df['title'] == selected_item, 'id'].values[0]

        for item in os.listdir(path):
            if item.endswith(".json"):
                json_file_path = os.path.join(path, item)
                try:
                    with open(json_file_path, "r") as file:
                        data = json.load(file)

                    if selected_item and item == f"Task_{selected_item_id}.json":
                        selected_task_tabs(path, data)
                        # update the 'most_recently_selected' column in the CSV
                        df.loc[df['id'] == data['id'], 'most_recently_selected'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        df.to_csv(csv_path)
                    if selected_item and item == f"Project_{selected_item_id}.json":
                        selected_project_tabs(path, data)
                        # update the 'most_recently_selected' column in the CSV
                        df.loc[df['id'] == data['id'], 'most_recently_selected'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        df.to_csv(csv_path)

                except json.JSONDecodeError as e:
                    st.error(f"Error loading JSON data from file '{json_file_path}': {e}")

        st.sidebar.title("Create New Item")
        if st.sidebar.button("Create New Project"):
            create_new_project(directory_path, selected_folder, "Project")
        if st.sidebar.button("Create New Task"):
            create_new_project(directory_path, selected_folder, "Task")

