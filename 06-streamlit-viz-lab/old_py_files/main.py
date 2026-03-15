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
from updates_to_csv import update_productivity_csv
#from gantt_chart_streamlit import create_gantt_chart
from pathlib import Path
import time

# make streamlit wide
st.set_page_config(layout="wide")

### options lists 
with open("gantt_and_proj_creation_v1/options_lists.json", "r") as file:
    options_data = json.load(file)

options_lists = options_data

st.session_state

# Read the content of the CSS file
css_file = Path("gantt_and_proj_creation_v1/custom.css").read_text()

st.markdown(f"<style>{css_file}</style>", unsafe_allow_html=True)

st.markdown("<div class='custom-text'>Hello, Streamlit with custom CSS!</div>", unsafe_allow_html=True)


directory_path = "productivity"
if not os.path.exists(directory_path):
        os.makedirs(directory_path)

csv_path = f"{directory_path}/productivity.csv"


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, time):
            return obj.strftime("%H:%M:%S")
        elif isinstance(obj, date):
            return obj.isoformat()
        return super(CustomJSONEncoder, self).default(obj)

### create csv if it doesn't exist
try:
    if os.stat(csv_path).st_size == 0:
        raise ValueError("Empty CSV file")
    productivity_csv = pd.read_csv(csv_path)
    # Remove rows corresponding to missing folders and update the CSV
    updated_productivity_csv = productivity_csv[productivity_csv["folder_dir"].apply(lambda x: os.path.exists(x))]
    if not updated_productivity_csv.empty:
        updated_productivity_csv.to_csv(os.path.join(directory_path, "productivity.csv"), index=False)
except (FileNotFoundError, ValueError):
    df = pd.DataFrame(columns=["date_created", "date_updated", "folder_dir", "folder_name", "project_title", "project_id", "has_project", "most_recently_selected"])
    df.to_csv(os.path.join(directory_path, "productivity.csv"), index=False)

def valid_value(value):
    return value not in [None, "None", "null", "Null", "NULL", "none", "NoneType", False, "", 0, []]



### create new project
def create_new_project(directory_path, folder_name, title=None):
    if title is None:
        title = folder_name
    new_folder_path = os.path.join(directory_path, folder_name)
    try:
        os.makedirs(new_folder_path)
        today = datetime.datetime.now()
        data = {
            "date_created": today.strftime("%Y-%m-%d %H:%M:%S"),
            "date_updated": today.strftime("%Y-%m-%d %H:%M:%S"),
            "folder_dir": os.path.join(directory_path, folder_name),
            "folder_name": folder_name,
            "project_title": title,
            "project_id": None,
            "has_project": True,
            "most_recently_selected": True
        }
        new_project = Project()
        new_project.edit_title_and_identifying_type(title, "Project")
        print(new_project.editable_data)
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
            main_key, inner_key = key.split(".")
            if main_key not in data_json["editable_data"]:
                data_json["editable_data"][main_key] = {}
            
            # Only set the default value if the key does not already exist in new_project.editable_data
            if inner_key not in data_json["editable_data"][main_key]:
                data_json["editable_data"][main_key][inner_key] = value.get("default")


        safe_title = new_project.id.replace(" ", "_")
        data["project_id"] = safe_title
        update_productivity_csv(data, directory_path)
        
        folder_path = os.path.join(directory_path, folder_name, "json_data")
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        filename = os.path.join(folder_path, f"project_{safe_title}.json")
        with open(filename, "w") as f:
            json.dump(data_json, f, indent=4)

        st.success(f"Folder '{folder_name}' with project '{title}' created.")
        return True
    except FileExistsError:
        st.warning(f"Folder '{folder_name}' already exists. Please change the name.")
        return False
    except Exception as e:
        st.error(f"Error creating folder '{folder_name}': {e}")
        return False




### get files in a folder
def get_files(path):
    return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

folder_name = st.sidebar.text_input("Folder Name")
create_button = st.sidebar.button("Create Folder")


### create folder
productivity_csv = pd.read_csv(f"{directory_path}/productivity.csv")
folder_list = productivity_csv["folder_name"].values.tolist()
selected_folder = None


### get existing folders
existing_folders = [folder for folder in folder_list if os.path.exists(f"{directory_path}/{folder}")]

if set(folder_list) != set(existing_folders):
    folder_list = existing_folders
    updated_productivity_csv = productivity_csv[productivity_csv["folder_name"].isin(folder_list)]
    updated_productivity_csv.to_csv(os.path.join(directory_path, "productivity.csv"), index=False)



### get most recently selected folder
most_recently_selected_folder = productivity_csv[productivity_csv["most_recently_selected"]].iloc[0]["folder_name"] if not productivity_csv[productivity_csv["most_recently_selected"]].empty else None
selected_folder = most_recently_selected_folder

### create new folder
if create_button:
    if folder_name:
        folder_created = create_new_project(directory_path, folder_name)
        if folder_created:
            selected_folder = folder_name
            files = get_files(directory_path)
            productivity_csv = pd.read_csv(f"{directory_path}/productivity.csv")
            folder_list = productivity_csv["folder_name"].values.tolist()
            st.experimental_rerun()
    else:
        st.sidebar.warning("Please enter a folder name.")


### select folder
if folder_list:
    st.sidebar.title("Select Folder")
    selected_folder = st.sidebar.selectbox("Choose a folder", folder_list, index=folder_list.index(selected_folder) if selected_folder else 0)





def conditional_date_input(label, checked, help=None):
    if checked:
        return st.date_input(label, help=help)
    else:
        st.write(label)
        return None


### create new project
def save_comment_to_md_file(selected_folder, comment, project_id):
    directory = f"{directory_path}/{selected_folder}/comments/{project_id}"
    if not os.path.exists(directory):
        os.makedirs(directory)

    comment_id = str(uuid.uuid4())
    md_file_path = f"{directory}/{comment_id}.md"

    with open(md_file_path, "w") as f:
        f.write(comment)

    return md_file_path


### add comment to project
def add_comment_to_project(projects, selected_folder, project_id, comment):
    md_file_path = save_comment_to_md_file(selected_folder, comment, project_id)

    for project in projects:
        if project["id"] == project_id:
            if "comments" not in project["notes"]:
                project["notes"]["comments"] = []
            project["notes"]["comments"].append({"id": str(uuid.uuid4()), "path": md_file_path})

    return projects






def formatted_options(old_value, options):
    sorted_options = sorted(options)
    if old_value in sorted_options:
        sorted_options.remove(old_value)
    return [old_value] + sorted_options


def save_btn_clicked(project_id, project_data, path):
    st.session_state.edit_mode = False
    for key, new_value in st.session_state.items():
        if key.startswith(f"{project_id}_"):
            split_key = key[len(project_id)+1:].split(".", 1)
            if len(split_key) < 2:
                continue
            section_string, section_key = split_key
            section_name = project_data["editable_data"].get(section_string)
            if section_name == "required":
                if new_value.strip():
                    section_name[section_key] = new_value
                    project_data["date_modified"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    with open(f"{path}/project_{project_id}.json", "w") as f:
                        json.dump(project_data, f, indent=4, cls=CustomJSONEncoder)
                    st.session_state.edit_mode = False
                else:
                    st.warning(f"{section_key} cannot be empty")  # Display warning message if the text is empty

            else:
                if section_name == "self_made_list":
                    project_data["editable_data"][section_string][section_key] = new_value
                elif section_name == "text_markdown":
                    if section_key == "notes.comments":
                        projects = [project_data] 
                        projects = add_comment_to_project(projects, selected_folder, project_id, new_value)
                        project_data = projects[0]
                    else:
                        markdown_file_path = os.path.join(json_file_path, f"{section_key}.md")
                        with open(markdown_file_path, "w") as f:
                            f.write(new_value)
                        project_data["editable_data"][section_string][section_key] = markdown_file_path
                elif section_name == "self_made_list_file":
                    saved_paths = []
                    for uploaded_file in new_value:
                        file_path = os.path.join(path, uploaded_file.name)
                        with open(file_path, "wb") as f:
                            f.write(uploaded_file.getvalue())
                        saved_paths.append(file_path)
                    project_data["editable_data"][section_string][section_key] = saved_paths
                section_name[section_key] = new_value
                project_data["date_modified"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                with open(f"{path}/project_{project_id}.json", "w") as f:
                    json.dump(project_data, f, indent=4, cls=CustomJSONEncoder)
    st.experimental_rerun()


def editable_field(tab_name, form, section_name, section_string, section_key, old_value, path, project_id, project_data):
    if st.session_state.edit_mode:
        with form:
            input_types = options_lists["input_types"].get(section_string + str(section_key))
            if input_types:
                input_types_type = input_types.get("type")
                input_types_label = input_types.get("label")
                input_types_description = input_types.get("description")
                input_types_options = input_types.get("options")
                input_types_default = input_types.get("default")
                input_types_conditional = input_types.get("conditional")
                input_types_tab = input_types.get("tab")

                if input_types_tab == tab_name:
                    if old_value == "":
                        if input_types_default:
                            old_value = input_types_default
                        else:
                            old_value = None
                    if input_types_type:
                        input_disabled = False
                        if input_types_conditional:
                            conditional = input_types_conditional.split(".")
                            conditional_section = conditional[0]
                            conditional_field = conditional[1]
                            session_key = f"{project_id}_{conditional_section}_{conditional_field}"
                            if session_key not in st.session_state:
                                st.session_state[session_key] = project_data["editable_data"][conditional_section][conditional_field]
                            input_disabled = not st.session_state[session_key]
                        if input_types_type == "text":
                            if section_key == "description":
                                new_value = st.text_area(input_types_label, value=old_value, help=input_types_description, disabled = input_disabled, key=f"{project_id}_{section_string}{section_key}")
                            else:
                                new_value = st.text_input(input_types_label, value=old_value, help=input_types_description, disabled = input_disabled, key=f"{project_id}_{section_string}{section_key}")
                        
                        elif input_types_type == "date":
                            if old_value == "today" or old_value == "Today" or old_value == None:
                                old_value = datetime.date.today()
                            new_value = st.date_input(input_types_label, value=old_value, help=input_types_description, disabled = input_disabled, key=f"{project_id}_{section_string}{section_key}")
                        elif input_types_type == "time":
                            if old_value == "now" or old_value == "Now" or old_value == None:
                                old_value = datetime.datetime.now()
                            new_value = st.time_input(input_types_label, value=old_value, help=input_types_description, disabled = input_disabled, key=f"{project_id}_{section_string}{section_key}")
                        elif input_types_type == "list":
                            formatted_input_types_options = formatted_options(old_value, input_types_options)
                            new_value = st.selectbox(input_types_label, formatted_input_types_options, help=input_types_description, disabled = input_disabled, key=f"{project_id}_{section_string}{section_key}")
                        elif input_types_type == "boolean":
                            new_value = st.checkbox(input_types_label, value=old_value, help=input_types_description, key=f"{project_id}_{section_string}{section_key}")
                        elif input_types_type == "currency":
                            new_value = st.number_input(input_types_label, value=old_value, help=input_types_description, disabled = input_disabled, key=f"{project_id}_{section_string}{section_key}")
                        elif input_types_type == "self_made_list":
                            new_value = st.text_input(input_types_label, value=old_value, help=input_types_description, disabled = input_disabled, key=f"{project_id}_{section_string}{section_key}")
                            if new_value:
                                new_value = new_value.split(', ')
                        elif input_types_type == "percentage":
                            if old_value == None:
                                old_value = 0
                            new_value = st.slider(input_types_label, min_value=0, max_value=100, value=old_value, help=input_types_description, format="%i", disabled = input_disabled, key=f"{project_id}_{section_string}{section_key}")
                        elif input_types_type == "text_markdown":
                            new_value = st.text_area(input_types_label, value=old_value, help=input_types_description, disabled = input_disabled, key=f"{project_id}_{section_string}{section_key}")
                        elif input_types_type == "self_made_list_file":
                            new_value = st.file_uploader(input_types_label, type=['png', 'jpg', 'jpeg', 'pdf', 'doc', 'docx', 'txt'], accept_multiple_files=True, help=input_types_description, disabled = input_disabled, key=f"{project_id}_{section_string}{section_key}")
                            if new_value:
                                new_value = [uploaded_file.name for uploaded_file in new_value]
                        else:
                            new_value = None
                        #if value is not None and input_type not in ["self_made_list", "text_markdown", "self_made_list_file"]:
                            #data["editable_data"][section][field] = value


    else:
        if old_value == "" or old_value == "None" or old_value == None or old_value == "null" or old_value == "Null" or old_value == "NULL" or old_value == "none" or old_value == "NoneType" or old_value == "NoneType" or old_value == False:
            pass


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
    input_types = options_lists["input_types"].get(f"time.{time_key}")
    if input_types:
        input_types_label = input_types.get("label")
        input_types_description = input_types.get("description")

    new_value = st.checkbox(input_types_label, value=current_value, help=input_types_description)

    if new_value != current_value and new_value == False:
        st.subheader(f"Remove {time_key} date?")
        project_data["editable_data"]["time"][time_key] = new_value
        project_data["editable_data"]["time"][f"date_{time_key}"] = None
        project_data["editable_data"]["time"][f"time_{time_key}"] = None
        if st.button("Save", key=f"{project_id}_{time_key}"):
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
                input_types = options_lists["input_types"].get(f"time.{key_type}_{time_key}")
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


def edit_tab(tab, project_id, path, project_data):
    st.session_state.edit_mode = tab
    st.write(f"Editing {tab} tab")



def selected_folder_tabs(path, project_data):
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

    if "edit_mode" not in st.session_state:
        st.session_state.edit_mode = False

    if "form" not in st.session_state:
        st.session_state.form = None


    if "title" in required:
        project_title = required["title"]
        if st.session_state.edit_mode == False:
            st.title(project_title)
        if general_form:
            form = general_form
            editable_field(form, required,"required.", "title", project_title, path, project_id, project_data)
    if "identifying_type" in required:
        identifying_type = required["identifying_type"]
        if st.session_state.edit_mode == False:
            st.subheader(identifying_type)
        if general_form:
            form = general_form
            editable_field(form, required,"required.", "identifying_type", identifying_type, path, project_id, project_data)

    general_tab, time_preferences_tab, tasks_tab, extras_tab, organize_stuff = st.tabs(["General", "Time Preferences", "Tasks", "Extras", "Organize Stuff"])
    
    with general_tab:
        
        if "completion_percentage" in progress:
            completion_percentage = progress["completion_percentage"]
        
            if completion_percentage == "None" or completion_percentage == None or completion_percentage == "null" or completion_percentage == "Null" or completion_percentage == "NULL" or completion_percentage == "none" or completion_percentage == "NoneType" or completion_percentage == "NoneType" or completion_percentage == False or completion_percentage == "" or completion_percentage == 0:
                pass
            else:
                if st.session_state.edit_mode == False:
                    progress_bar = st.progress(completion_percentage)
                    st.caption(f"{completion_percentage}% Complete")

        if "description" in descriptors:
            description = descriptors["description"]
            if valid_value(description):
                if st.session_state.edit_mode == False:
                    st.write(description)
            if general_form:
                form = general_form
                editable_field(form, descriptors, "descriptors.","description", description, path, project_id, project_data)

        if "category" in descriptors:
            category = descriptors["category"]
            if valid_value(category):
                if st.session_state.edit_mode == False:
                    st.write(f"Category: {category}")
                    st.markdown('<p class="custom-weight">Hello World !!</p>', unsafe_allow_html=True)
            if general_form:
                form = general_form
                editable_field(form, descriptors, "descriptors.","category", category, path, project_id, project_data)


        if "goal_verb" in descriptors:
            goal_verb = descriptors["goal_verb"]
            if valid_value(goal_verb):
                if st.session_state.edit_mode == False:
                    st.write(goal_verb)
            if general_form:
                form = general_form
                editable_field(form, descriptors, "descriptors.","goal_verb", goal_verb, path, project_id, project_data)

        if "genre" in descriptors:
            genre = descriptors["genre"]
            if valid_value(genre):
                if st.session_state.edit_mode == False:
                    st.write(genre)
            if general_form:
                form = general_form
                editable_field(form, descriptors, "descriptors.","genre", genre, path, project_id, project_data)
            
        if "priority" in descriptors:
            priority = descriptors["priority"]
            if valid_value(priority):
                if st.session_state.edit_mode == False:
                    st.write("Priority: ")
                    st.write(priority)
            if general_form:
                form = general_form
                editable_field(form, descriptors, "descriptors.","priority", priority, path, project_id, project_data)
           
        if "use_case" in descriptors:
            use_case = descriptors["use_case"]
            if valid_value(use_case):
                if st.session_state.edit_mode == False:
                    st.write("Use case: ")
                    st.write(use_case)
            if general_form:
                form = general_form
                editable_field(form, descriptors, "descriptors.","use_case", use_case, path, project_id, project_data)
            
        if "milestones" in progress:
            milestones = progress["milestones"]
            if valid_value(milestones):
                if st.session_state.edit_mode == False:
                    st.write("Milestones: ")
                    st.write(milestones)
            if general_form:
                form = general_form
                editable_field(form, progress, "progress.","milestones", milestones, path, project_id, project_data)
            
        if "status" in progress:
            status = progress["status"]
            if valid_value(status):
                if st.session_state.edit_mode == False:
                    st.write("Status: ")
                    st.write(status)
            if general_form:
                form = general_form
                editable_field(form, progress, "progress.","status", status, path, project_id, project_data)

        if st.session_state.edit_mode == False:
            if "completed" in time:
                handle_time_section(project_id, path, time, "completed", options_lists, project_data)
            

        if "completion_percentage" in progress:
            completion_percentage = progress["completion_percentage"]
            if general_form:
                form = general_form
                editable_field(form, progress, "progress.","completion_percentage", completion_percentage, path, project_id, project_data)

        if st.session_state.edit_mode == False:
            if st.button("Edit", key=f"{project_id}_general_edit"):
                st.session_state.edit_mode = True
                st.session_state.edit_general = True
                st.experimental_rerun()

            

    with time_preferences_tab:
        if "due" in time:
            handle_time_section(project_id, path, time, "due", options_lists, project_data)
        if "started" in time:
            handle_time_section(project_id, path, time, "started", options_lists, project_data)

        if "time_period" in time:
            time_period = time["time_period"]
            if valid_value(time_period):
                if st.session_state.edit_mode == False:
                    st.write("Time period")
                    st.write(time_period)
                if time_form:
                    form = time_form
                    editable_field(form, time, "time.","time_period", time_period, path, project_id, project_data)

        if "time_estimate" in time:
            time_estimate = time["time_estimate"]
            handle_time_intervals(project_id, path, time, "time_estimate", time_estimate, project_data)

        if "time_spent" in time:
            time_spent = time["time_spent"]
            if valid_value(time_spent):
                if st.session_state.edit_mode == False:
                    st.write("Time spent")
                    st.write(time_spent)
                if time_form:
                    form = time_form
                    editable_field(form, time, "time.","time_spent", time_spent, path, project_id, project_data)
        
        handle_recurring_section(project_id, path, scheduling, options_lists, project_data)

        st.button("Edit Time Preferences", key=f"{project_id}_time_edit", on_click=edit_tab, args=("time", project_id, path, project_data))


        if st.session_state.edit_mode == False:
            if st.button("Edit", key=f"{project_id}_time_edit"):
                st.session_state.edit_mode = True
                st.session_state.edit_time = True
                st.experimental_rerun()
        
    if save_button:
        save_btn_clicked(project_id, project_data, path)
    elif cancel_button:
        st.session_state.edit_mode = False
        st.experimental_rerun()





### get project data
if selected_folder:
    st.sidebar.write(f"Selected folder: {selected_folder}")
    path = f"{directory_path}/{selected_folder}/json_data"
    for item in os.listdir(path):
        if item.endswith(".json"):
            json_file_path = os.path.join(path, item)
            try:
                with open(json_file_path, "r") as file:
                    project_data = json.load(file)
            except json.JSONDecodeError as e:
                st.error(f"Error loading JSON data from file '{json_file_path}': {e}")
                project_data = None

    selected_folder_tabs(path, project_data)