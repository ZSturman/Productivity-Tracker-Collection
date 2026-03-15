import streamlit as st
import os
import pandas as pd
import json
import uuid
from datetime import date, datetime, time
import plotly.figure_factory as ff
from app.csv_creation import create_csvs
from app.administrative import make_safe, valid_value, formatted_options, CustomJSONEncoder, make_sure_items_are_in_csv
from app.json_data import new_project_json_template, new_deliverable_json_template, new_milestone_json_template



# make streamlit wide
st.set_page_config(layout="wide")

session_states = ["save_successful", "selected_folder", "new_project_creation", "selected_project"]

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
    st.session_state.new_project_creation = False


directory_path = "productivity"
if not os.path.exists(directory_path):
    os.makedirs(directory_path)

csv_folder = "csvs"
if not os.path.exists(os.path.join(directory_path, csv_folder)):
    os.makedirs(os.path.join(directory_path, csv_folder))

productivity_csv_path, relationships_csv_path, timeline_csv_path  = create_csvs(directory_path, csv_folder)
productivity_csv = pd.read_csv(productivity_csv_path)
relationships_csv = pd.read_csv(relationships_csv_path)
timeline_csv = pd.read_csv(timeline_csv_path)

csv_folder_path = os.path.join(directory_path, csv_folder)

# add csvs to productivity_csv
if csv_folder_path not in productivity_csv["folder_dir"].values:
    new_csv = pd.DataFrame({"id": make_safe(), "date_created": [pd.Timestamp.now()], "date_updated": [pd.Timestamp.now()], "folder_dir": [csv_folder_path], "identifying_type": ["administrative"], "title": [csv_folder], "most_recently_selected": "None"})
    new_csv.to_csv(productivity_csv_path, mode="a", header=False, index=False)
    st.experimental_rerun()

# Load Options Lists
with open("app/options_lists.json", "r") as file:
    options_data = json.load(file)

options_lists = options_data



selected_folder = None

# Create a list of all the folders in the directory
folders = [folder for folder in os.listdir(directory_path) if os.path.isdir(os.path.join(directory_path, folder))]
# Create a list of all the files in the directory
files = [file for file in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, file))]

make_sure_items_are_in_csv(directory_path, productivity_csv, productivity_csv_path, timeline_csv, timeline_csv_path, folders)









try:
    # filter the productivity_csv to only show folders
    folder_options = productivity_csv[productivity_csv["identifying_type"] == "folder"]
    # sort the folders by most recently selected
    selected_folder = folder_options.sort_values("date_updated", ascending=False).iloc[0]
    st.session_state.selected_folder = selected_folder["id"]
except IndexError:
    pass





gannt_section = st.empty()

folder_sidebar_area = st.sidebar.empty()

folder_selector = folder_sidebar_area.selectbox("Select a folder", folder_options["title"].values, key="folder_selector")
new_folder_btn = folder_sidebar_area.button("Create New Folder")

if new_folder_btn:
    folder_sidebar_area.empty()
    folder_name = st.sidebar.text_input("Folder Name")
    folder_dir = os.path.join(directory_path, folder_name)
    create_folder_btn = folder_sidebar_area.button("Save Folder")
    folder_sidebar_area.button("Cancel")


# Use streamlit's txt input to get the name of the folder
selected_folder_section = st.sidebar.empty()
selected_project_section = st.sidebar.empty()
new_project = st.sidebar.empty()

if new_folder_btn:
    # Create the folder if it doesn't exist
    if not os.path.exists(folder_dir):
        os.makedirs(folder_dir)
        # add folder to productivity_csv without using append
        new_folder = pd.DataFrame({"id": make_safe(), "date_created": [pd.Timestamp.now()], "date_updated": [pd.Timestamp.now()], "folder_dir": [folder_dir], "identifying_type": ["folder"], "title": [folder_name], "most_recently_selected": [pd.Timestamp.now()]})
        new_folder.to_csv(productivity_csv_path, mode="a", header=False, index=False)
        success_func(f"Successfully created folder {folder_name}")
    elif folder_name == "":
        st.warning("Please enter a folder name.")
    elif os.path.exists(folder_dir):
        st.warning("Folder already exists. Please use a different name.")



if selected_folder is None:
    st.write("No folders found. Please create a folder.")
else:
    with selected_folder_section.container():
        folder_path = selected_folder["folder_dir"]

        if not os.path.exists(os.path.join(selected_folder["folder_dir"], "json_data")):
            st.write("No items in directory")
        else:
            if os.path.exists(os.path.join(folder_path, "json_data")):
                json_files = [file for file in os.listdir(os.path.join(folder_path, "json_data")) if os.path.isfile(os.path.join(folder_path, "json_data", file)) and file.endswith(".json")]

                for json_file in json_files:
                    json_file_path = os.path.join(folder_path, "json_data", json_file)
                    with open(json_file_path, "r") as file:
                        json_data = json.load(file)
                    identifying_type = json_data["identifying_type"]

                    if identifying_type == "project":
                        project_id = json_data["id"]
                        title = json_data["title"]
                        if not json_data["no_due_date"]:
                            due_date = json_data["datetime_due"]
                        else:
                            due_date = "No due date"
                        completed = json_data["completed"]
                        start_date = json_data["start_date"]

                        num_tasks = len(json_data["tasks"])

                        if num_tasks > 0:
                            for task in json_data['tasks']:
                                # use the task id to find the task's folder_dir in productivity_csv
                                task_folder_dir = productivity_csv[productivity_csv["id"] == task]["folder_dir"].values[0]
                                # use the task_folder_dir to find the task's json file
                                task_json_file = [file for file in os.listdir(os.path.join(task_folder_dir, "json_data")) if os.path.isfile(os.path.join(task_folder_dir, "json_data", file)) and file.endswith(".json")][0]
                                # open the task's json file
                                with open(os.path.join(task_folder_dir, "json_data", task_json_file), "r") as file:
                                    task_json_data = json.load(file)
                                # get the task's title
                                task_title = task_json_data["title"]
                                # get the task's completed status
                                task_completed = task_json_data["completed"]


                        with st.expander(title):
                            st.checkbox("Completed", value=completed, key=f"{project_id}_completed")
                            st.write(f"#### due date: {due_date}")

                            if num_tasks > 0:
                                st.write(f"##### {num_tasks} tasks")
                            else:
                                st.write(f"##### No tasks")

                            st.write(f"##### Created: {json_data['date_created']}")
                            st.write(f"##### Updated: {json_data['date_modified']}")
                            edit_project_btn = st.button("Edit Project", key=f"{project_id}_edit_project")
                            add_task_btn = st.button("Add Task", key=f"{project_id}_add_task")
                            add_deliverable_btn = st.button("Add Deliverable", key=f"{project_id}_add_deliverable")
                            add_milestone_btn = st.button("Add Milestone", key=f"{project_id}_add_milestone")

                


    

    if st.session_state.new_project_creation == False:
        new_project_button = new_project.button("Create New Project")
        if new_project_button:
            st.session_state.new_project_creation = True
            st.experimental_rerun()
    else:
        with new_project.container():
            st.write("## New Project")
            new_project_title = st.empty()
            new_project_description = st.empty()
            st.write("---")
            new_project_due_date_checkbox = st.empty()
            new_project_due_date = st.empty()
            new_project_priority = st.empty()
            new_project_status = st.empty()
            st.write("---")
            new_project_more_descriptors = st.expander("Add More Descriptors")
            st.write("---")
            new_project_resources = st.expander("Add Resources")
            st.write("---")
            with new_project_more_descriptors:
                category_col, goal_verb_col, genre_col = st.empty(), st.empty(), st.empty()
                for key, value in options_lists.items():
                    for k,v in value.items():
                        for k2, v2 in v.items():
                            if v2['type'] == "list":
                                formatted_input_options = formatted_options("None", v2["options"])
                                if k2 == "category":
                                    project_category = category_col.selectbox(v2['label'], formatted_input_options, help=v2['description'], key=f"{k2}_selectbox")
                                if k2 == "goal_verb":
                                    project_goal_verb = goal_verb_col.selectbox(v2['label'], formatted_input_options, help=v2['description'], key=f"{k2}_selectbox")
                                if k2 == "genre":
                                    project_genre = genre_col.selectbox(v2['label'], formatted_input_options, help=v2['description'], key=f"{k2}_selectbox")
                                if k2 == "priority":
                                    project_priority = new_project_priority.selectbox(v2['label'], formatted_input_options, help=v2['description'], key=f"{k2}_selectbox")
                                if k2 == "status":
                                    project_status = new_project_status.selectbox(v2['label'], formatted_input_options, help=v2['description'], key=f"{k2}_selectbox")

            for key, value in options_lists.items():
                    for k,v in value.items():
                        for k2, v2 in v.items():
                            if v2['type'] == "text":
                                if k2 == "title":
                                    project_title = new_project_title.text_input(v2['label'], help=v2['description'])
                                if k2 == "description":
                                    project_description = new_project_description.text_area(v2['label'], help=v2['description'])

                            if v2['type'] == "boolean":
                                if k2 == "due":
                                    project_due = new_project_due_date_checkbox.checkbox(v2['label'], value=False, help=v2['description'])
                            
                            if v2['type'] == "date":
                                if k2 == "date_due":
                                    # set var x to today's date + 1 month
                                    month_from_now = datetime.now() + pd.DateOffset(months=1)
                                    project_due_date = new_project_due_date.date_input(v2['label'], help=v2['description'], key=f"{k2}_date_input", value=month_from_now, min_value=datetime.now(), disabled=project_due)
                                if k2 == "estimated_date_to_start":
                                    project_estimated_date_to_start = new_project_due_date.date_input(v2['label'], help=v2['description'], key=f"{k2}_date_input", value=datetime.now(), min_value=datetime.now(), disabled=project_due)




            st.write("---")
            save_col, cancel_col = st.columns([1, 1])
            new_project_button = save_col.button("Save Project")
            cancel_button = cancel_col.button("Cancel")

        if cancel_button:
            st.session_state.new_project_creation = False
            st.experimental_rerun()

        if new_project_button:
            # add row to productivity_csv
            new_project_id = make_safe()
            new_project = pd.DataFrame({"id": new_project_id, "date_created": [pd.Timestamp.now()], "date_updated": [pd.Timestamp.now()], "folder_dir": [os.path.join(selected_folder["folder_dir"], "json_data", project_title)], "identifying_type": ["project"], "title": [project_title], "most_recently_selected": [pd.Timestamp.now()]})

            new_project_timeline = pd.DataFrame({"id": new_project_id, "completed": False, "type": "project", "title": project_title, "started": False, "estimated_duration": None, "actual_duration": None, "due_date": project_due_date}, index=[0])
            with open(timeline_csv_path, 'a') as f:
                new_project_timeline.to_csv(f, header=False, index=False)

            with open(productivity_csv_path, 'a') as f:
                new_project.to_csv(f, header=False, index=False)

            if not os.path.exists(os.path.join(selected_folder["folder_dir"], project_title)):
                os.makedirs(os.path.join(selected_folder["folder_dir"], project_title))
            if not os.path.exists(os.path.join(selected_folder["folder_dir"], "json_data")):
                os.makedirs(os.path.join(selected_folder["folder_dir"], "json_data"))
            
            new_project_json = new_project_json_template.copy()
            new_project_json["id"] = new_project_id
            new_project_json["date_created"] = pd.Timestamp.now()
            new_project_json["date_modified"] = pd.Timestamp.now()
            new_project_json["title"] = project_title
            new_project_json["description"] = project_description
            new_project_json["folder_dir"] = os.path.join(selected_folder["folder_dir"], "json_data", project_title)
            new_project_json["due"] = project_due
            new_project_json["datetime_due"] = project_due_date
            new_project_json["category"] = project_category
            new_project_json["goal_verb"] = project_goal_verb
            new_project_json["genre"] = project_genre

            with open(os.path.join(selected_folder["folder_dir"], "json_data", f"project_{new_project_id}.json"), "w") as file:
                json.dump(new_project_json, file, cls=CustomJSONEncoder)
            
            with open(os.path.join(selected_folder["folder_dir"], "README.md"), "w") as file:
                file.write(f"# {project_title}\n\n{project_description}")
            st.session_state.selected_project = new_project_id
            st.session_state.new_project_creation = False
            success_func(f"Successfully created project {project_title}")


