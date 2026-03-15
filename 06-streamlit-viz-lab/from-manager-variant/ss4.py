import os
import streamlit as st
import uuid
import json
import datetime
from app.administrative import make_safe, valid_value, CustomJSONEncoder, formatted_options, comment_safe
from app.options_lists import time_conversion_factors, project_inputs, task_inputs, milestone_inputs, deliverable_inputs
from app.csv_creation import create_csvs
import pandas as pd
import shutil
import csv

# make streamlit wide
st.set_page_config(layout="wide")

edit_delete_selected_session_states = ["delete_selected_folder", "delete_selected_project", "delete_selected_task",  "delete_selected_milestone", "delete_selected_deliverable", "edit_selected_folder", "edit_selected_project", "edit_selected_task", "edit_selected_milestone", "edit_selected_deliverable"]
selected_session_states = ["selected_folder", "selected_folder_name", "selected_project", "selected_project_name", "selected_task", "selected_task_name","selected_milestone", "selected_milestone_name", "selected_deliverable", "selected_deliverable_name"]
view_session_stated = ["view_mode", "view_selected_project", "view_project", "view_selected_task", "view_task", "view_selected_milestone", "view_milestone", "view_selected_deliverable", "view_deliverable", "view_folder", "view_selected_folder"]
create_session_states = ["create_mode", "create_folder", "create_project", "create_task", "create_milestone", "create_deliverable"]
edit_session_states = ["edit_mode", "edit_folder", "edit_project", "edit_task", "edit_milestone", "edit_deliverable"]
delete_session_states = ["delete_mode", "delete_folder", "delete_project", "delete_task", "delete_milestone", "delete_deliverable"]
save_session_states = ["save_mode", "save_successful", "save_folder", "save_project", "save_task", "save_milestone", "save_deliverable"]

# combine all the session_state lists into one list

session_states = edit_delete_selected_session_states + selected_session_states + create_session_states + edit_session_states + delete_session_states + save_session_states + view_session_stated
    
for session_state in session_states:
    if session_state not in st.session_state:
        st.session_state[session_state] = False


directory_path = "productivity"
if not os.path.exists(directory_path):
    os.makedirs(directory_path)

csv_folder = "csvs"
if not os.path.exists(os.path.join(directory_path, csv_folder)):
    os.makedirs(os.path.join(directory_path, csv_folder))

productivity_csv_path, timeline_csv_path = create_csvs(directory_path, csv_folder)
productivity_csv = pd.read_csv(productivity_csv_path)
timeline_csv = pd.read_csv(timeline_csv_path)

# Load data
@st.cache_data(ttl=60)
def load_data():
    timeline_df = pd.read_csv(timeline_csv_path)
    productivity_df = pd.read_csv(productivity_csv_path)

    return timeline_df, productivity_df


def success_func(txt="Success"):
    success_txt = txt
    st.session_state.clear()
    if "save_successful" not in st.session_state:
        st.session_state.save_successful = success_txt
    st.experimental_rerun()
    st.success(st.session_state.save_successful)
    st.session_state.save_successful = False

def set_session_states(true, false, ids, names):
    # Setting session_state keys in 'true' list to True
    st.session_state.clear()
    for key in true:
        st.session_state[key] = True
        print("### True")
        print(st.session_state[key])
    # Setting session_state keys in 'false' list to False
    for key in false:
        st.session_state[key] = False
        print("### False")
        print(st.session_state[key])
    # Setting session_state keys in 'ids' dictionary to corresponding values
    for key, value in ids.items():
        st.session_state[key] = value
        print("### ids")
        print(st.session_state[key])
    # Setting session_state keys in 'names' dictionary to corresponding values
    for key, value in names.items():
        st.session_state[key] = value
        print("### names")
        print(st.session_state[key])
        
def save_comment_to_md_file(selected_folder_name, comment, comment_id):
    folder_dir = f"{directory_path}/{selected_folder_name}/comments"
    if not os.path.exists(folder_dir):
        os.makedirs(folder_dir)
    file_name = f"comment_{comment_id}.md"
    md_file_path = os.path.join(folder_dir, file_name)
    with open(md_file_path, "w") as f:
        f.write(comment)
    return folder_dir, file_name

def add_comment_to_item(selected_folder_name, selected_item, comment):
    comment_id = make_safe()
    folder_dir, file_name = save_comment_to_md_file(selected_folder_name, comment, comment_id)

    # add comment to productivity.csv
    comment_preview = comment_safe(comment)
    today = datetime.datetime.now()
    today = pd.to_datetime(today.strftime("%Y-%m-%d %H:%M:%S"))
    new_comment_csv_data = {
        "id": [comment_id],
        "date_created": [today],
        "date_updated": [today],
        "folder_dir": [folder_dir],
        "file_name": [file_name],
        "identifying_type": ["comment"],
        "title": [comment_preview],
        "parent": [selected_item],
    }
    new_comment_csv = pd.DataFrame(new_comment_csv_data)
    new_comment_csv.to_csv(productivity_csv_path, mode="a", header=False, index=False)

    #find the row in productivity_csv where id == selected_item and update the children column
    productivity_csv.loc[productivity_csv['id'] == selected_item, 'children'] = f"{productivity_csv.loc[productivity_csv['id'] == selected_item, 'children'].values[0]}{comment_id},"
    productivity_csv.to_csv(productivity_csv_path, index=False)

    return comment_id

def save_attachment_to_file(selected_folder_name, file):
    if file.type == "application/pdf":
        folder_dir = f"{directory_path}/{selected_folder_name}/attachments/documents"
    elif file.type == "image/png" or file.type == "image/jpeg":
        folder_dir = f"{directory_path}/{selected_folder_name}/attachments/images"
    elif file.type == "text/plain":
        folder_dir = f"{directory_path}/{selected_folder_name}/attachments/documents"
    else:
        folder_dir = f"{directory_path}/{selected_folder_name}/attachments/other"
    if not os.path.exists(folder_dir):
        os.makedirs(folder_dir)
    file_name = file.name
    file_path = os.path.join(folder_dir, file_name)
    with open(file_path, "wb") as f:
        f.write(file.getbuffer())
    return folder_dir, file_name

def save_attachment(selected_folder_name, selected_item, file):
    attachment_id = make_safe()
    folder_dir, file_name = save_attachment_to_file(selected_folder_name, file)

    # add attachment to productivity.csv
    today = datetime.datetime.now()
    today = pd.to_datetime(today.strftime("%Y-%m-%d %H:%M:%S"))
    new_attachment_csv_data = {
        "id": [attachment_id],
        "date_created": [today],
        "date_updated": [today],
        "folder_dir": [folder_dir],
        "file_name": [file_name],
        "identifying_type": ["attachment"],
        "title": [file_name],
        "parent": [selected_item],
    }
    new_attachment_csv = pd.DataFrame(new_attachment_csv_data)
    new_attachment_csv.to_csv(productivity_csv_path, mode="a", header=False, index=False)

    return attachment_id

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

def check_if_projects_exist():
    project_data = productivity_csv[productivity_csv['identifying_type'] == 'project'].sort_values(by=['date_updated'], ascending=False)

    # get the rows where the parent column of productivity csv == selected_folder
    project_data = project_data[project_data['parent'] == st.session_state.selected_folder]

    # create a dictionary of project titles and ids from the csv file
    projects = {row["title"]: row["id"] for _, row in project_data.iterrows()}

    # if no project in the csv, selected_project will be None
    if len(project_data) == 0:
        st.session_state.selected_project = None
        st.session_state.edit_project = False
        st.session_state.delete_project = False
        st.session_state.view_project = False

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
        st.session_state.edit_project = True
        st.session_state.delete_project = True
        st.session_state.create_task = True
        st.session_state.create_milestone = True
        st.session_state.create_deliverable = True
        st.session_state.view_project = True

        st.session_state.selected_project = project_data.iloc[0]['id']
        st.session_state.selected_project_name = project_data.iloc[0]['title']

    return projects, project_data

def check_if_tasks_exist():
    task_data = productivity_csv[productivity_csv['identifying_type'] == 'task'].sort_values(by=['date_updated'], ascending=False)

    # get the rows where the parent column of productivity csv == selected_project or selected_folder
    task_data = task_data[task_data['parent'].isin([st.session_state.selected_project, st.session_state.selected_folder])]

    # create a dictionary of task titles and ids from the csv file
    tasks = {row["title"]: row["id"] for _, row in task_data.iterrows()}

    # if no task in the csv, selected_task will be None
    if len(task_data) == 0:
        st.session_state.selected_task = None
        st.session_state.edit_task = False
        st.session_state.delete_task = False
    else:
        st.session_state.edit_task = True
        st.session_state.delete_task = True

        st.session_state.selected_task = task_data.iloc[0]['id']
        st.session_state.selected_task_name = task_data.iloc[0]['title']

    return tasks, task_data

def check_if_milestones_exist():
    milestone_data = productivity_csv[productivity_csv['identifying_type'] == 'milestone'].sort_values(by=['date_updated'], ascending=False)

    # get the rows where the parent column of productivity csv == selected_project or selected_folder
    milestone_data = milestone_data[milestone_data['parent'].isin([st.session_state.selected_project, st.session_state.selected_folder])]

    # create a dictionary of milestone titles and ids from the csv file
    milestones = {row["title"]: row["id"] for _, row in milestone_data.iterrows()}

    # if no milestone in the csv, selected_milestone will be None
    if len(milestone_data) == 0:
        st.session_state.selected_milestone = None
        st.session_state.edit_milestone = False
        st.session_state.delete_milestone = False
    else:
        st.session_state.edit_milestone = True
        st.session_state.delete_milestone = True

        st.session_state.selected_milestone = milestone_data.iloc[0]['id']
        st.session_state.selected_milestone_name = milestone_data.iloc[0]['title']

    return milestones, milestone_data

def check_if_deliverables_exist():
    deliverable_data = productivity_csv[productivity_csv['identifying_type'] == 'deliverable'].sort_values(by=['date_updated'], ascending=False)

    # get the rows where the parent column of productivity csv == selected_project or selected_folder
    deliverable_data = deliverable_data[deliverable_data['parent'].isin([st.session_state.selected_project, st.session_state.selected_folder])]

    # create a dictionary of deliverable titles and ids from the csv file
    deliverables = {row["title"]: row["id"] for _, row in deliverable_data.iterrows()}
    # if no deliverable in the csv, selected_deliverable will be None
    if len(deliverable_data) == 0:
        st.session_state.selected_deliverable = None
        st.session_state.edit_deliverable = False
        st.session_state.delete_deliverable = False
    else:
        st.session_state.edit_deliverable = True
        st.session_state.delete_deliverable = True

        st.session_state.selected_deliverable = deliverable_data.iloc[0]['id']
        st.session_state.selected_deliverable_name = deliverable_data.iloc[0]['title']

    return deliverables, deliverable_data

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

def add_new_project_data():
    title_dict = project_inputs['title']
    description_dict = project_inputs['description']
    status_dict = project_inputs['status']
    priority_dict = project_inputs['priority']
    category_dict = project_inputs['category']
    goal_verb_dict = project_inputs['goal_verb']
    genre_dict = project_inputs['genre']
    use_case_dict = project_inputs['use_case']
    no_start_date_dict = project_inputs['no_start_date']
    start_date_dict = project_inputs['start_date']
    no_due_date_dict = project_inputs['no_due_date']
    due_date_dict = project_inputs['due_date']
    add_time_estimation_dict = project_inputs['estimated_time_to_complete_checkbox']
    estimated_time_to_complete_dict = project_inputs['estimated_time_to_complete']
    attachments_dict = project_inputs['attachments']
    comments_dict = project_inputs['comments']
    # Use the values from the dictionary to create the text_input
    title = st.text_input(
        title_dict['label'],  
        help=title_dict['help'], 
        placeholder=title_dict['placeholder']
        )
    description = st.text_area(
        description_dict['label'],
        help=description_dict['help'],
        placeholder=description_dict['placeholder']
        )
    status_col, priority_col = st.columns(2)
    status = status_col.selectbox(
        status_dict['label'],
        options=status_dict['options'],
        help=status_dict['help'],
        )
    priority = priority_col.number_input(
        priority_dict['label'],
        help=priority_dict['help'],
        min_value=priority_dict['min_value'],
        max_value=priority_dict['max_value'],
        )
    st.write("---")
    no_start_date = st.checkbox(
        no_start_date_dict['label'],
        value=no_start_date_dict['value'],
        help=no_start_date_dict['help'],
        )
    start_date = st.date_input(
        start_date_dict['label'],
        disabled=no_start_date,
        help=start_date_dict['help'],
        )
    no_due_date = st.checkbox(
        no_due_date_dict['label'],
        value=no_due_date_dict['value'],
        help=no_due_date_dict['help'],
        )
    due_date = st.date_input(
        due_date_dict['label'],
        disabled=no_due_date,
        help=due_date_dict['help'],
        )
    add_time_estimation = st.checkbox(add_time_estimation_dict['label'], help=add_time_estimation_dict['help'], value=False)
    add_time_completion_estimates = st.empty()
    duration=0
    unit = "minutes"
    unit_ammount = 1
    if add_time_estimation:
        with add_time_completion_estimates.container():
            available_units = [unit for unit in time_conversion_factors.keys()]
            time_completion_units, time_completion_number = st.columns(2)
            with time_completion_units:
                unit = st.selectbox(
                    "Unit",
                    options=available_units,
                    help=estimated_time_to_complete_dict["help"],
                    key = f"units_{len(available_units)}",
                )
            with time_completion_number:
                unit_ammount = st.number_input(
                    estimated_time_to_complete_dict['label'],
                    help=estimated_time_to_complete_dict['help'],
                    key = f"duration_{len(available_units)}",
                    min_value=1
                    )
            duration = unit_ammount * time_conversion_factors[unit]
    st.write("---")
    category_col, goal_verb_col = st.columns(2)
    genre_col, use_case_col = st.columns(2)
    category = category_col.selectbox(
        category_dict['label'],
        options=category_dict['options'],
        help=category_dict['help'],
        )
    goal_verb = goal_verb_col.selectbox(
        goal_verb_dict['label'],
        options=goal_verb_dict['options'],
        help=goal_verb_dict['help'],
        )
    genre = genre_col.selectbox(
        genre_dict['label'],
        options=genre_dict['options'],
        help=genre_dict['help'],
        )
    use_case = use_case_col.selectbox(
        use_case_dict['label'],
        options=use_case_dict['options'],
        help=use_case_dict['help'],
        )
    st.write("---")
    attachments = st.file_uploader(
        attachments_dict['label'],
        accept_multiple_files=True,
        help=attachments_dict['help'],
    )
    comments = st.text_area(
        comments_dict['label'],
        help=comments_dict['help'],
        placeholder=comments_dict['placeholder']
    )
    new_data = {
        "title": title,
        "description": description,
        "status": status,
        "priority": priority,
        "category": category,
        "goal_verb": goal_verb,
        "genre": genre,
        "use_case": use_case,
        "no_start_date": no_start_date,
        "start_date": start_date,
        "no_due_date": no_due_date,
        "due_date": due_date,
        "estimated_time_to_complete_checkbox": add_time_estimation,
        "estimated_time_to_complete": duration,
        "estimated_time_units": unit,
        "estimated_time_unit_ammount": unit_ammount,
        "actual_time_to_complete": None,
        "datetime_completed": None,
        "comments": comments,
        "attachments": attachments
    }
    if savebtn:
        if not valid_value(title):
            st.warning("Please enter a valid title")
        else:
            try:
                add_project(new_data)
                success_func("Project created successfully.")
            except Exception as e:
                st.write(f"An error occurred: {e}")

def add_new_task_data():
    title_dict = task_inputs['title']
    description_dict = task_inputs['description']
    status_dict = task_inputs['status']
    priority_dict = task_inputs['priority']
    category_dict = task_inputs['category']
    goal_verb_dict = task_inputs['goal_verb']
    genre_dict = task_inputs['genre']
    use_case_dict = task_inputs['use_case']
    no_start_date_dict = task_inputs['no_start_date']
    start_date_dict = task_inputs['start_date']
    no_due_date_dict = task_inputs['no_due_date']
    due_date_dict = task_inputs['due_date']
    add_time_estimation_dict = task_inputs['estimated_time_to_complete_checkbox']
    estimated_time_to_complete_dict = task_inputs['estimated_time_to_complete']
    dependencies_dict = task_inputs['dependencies']
    # Use the values from the dictionary to create the text_input
    title = st.text_input(
        title_dict['label'],  
        help=title_dict['help'], 
        placeholder=title_dict['placeholder']
        )
    description = st.text_area(
        description_dict['label'],
        help=description_dict['help'],
        placeholder=description_dict['placeholder']
        )
    status_col, priority_col = st.columns(2)
    status = status_col.selectbox(
        status_dict['label'],
        options=status_dict['options'],
        help=status_dict['help'],
        )
    priority = priority_col.number_input(
        priority_dict['label'],
        help=priority_dict['help'],
        min_value=priority_dict['min_value'],
        max_value=priority_dict['max_value'],
        )
    st.write("---")
    if "start_date" not in st.session_state:
        st.session_state.start_date = None
    no_start_date = st.checkbox(
        no_start_date_dict['label'],
        value=no_start_date_dict['value'],
        help=no_start_date_dict['help'],
        )
    start_date = st.date_input(
        start_date_dict['label'],
        disabled=no_start_date,
        help=start_date_dict['help'],
        )
    no_due_date = st.checkbox(
        no_due_date_dict['label'],
        value=no_due_date_dict['value'],
        help=no_due_date_dict['help'],
        )
    
    due_date = st.date_input(
        due_date_dict['label'],
        disabled=no_due_date,
        help=due_date_dict['help'],
        )
    add_time_estimation = st.checkbox(add_time_estimation_dict['label'], help=add_time_estimation_dict['help'], value=False)
    add_time_completion_estimates = st.empty()
    duration=None
    if add_time_estimation:
        with add_time_completion_estimates.container():
            available_units = [unit for unit in time_conversion_factors.keys()]
            time_completion_units, time_completion_number = st.columns(2)
            with time_completion_units:
                unit = st.selectbox(
                    "Unit",
                    options=available_units,
                    help=estimated_time_to_complete_dict["help"],
                    key = f"units_{len(available_units)}",
                )
            with time_completion_number:
                duration = st.number_input(
                    estimated_time_to_complete_dict['label'],
                    help=estimated_time_to_complete_dict['help'],
                    key = f"duration_{len(available_units)}",
                    min_value=1
                    )
            duration = duration * time_conversion_factors[unit]
    st.write("---")
    category_col, goal_verb_col = st.columns(2)
    genre_col, use_case_col = st.columns(2)
    category = category_col.selectbox(
        category_dict['label'],
        options=category_dict['options'],
        help=category_dict['help'],
        )
    goal_verb = goal_verb_col.selectbox(
        goal_verb_dict['label'],
        options=goal_verb_dict['options'],
        help=goal_verb_dict['help'],
        )
    genre = genre_col.selectbox(
        genre_dict['label'],
        options=genre_dict['options'],
        help=genre_dict['help'],
        )
    use_case = use_case_col.selectbox(
        use_case_dict['label'],
        options=use_case_dict['options'],
        help=use_case_dict['help'],
        )
    st.write("---")
    new_data = {
        "title": title,
        "description": description,
        "status": status,
        "priority": priority,
        "category": category,
        "goal_verb": goal_verb,
        "genre": genre,
        "use_case": use_case,
        "no_start_date": no_start_date,
        "start_date": start_date,
        "no_due_date": no_due_date,
        "due_date": due_date,
        "estimated_time_to_complete_checkbox": add_time_estimation,
        "estimated_time_to_complete": duration,
        "actual_time_to_complete": None,
        "completed": False,
        "datetime_completed": None,
    }
    if savebtn:
        if not valid_value(title):
            st.warning("Please enter a valid title")
        else:
            try:
                add_task(new_data)
                success_func("Task created successfully.")
            except Exception as e:
                st.write(f"An error occurred: {e}")

def add_new_milestone_data():
    title_dict = milestone_inputs['title']
    description_dict = milestone_inputs['description']
    category_dict = milestone_inputs['category']
    goal_verb_dict = milestone_inputs['goal_verb']
    genre_dict = milestone_inputs['genre']
    use_case_dict = milestone_inputs['use_case']
    no_due_date_dict = milestone_inputs['no_due_date']
    due_date_dict = milestone_inputs['due_date']
    # Use the values from the dictionary to create the text_input
    title = st.text_input(
        title_dict['label'],  
        help=title_dict['help'], 
        placeholder=title_dict['placeholder']
        )
    description = st.text_area(
        description_dict['label'],
        help=description_dict['help'],
        placeholder=description_dict['placeholder']
        )
    st.write("---")
    if "start_date" not in st.session_state:
        st.session_state.start_date = None
    no_due_date = st.checkbox(
        no_due_date_dict['label'],
        value=no_due_date_dict['value'],
        help=no_due_date_dict['help'],
        )
    due_date = st.date_input(
        due_date_dict['label'],
        disabled=no_due_date,
        help=due_date_dict['help'],
        )
    st.write("---")
    category_col, goal_verb_col = st.columns(2)
    genre_col, use_case_col = st.columns(2)
    category = category_col.selectbox(
        category_dict['label'],
        options=category_dict['options'],
        help=category_dict['help'],
        )
    goal_verb = goal_verb_col.selectbox(
        goal_verb_dict['label'],
        options=goal_verb_dict['options'],
        help=goal_verb_dict['help'],
        )
    genre = genre_col.selectbox(
        genre_dict['label'],
        options=genre_dict['options'],
        help=genre_dict['help'],
        )
    use_case = use_case_col.selectbox(
        use_case_dict['label'],
        options=use_case_dict['options'],
        help=use_case_dict['help'],
        )
    new_data = {
        "title": title,
        "description": description,
        "category": category,
        "goal_verb": goal_verb,
        "genre": genre,
        "use_case": use_case,
        "no_due_date": no_due_date,
        "due_date": due_date,
        "actual_time_to_complete": None,
        "completed": False,
        "datetime_completed": None,
    }
    if savebtn:
        if not valid_value(title):
            st.warning("Please enter a valid title")
        else:
            try:
                add_milestone(new_data)
                success_func("Milestone created successfully.")
            except Exception as e:
                st.write(f"An error occurred: {e}")

def add_new_deliverable_data():
    title_dict = deliverable_inputs['title']
    description_dict = deliverable_inputs['description']
    category_dict = deliverable_inputs['category']
    goal_verb_dict = deliverable_inputs['goal_verb']
    genre_dict = deliverable_inputs['genre']
    use_case_dict = deliverable_inputs['use_case']
    no_due_date_dict = deliverable_inputs['no_due_date']
    due_date_dict = deliverable_inputs['due_date']
    dependencies_dict = deliverable_inputs['dependencies']
    quality_criteria = deliverable_inputs['quality_criteria']
    acceptance_criteria = deliverable_inputs['acceptance_criteria']
    # Use the values from the dictionary to create the text_input
    title = st.text_input(
        title_dict['label'],  
        help=title_dict['help'], 
        placeholder=title_dict['placeholder']
        )
    description = st.text_area(
        description_dict['label'],
        help=description_dict['help'],
        placeholder=description_dict['placeholder']
        )
    st.write("---")
    no_due_date = st.checkbox(
        no_due_date_dict['label'],
        value=no_due_date_dict['value'],
        help=no_due_date_dict['help'],
        )
    due_date = st.date_input(
        due_date_dict['label'],
        disabled=no_due_date,
        help=due_date_dict['help'],
        )
    st.write("---")
    category_col, goal_verb_col = st.columns(2)
    genre_col, use_case_col = st.columns(2)
    category = category_col.selectbox(
        category_dict['label'],
        options=category_dict['options'],
        help=category_dict['help'],
        )
    goal_verb = goal_verb_col.selectbox(
        goal_verb_dict['label'],
        options=goal_verb_dict['options'],
        help=goal_verb_dict['help'],
        )
    genre = genre_col.selectbox(
        genre_dict['label'],
        options=genre_dict['options'],
        help=genre_dict['help'],
        )
    use_case = use_case_col.selectbox(
        use_case_dict['label'],
        options=use_case_dict['options'],
        help=use_case_dict['help'],
        )
    st.write("---")
    quality_criteria = st.text_area(
        quality_criteria['label'],
        help=quality_criteria['help'],
        placeholder=quality_criteria['placeholder']
    )
    acceptance_criteria = st.text_area(
        acceptance_criteria['label'],
        help=acceptance_criteria['help'],
        placeholder=acceptance_criteria['placeholder']
    )
    new_data = {
        "title": title,
        "description": description,
        "category": category,
        "goal_verb": goal_verb,
        "genre": genre,
        "use_case": use_case,
        "no_due_date": no_due_date,
        "due_date": due_date,
        "actual_time_to_complete": None,
        "completed": False,
        "datetime_completed": None,
        "quality_criteria": quality_criteria,
        "acceptance_criteria": acceptance_criteria
    }
    if savebtn:
        if not valid_value(title):
            st.warning("Please enter a valid title")
        else:
            try:
                add_deliverable(new_data)
                success_func("Deliverable created successfully.")
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

def add_project(new_data):
    new_project = {
        "id": make_safe(),
        "tasks": [],
        "milestones": [],
        "deliverables": [],
        "completed": False,
        "datetime_completed": datetime.datetime.now().strftime("%Y-%m-%d")
    }
    new_data['id'] = new_project['id']
    new_data['tasks'] = new_project['tasks']
    new_data['milestones'] = new_project['milestones']
    new_data['deliverables'] = new_project['deliverables']
    new_data['completed'] = new_project['completed']
    new_data['datetime_completed'] = new_project['datetime_completed']
    today = datetime.datetime.now()
    today = pd.to_datetime(today.strftime("%Y-%m-%d %H:%M:%S"))

    if new_data['attachments'] is not None:
        attachment_ids_list = []
        for attachment in new_data['attachments']:
            attachment_id = save_attachment(st.session_state.selected_folder_name, new_data['id'], attachment)
            attachment_ids_list.append(attachment_id)
        new_data['attachments'] = []
        for att_id in attachment_ids_list:
            new_data['attachments'].append(att_id)

    if valid_value(new_data['comments']):
        comment_id = add_comment_to_item(st.session_state.selected_folder_name, new_data['id'], new_data['comments'])
        new_data['comments'] = []
        new_data['comments'].append(comment_id)

    new_project_path = os.path.join(directory_path, st.session_state.selected_folder_name, 'json_data', f"project_{new_data['id']}.json")
    if not os.path.exists(new_project_path):
        with open(new_project_path, "w") as file:
            json.dump(new_data, file, indent=4, cls=CustomJSONEncoder)
    project_folder_directory = os.path.join(directory_path, st.session_state.selected_folder_name)
    new_project_csv_data = {
        "id": [new_data['id']],
        "date_created": [today],
        "date_updated": [today],
        "folder_dir": [project_folder_directory],
        "file_name": [f"project_{new_data['id']}.json"],
        "identifying_type": ["project"],
        "title": [new_data['title']],
        "parent": [st.session_state.selected_folder]
    }

    new_project_csv = pd.DataFrame(new_project_csv_data)
    new_project_csv.to_csv(productivity_csv_path, mode="a", header=False, index=False)

    new_timeline_csv_data = {
        "id": [new_data['id']],
        "type": ["project"],
        "title": [new_data['title']],
        "status": [new_data['status']],
        "priority": [new_data['priority']],
        "no_start_date": [new_data['no_start_date']],
        "start_date": [new_data['start_date']],
        "no_due_date": [new_data['no_due_date']],
        "due_date": [new_data['due_date']],
        "estimated_time_to_complete": [new_data['estimated_time_to_complete_checkbox']],
        "estimated_duration": [new_data['estimated_time_to_complete']],
        "completed": [new_data['completed']],
        "datetime_completed": [new_data['datetime_completed']],
        "date_last_worked_on": [today],
    }
    new_timeline_csv = pd.DataFrame(new_timeline_csv_data)
    new_timeline_csv.to_csv(timeline_csv_path, mode="a", header=False, index=False)

def add_task(new_data):
    new_task = {
        "id": make_safe(),
        "complete": False,
        "datetime_completed": datetime.datetime.now().strftime("%Y-%m-%d")
    }
    new_data['id'] = new_task['id']
    new_data['complete'] = new_task['complete']
    new_data['datetime_completed'] = new_task['datetime_completed']
    today = datetime.datetime.now()
    today = pd.to_datetime(today.strftime("%Y-%m-%d %H:%M:%S"))

    # create task_{id}.json in selected folder/json_data
    new_task_path = os.path.join(directory_path, st.session_state.selected_folder_name, 'json_data', f"task_{new_data['id']}.json")
    if not os.path.exists(new_task_path):
        with open(new_task_path, "w") as file:
            json.dump(new_data, file, indent=4, cls=CustomJSONEncoder)


    task_folder_directory = os.path.join(directory_path, st.session_state.selected_folder_name)
    new_task_csv_data = {
        "id": [new_data['id']],
        "date_created": [today],
        "date_updated": [today],
        "folder_dir": [task_folder_directory],
        "file_name": [f"task_{new_data['id']}.json"],
        "identifying_type": ["task"],
        "title": [new_data['title']],
        "parent": [st.session_state.selected_project]
    }
    new_task_csv = pd.DataFrame(new_task_csv_data)
    new_task_csv.to_csv(productivity_csv_path, mode="a", header=False, index=False)

    # append the task id to the selected_project json file
    project_json_path = os.path.join(directory_path, st.session_state.selected_folder_name, 'json_data', f"project_{st.session_state.selected_project}.json")
    with open(project_json_path, "r") as file:
        project_json = json.load(file)
    project_json['tasks'].append(new_data['id'])
    with open(project_json_path, "w") as file:
        json.dump(project_json, file, indent=4, cls=CustomJSONEncoder)

    new_timeline_csv_data = {
        "id": [new_data['id']],
        "type": ["task"],
        "title": [new_data['title']],
        "status": [new_data['status']],
        "priority": [new_data['priority']],
        "no_start_date": [new_data['no_start_date']],
        "start_date": [new_data['start_date']],
        "no_due_date": [new_data['no_due_date']],
        "due_date": [new_data['due_date']],
        "estimated_time_to_complete": [new_data['estimated_time_to_complete_checkbox']],
        "estimated_duration": [new_data['estimated_time_to_complete']],
        "completed": [new_data['completed']],
        "datetime_completed": [new_data['datetime_completed']],
        "date_last_worked_on": [today],
    }
    new_timeline_csv = pd.DataFrame(new_timeline_csv_data)
    new_timeline_csv.to_csv(timeline_csv_path, mode="a", header=False, index=False)

def add_milestone(new_data):
    new_milestone = {
        "id": make_safe(),
        "complete": False,
        "datetime_completed": datetime.datetime.now().strftime("%Y-%m-%d")
    }
    new_data['id'] = new_milestone['id']
    new_data['complete'] = new_milestone['complete']
    new_data['datetime_completed'] = new_milestone['datetime_completed']
    today = datetime.datetime.now()
    today = pd.to_datetime(today.strftime("%Y-%m-%d %H:%M:%S"))

    # create milestone_{id}.json in selected folder/json_data
    new_milestone_path = os.path.join(directory_path, st.session_state.selected_folder_name, 'json_data', f"milestone_{new_data['id']}.json")
    if not os.path.exists(new_milestone_path):
        with open(new_milestone_path, "w") as file:
            json.dump(new_data, file, indent=4, cls=CustomJSONEncoder)

    milestone_folder_directory = os.path.join(directory_path, st.session_state.selected_folder_name)
    new_milestone_csv_data = {
        "id": [new_data['id']],
        "date_created": [today],
        "date_updated": [today],
        "folder_dir": [milestone_folder_directory],
        "file_name": [f"milestone_{new_data['id']}.json"],
        "identifying_type": ["milestone"],
        "title": [new_data['title']],
        "parent": [st.session_state.selected_project]
    }
    new_milestone_csv = pd.DataFrame(new_milestone_csv_data)
    new_milestone_csv.to_csv(productivity_csv_path, mode="a", header=False, index=False)

    # append the milestone id to the selected_project json file
    project_json_path = os.path.join(directory_path, st.session_state.selected_folder_name, 'json_data', f"project_{st.session_state.selected_project}.json")
    with open(project_json_path, "r") as file:
        project_json = json.load(file)
    project_json['milestones'].append(new_data['id'])
    with open(project_json_path, "w") as file:
        json.dump(project_json, file, indent=4, cls=CustomJSONEncoder)

    new_timeline_csv_data = {
        "id": [new_data['id']],
        "type": ["milestone"],
        "title": [new_data['title']],
        "no_due_date": [new_data['no_due_date']],
        "due_date": [new_data['due_date']],
        "completed": [new_data['completed']],
        "datetime_completed": [new_data['datetime_completed']],
        "date_last_worked_on": [today],
        "status": [None],
        "priority": [None],
        "no_start_date": [None],
        "start_date": [None],
        "estimated_time_to_complete": [None],
        "estimated_duration": [None]
    }
    new_timeline_csv = pd.DataFrame(new_timeline_csv_data)
    new_timeline_csv.to_csv(timeline_csv_path, mode="a", header=False, index=False)

def add_deliverable(new_data):
    new_deliverable = {
        "id": make_safe(),
        "complete": False,
        "datetime_completed": datetime.datetime.now().strftime("%Y-%m-%d")
    }
    new_data['id'] = new_deliverable['id']
    new_data['complete'] = new_deliverable['complete']
    new_data['datetime_completed'] = new_deliverable['datetime_completed']
    today = datetime.datetime.now()
    today = pd.to_datetime(today.strftime("%Y-%m-%d %H:%M:%S"))

    # create deliverable_{id}.json in selected folder/json_data
    new_deliverable_path = os.path.join(directory_path, st.session_state.selected_folder_name, 'json_data', f"deliverable_{new_data['id']}.json")
    if not os.path.exists(new_deliverable_path):
        with open(new_deliverable_path, "w") as file:
            json.dump(new_data, file, indent=4, cls=CustomJSONEncoder)

    deliverable_folder_directory = os.path.join(directory_path, st.session_state.selected_folder_name)
    new_deliverable_csv_data = {
        "id": [new_data['id']],
        "date_created": [today],
        "date_updated": [today],
        "folder_dir": [deliverable_folder_directory],
        "file_name": [f"deliverable_{new_data['id']}.json"],
        "identifying_type": ["deliverable"],
        "title": [new_data['title']],
        "parent": [st.session_state.selected_project]
    }
    new_deliverable_csv = pd.DataFrame(new_deliverable_csv_data)
    new_deliverable_csv.to_csv(productivity_csv_path, mode="a", header=False, index=False)

    # append the deliverable id to the selected_project json file
    project_json_path = os.path.join(directory_path, st.session_state.selected_folder_name, 'json_data', f"project_{st.session_state.selected_project}.json")
    with open(project_json_path, "r") as file:
        project_json = json.load(file)
    project_json['deliverables'].append(new_data['id'])
    with open(project_json_path, "w") as file:
        json.dump(project_json, file, indent=4, cls=CustomJSONEncoder)


    new_timeline_csv_data = {
        "id": [new_data['id']],
        "type": ["deliverable"],
        "title": [new_data['title']],
        "no_due_date": [new_data['no_due_date']],
        "due_date": [new_data['due_date']],
        "completed": [new_data['completed']],
        "datetime_completed": [new_data['datetime_completed']],
        "date_last_worked_on": [today],
        "status": [None],
        "priority": [None],
        "no_start_date": [None],
        "start_date": [None],
        "estimated_time_to_complete": [None],
        "estimated_duration": [None]
    }
    new_timeline_csv = pd.DataFrame(new_timeline_csv_data)
    new_timeline_csv.to_csv(timeline_csv_path, mode="a", header=False, index=False)

def remove_folder(folder_id):
    if folder_id != st.session_state.selected_folder:
        st.experimental_rerun()
        return
    # delete the folder from the directory_path
    folder_path = os.path.join(directory_path, st.session_state.selected_folder_name)
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
    else:
        print(f"Error: Folder '{st.session_state.selected_folder_name}' does not exist")

    productivity_csv = pd.read_csv(productivity_csv_path)

    ids_to_delete = [folder_id]

    # find all the rows where the parent column of productivity csv is the folder_id
    children = productivity_csv[productivity_csv["parent"] == folder_id]
    child_ids = children['id'].tolist()

    # extend ids_to_delete with the child_ids
    ids_to_delete.extend(child_ids)

    # check if any of the ids_to_delete are in the parent column of productivity_csv
    grand_children = productivity_csv[productivity_csv["parent"].isin(ids_to_delete)]
    grand_child_ids = grand_children['id'].tolist()

    # extend ids_to_delete with the grand_child_ids
    ids_to_delete.extend(grand_child_ids)

    # Delete the json files for the ids_to_delete
    for id_to_delete in ids_to_delete:
        file_info = productivity_csv[productivity_csv['id'] == id_to_delete]
        if not file_info.empty:
            folder_dir = file_info['folder_dir'].values[0]
            file_name = file_info['file_name'].values[0]
            file_path = os.path.join(folder_dir, "json_data", file_name)

            if os.path.exists(file_path):
                os.remove(file_path)

    # delete all the rows where id is in ids_to_delete
    productivity_csv = productivity_csv[~productivity_csv['id'].isin(ids_to_delete)]
    productivity_csv.to_csv(productivity_csv_path, index=False)

def remove_project(project_id):
    # load the csv files
    productivity_csv = pd.read_csv(productivity_csv_path)

    # initialize a list with ids to delete
    ids_to_delete = [project_id]

    # find all the rows where the parent column of productivity csv is the project_id
    children = productivity_csv[productivity_csv["parent"] == project_id]
    child_ids = children['id'].tolist()

    # extend ids_to_delete with the child_ids
    ids_to_delete.extend(child_ids)

    # check if any of the ids_to_delete are in the parent column of productivity_csv
    grand_children = productivity_csv[productivity_csv["parent"].isin(ids_to_delete)]
    grand_child_ids = grand_children['id'].tolist()

    # extend ids_to_delete with the grand_child_ids
    ids_to_delete.extend(grand_child_ids)

    # Delete the json files for the ids_to_delete
    for id_to_delete in ids_to_delete:
        file_info = productivity_csv[productivity_csv['id'] == id_to_delete]
        if not file_info.empty:
            folder_dir = file_info['folder_dir'].values[0]
            file_name = file_info['file_name'].values[0]
            file_path = os.path.join(folder_dir, "json_data", file_name)

            if os.path.exists(file_path):
                os.remove(file_path)

    # delete all the rows where id is in ids_to_delete
    productivity_csv = productivity_csv[~productivity_csv['id'].isin(ids_to_delete)]
    productivity_csv.to_csv(productivity_csv_path, index=False)

def remove_task(task_id):
    # load the csv files
    productivity_csv = pd.read_csv(productivity_csv_path)


    # get the task info and delete the json file
    task_info = productivity_csv[productivity_csv['id'] == task_id]
    if not task_info.empty:
        folder_dir = task_info['folder_dir'].values[0]
        file_name = task_info['file_name'].values[0]
        file_path = os.path.join(folder_dir, "json_data", file_name)

        if os.path.exists(file_path):
            os.remove(file_path)

    # remove the task id from the selected project json file
    parent_project = st.session_state.selected_project
    
    # using the parent_project as the id, find the corresponding row in the productivity_csv
    parent_project_row = productivity_csv[productivity_csv['id'] == parent_project]
    if not parent_project_row.empty:
        folder_dir = parent_project_row['folder_dir'].values[0]
        file_name = parent_project_row['file_name'].values[0]
        file_path = os.path.join(folder_dir, "json_data", file_name)

        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                project_json = json.load(f)
            project_json['tasks'].remove(task_id)
            with open(file_path, 'w') as f:
                json.dump(project_json, f)

    # remove the task from the timeline csv
    timeline_csv = pd.read_csv(timeline_csv_path)
    timeline_csv = timeline_csv[timeline_csv['id'] != task_id]
    timeline_csv.to_csv(timeline_csv_path, index=False)

    # delete the task row in the csv files
    productivity_csv = productivity_csv[productivity_csv['id'] != task_id]
    productivity_csv.to_csv(productivity_csv_path, index=False)

def remove_milestone(milestone_id):
    # load the csv files
    productivity_csv = pd.read_csv(productivity_csv_path)

    # get the milestone info and delete the json file
    milestone_info = productivity_csv[productivity_csv['id'] == milestone_id]
    if not milestone_info.empty:
        folder_dir = milestone_info['folder_dir'].values[0]
        file_name = milestone_info['file_name'].values[0]
        file_path = os.path.join(folder_dir, "json_data", file_name)

        if os.path.exists(file_path):
            os.remove(file_path)

    # delete the milestone row in the csv files
    productivity_csv = productivity_csv[productivity_csv['id'] != milestone_id]
    productivity_csv.to_csv(productivity_csv_path, index=False)

def remove_deliverable(deliverable_id):
    # load the csv files
    productivity_csv = pd.read_csv(productivity_csv_path)


    # get the deliverable info and delete the json file
    deliverable_info = productivity_csv[productivity_csv['id'] == deliverable_id]
    if not deliverable_info.empty:
        folder_dir = deliverable_info['folder_dir'].values[0]
        file_name = deliverable_info['file_name'].values[0]
        file_path = os.path.join(folder_dir, "json_data", file_name)

        if os.path.exists(file_path):
            os.remove(file_path)

    # delete the deliverable row in the csv files
    productivity_csv = productivity_csv[productivity_csv['id'] != deliverable_id]
    productivity_csv.to_csv(productivity_csv_path, index=False)

def edit_folder_func(folder_id):
    if folder_id != st.session_state.selected_folder:
        st.experimental_rerun()
        return

    # load the csv files
    productivity_csv = pd.read_csv(productivity_csv_path)

    # get the folder info
    folder_info = productivity_csv[productivity_csv['id'] == folder_id]
    if not folder_info.empty:
        folder_title = st.text_input("Folder Title", value=folder_info['title'].values[0])
        folder_title = folder_title.strip()
        if saveeditbtn:
            if folder_title != folder_info['title'].values[0]:
                if folder_title in folders:
                    st.error(f"Error: Folder with title '{folder_title}' already exists")
                    return
                elif not valid_value(folder_title):
                    st.error(f"Error: Invalid folder title '{folder_title}'")
                    return
                else:
                    # get the old folder title
                    old_folder_title = folder_info['title'].values[0]

                    ids_to_update = []

                    # find all the rows where folder_id is in the parent column
                    children = productivity_csv[productivity_csv["parent"] == folder_id]
                    child_ids = children['id'].tolist()

                    # extend ids_to_update with the child_ids
                    ids_to_update.extend(child_ids)

                    # check if any of the ids_to_update are in the parent column of productivity_csv
                    grand_children = productivity_csv[productivity_csv["parent"].isin(ids_to_update)]
                    grand_child_ids = grand_children['id'].tolist()

                    # extend ids_to_update with the grand_child_ids
                    ids_to_update.extend(grand_child_ids)

                    # update the folder_dir column for all the rows in ids_to_update
                    for id_to_update in ids_to_update:
                        # only remove the old folder name from the folder_dir and replace with the new folder name
                        # if the old folder name is in the folder_dir
                        if old_folder_title in productivity_csv[productivity_csv['id'] == id_to_update]['folder_dir'].values[0]:
                            productivity_csv.loc[productivity_csv['id'] == id_to_update, 'folder_dir'] = productivity_csv[productivity_csv['id'] == id_to_update]['folder_dir'].values[0].replace(old_folder_title, folder_title)


                    # update the folder title
                    productivity_csv.loc[productivity_csv['id'] == folder_id, 'title'] = folder_title
                    productivity_csv.loc[productivity_csv['id'] == folder_id, 'file_name'] = folder_title
                    productivity_csv.loc[productivity_csv['id'] == folder_id, 'date_updated'] = datetime.datetime.now()

                    # write updated dataframe to csv
                    productivity_csv.to_csv(productivity_csv_path, index=False)

                    # update the folder name in the directory
                    old_folder_path = os.path.join(directory_path, st.session_state.selected_folder_name)
                    new_folder_path = os.path.join(directory_path, folder_title)
                    os.rename(old_folder_path, new_folder_path)

                    success_func("Folder updated")

def edit_project_func(project_id):
    # load the csv file
    productivity_csv = pd.read_csv(productivity_csv_path)

    # get the project info
    project_info = productivity_csv[productivity_csv['id'] == project_id]

    if not project_info.empty:
        # use the project_info to load the json file
        path_to_json = os.path.join(project_info['folder_dir'].values[0], "json_data", project_info['file_name'].values[0])

        with open(path_to_json, "r") as file:
            data = json.load(file)

        # get the project inputs
        title_dict = project_inputs['title']
        description_dict = project_inputs['description']
        status_dict = project_inputs['status']
        priority_dict = project_inputs['priority']
        category_dict = project_inputs['category']
        goal_verb_dict = project_inputs['goal_verb']
        genre_dict = project_inputs['genre']
        use_case_dict = project_inputs['use_case']
        completed_dict = project_inputs['completed']
        datetime_completed_dict = project_inputs['datetime_completed']
        no_start_date_dict = project_inputs['no_start_date']
        start_date_dict = project_inputs['start_date']
        no_due_date_dict = project_inputs['no_due_date']
        due_date_dict = project_inputs['due_date']
        add_time_estimation_dict = project_inputs['estimated_time_to_complete_checkbox']
        estimated_time_to_complete_dict = project_inputs['estimated_time_to_complete']
        attachments_dict = project_inputs['attachments']
        comments_dict = project_inputs['comments']
        if data is not None:
            project = data
            if project['id'] == project_id:
                completed_old_value = project['completed']
                project['completed'] = st.checkbox(
                    completed_dict['label'],
                    value=project['completed'],
                    help=completed_dict['help'],
                    key=f"{project['id']}_completed")
                if project['completed'] and project['completed'] == completed_old_value:
                    project['datetime_completed'] = datetime.strptime(project['datetime_completed'], '%Y-%m-%d')
                    project['datetime_completed'] = st.date_input(
                        datetime_completed_dict['label'],
                        value=project['datetime_completed'],
                        help=datetime_completed_dict['help'],
                        key=f"{project['id']}_datetime_completed")
                elif project['completed'] and project['completed'] != completed_old_value:
                    project['datetime_completed'] = datetime.now().strftime("%Y-%m-%d")
                    project['datetime_completed'] = datetime.strptime(project['datetime_completed'], '%Y-%m-%d')
                    project['datetime_completed'] = st.date_input(
                        datetime_completed_dict['label'],
                        value=project['datetime_completed'],
                        help=datetime_completed_dict['help'],
                        key=f"{project['id']}_datetime_completed")
                project['title'] = st.text_input(
                    title_dict['label'], 
                    value=project['title'],
                    help=title_dict['help'],
                    key=f"{project['id']}_title")
                project['description'] = st.text_area(
                    description_dict['label'],
                    value=project['description'],
                    help=description_dict['help'],
                    key=f"{project['id']}_description")
                status_col, priority_col = st.columns(2)
                project['status'] = status_col.selectbox(
                    status_dict['label'],
                    options = formatted_options(project['status'], status_dict['options']),
                    help=status_dict['help'],
                    key=f"{project['id']}_status")
                project['priority'] = priority_col.number_input(
                    priority_dict['label'],
                    value=project['priority'],
                    help=priority_dict['help'],
                    key=f"{project['id']}_priority")
                st.write("---")
                project['no_start_date'] = st.checkbox(
                    no_start_date_dict['label'],
                    value=project['no_start_date'],
                    help=no_start_date_dict['help'],
                    key=f"{project['id']}_no_start_date")
                if not project['no_start_date']:
                    project['start_date'] = datetime.datetime.strptime(project['start_date'], '%Y-%m-%d')
                    project['start_date'] = st.date_input(
                        start_date_dict['label'],
                        value=project['start_date'],
                        help=start_date_dict['help'],
                        key=f"{project['id']}_start_date")
                project['no_due_date'] = st.checkbox(
                    no_due_date_dict['label'],
                    value=project['no_due_date'],
                    help=no_due_date_dict['help'],
                    key=f"{project['id']}_no_due_date")
                if not project['no_due_date']:
                    project['due_date'] = datetime.datetime.strptime(project['due_date'], '%Y-%m-%d')
                    project['due_date'] = st.date_input(
                        due_date_dict['label'],
                        value=project['due_date'],
                        help=due_date_dict['help'],
                        key=f"{project['id']}_due_date")
                project['estimated_time_to_complete_checkbox'] = st.checkbox(
                    add_time_estimation_dict['label'],
                    value=project['estimated_time_to_complete_checkbox'],
                    help=add_time_estimation_dict['help'],
                    key=f"{project['id']}_estimated_time_to_complete_checkbox")
                add_time_completion_estimates = st.empty()
                if project['estimated_time_to_complete_checkbox']:
                    with add_time_completion_estimates.container():
                        available_units = [unit for unit in time_conversion_factors.keys()]
                        time_completion_units, time_completion_number = st.columns(2)
                        with time_completion_units:
                            unit = st.selectbox(
                                "Unit",
                                options=formatted_options(project['estimated_time_units'], available_units),
                                help=estimated_time_to_complete_dict["help"],
                                key = f"units_{project['id']}",
                            )
                        with time_completion_number:
                            unit_ammount = st.number_input(
                                estimated_time_to_complete_dict['label'],
                                help=estimated_time_to_complete_dict['help'],
                                key = f"duration_{project['id']}",
                                value= project['estimated_time_unit_ammount'],
                                min_value=1
                                )
                        project['estimated_time_to_complete'] = unit_ammount * time_conversion_factors[unit.lower()]
                st.write("---")
                category_col, goal_verb_col = st.columns(2)
                genre_col, use_case_col = st.columns(2)
                project['category'] = category_col.selectbox(
                    category_dict['label'],
                    options = formatted_options(project['category'], category_dict['options']),
                    help=category_dict['help'],
                    key=f"{project['id']}_category")
                project['goal_verb'] = goal_verb_col.selectbox(
                    goal_verb_dict['label'],
                    options = formatted_options(project['goal_verb'], goal_verb_dict['options']),
                    help=goal_verb_dict['help'],
                    key=f"{project['id']}_goal_verb")
                project['genre'] = genre_col.selectbox(
                    genre_dict['label'],
                    options = formatted_options(project['genre'], genre_dict['options']),
                    help=genre_dict['help'],
                    key=f"{project['id']}_genre")
                project['use_case'] = use_case_col.selectbox(
                    use_case_dict['label'],
                    options = formatted_options(project['use_case'], use_case_dict['options']),
                    help=use_case_dict['help'],
                    key=f"{project['id']}_use_case")
                st.write("---")
                comments_col, attachments_col = st.columns(2)
                with comments_col:
                    add_comments = st.text_area(
                        comments_dict['label'],
                        help=comments_dict['help'],
                        placeholder=comments_dict['placeholder']
                    )
                with attachments_col:
                    add_attachments = st.file_uploader(
                        attachments_dict['label'],
                        help=attachments_dict['help'],
                        accept_multiple_files=True
                    )
                task_col, milestone_col, deliverable_col = st.columns(3)
                with task_col:
                    for task in project['tasks']:
                        task['title'] = st.button(f"{task['title']}", key = f"{task['id']}_task_title")
                with milestone_col:
                    for milestone in project['milestones']:
                        milestone['title'] = st.button("Milestone Title")
                with deliverable_col:
                    for deliverable in project['deliverables']:
                        deliverable['title'] = st.button("Deliverable Title")
                if saveeditbtn:
                    try:
                        # update the csv file
                        productivity_csv.loc[productivity_csv['id'] == project_id, 'title'] = project['title']
                        productivity_csv.loc[productivity_csv['id'] == project_id, 'date_updated'] = datetime.datetime.now()
                        productivity_csv.to_csv(productivity_csv_path, index=False)

                        # update timeline.csv
                        timeline_csv = pd.read_csv(timeline_csv_path)
                        timeline_csv.loc[timeline_csv['id'] == project_id, 'title'] = project['title']
                        timeline_csv.loc[timeline_csv['id'] == project_id, 'status'] = project['status']
                        timeline_csv.loc[timeline_csv['id'] == project_id, 'priority'] = project['priority']
                        timeline_csv.loc[timeline_csv['id'] == project_id, 'no_start_date'] = project['no_start_date']
                        timeline_csv.loc[timeline_csv['id'] == project_id, 'start_date'] = project['start_date']
                        timeline_csv.loc[timeline_csv['id'] == project_id, 'no_due_date'] = project['no_due_date']
                        timeline_csv.loc[timeline_csv['id'] == project_id, 'due_date'] = project['due_date']
                        timeline_csv.loc[timeline_csv['id'] == project_id, 'estimated_time_to_complete'] = project['estimated_time_to_complete_checkbox']
                        timeline_csv.loc[timeline_csv['id'] == project_id, 'estimated_duration'] = project['estimated_time_to_complete']
                        timeline_csv.loc[timeline_csv['id'] == project_id, 'completed'] = project['completed']
                        timeline_csv.loc[timeline_csv['id'] == project_id, 'datetime_completed'] = project['datetime_completed']
                        timeline_csv.loc[timeline_csv['id'] == project_id, 'date_last_worked_on'] = datetime.datetime.now()
                        timeline_csv.to_csv(timeline_csv_path, index=False)

                        if add_attachments is not None:
                            for attachment in add_attachments:
                                attachment_id = save_attachment(st.session_state.selected_folder_name, project['id'], attachment)
                                project['attachments'].append(attachment_id)
                        if valid_value(add_comments):
                            comment_id = add_comment_to_item(st.session_state.selected_folder_name, project['id'], add_comments)
                            project['comments'].append(comment_id)
                        #update the json file
                        with open(path_to_json, "w") as file:
                            json.dump(project, file, indent=4, cls=CustomJSONEncoder)
                        success_func("Project edited successfully.")
                    except Exception as e:
                        st.write(f"An error occurred: {e}")
            else:
                print("Error: No folders found in JSON data")
        else:
            print("Error: Could not load JSON data")

def edit_task_func(task_id):
    # load the csv file
    productivity_csv = pd.read_csv(productivity_csv_path)

    # get the task info
    task_info = productivity_csv[productivity_csv['id'] == task_id]

    if not task_info.empty:
        # use the task_info to load the json file
        path_to_json = os.path.join(task_info['folder_dir'].values[0], "json_data", task_info['file_name'].values[0])

        with open(path_to_json, "r") as file:
            data = json.load(file)

        # get the task inputs
        title_dict = task_inputs['title']
        description_dict = task_inputs['description']
        status_dict = task_inputs['status']
        priority_dict = task_inputs['priority']
        category_dict = task_inputs['category']
        goal_verb_dict = task_inputs['goal_verb']
        genre_dict = task_inputs['genre']
        use_case_dict = task_inputs['use_case']
        no_start_date_dict = task_inputs['no_start_date']
        start_date_dict = task_inputs['start_date']
        no_due_date_dict = task_inputs['no_due_date']
        due_date_dict = task_inputs['due_date']
        add_time_estimation_dict = task_inputs['estimated_time_to_complete_checkbox']
        estimated_time_to_complete_dict = task_inputs['estimated_time_to_complete']

        if data is not None:
            task = data
            if task['id'] == task_id:
                task['title'] = st.text_input(
                    title_dict['label'], 
                    value=task['title'],
                    help=title_dict['help'],
                    key=f"{task['id']}_title")
                task['description'] = st.text_area(
                    description_dict['label'],
                    value=task['description'],
                    help=description_dict['help'],
                    key=f"{task['id']}_description")
                status_col, priority_col = st.columns(2)
                task['status'] = status_col.selectbox(
                    status_dict['label'],
                    options=formatted_options(task['status'], status_dict['options']),
                    help=status_dict['help'],
                    key=f"{task['id']}_status")
                task['priority'] = priority_col.number_input(
                    priority_dict['label'],
                    value=task['priority'],
                    help=priority_dict['help'],
                    key=f"{task['id']}_priority")
                st.write("---")
                task['no_start_date'] = st.checkbox(
                    no_start_date_dict['label'],
                    value=task['no_start_date'],
                    help=no_start_date_dict['help'],
                    key=f"{task['id']}_no_start_date")
                if not task['no_start_date']:
                    task['start_date'] = datetime.datetime.strptime(task['start_date'], '%Y-%m-%d')
                    task['start_date'] = st.date_input(
                        start_date_dict['label'],
                        value=task['start_date'],
                        help=start_date_dict['help'],
                        key=f"{task['id']}_start_date")
                task['no_due_date'] = st.checkbox(
                    no_due_date_dict['label'],
                    value=task['no_due_date'],
                    help=no_due_date_dict['help'],
                    key=f"{task['id']}_no_due_date")
                
                if not task['no_due_date']:
                    task['due_date'] = datetime.datetime.strptime(task['due_date'], '%Y-%m-%d')
                    task['due_date'] = st.date_input(
                        due_date_dict['label'],
                        value=task['due_date'],
                        help=due_date_dict['help'],
                        key=f"{task['id']}_due_date")
                    
                task['estimated_time_to_complete_checkbox'] = st.checkbox(
                    add_time_estimation_dict['label'],
                    value=task['estimated_time_to_complete_checkbox'],
                    help=add_time_estimation_dict['help'],
                    key=f"{task['id']}_estimated_time_to_complete_checkbox")
                add_time_completion_estimates = st.empty()
                if task['estimated_time_to_complete_checkbox']:
                    with add_time_completion_estimates.container():
                        available_units = [unit for unit in time_conversion_factors.keys()]
                        time_completion_units, time_completion_number = st.columns(2)
                        with time_completion_units:
                            unit = st.selectbox(
                                "Unit",
                                options=formatted_options(task['estimated_time_units'], available_units),
                                help=estimated_time_to_complete_dict["help"],
                                key = f"units_{task['id']}",
                            )
                        with time_completion_number:
                            unit_ammount = st.number_input(
                                estimated_time_to_complete_dict['label'],
                                help=estimated_time_to_complete_dict['help'],
                                key = f"duration_{task['id']}",
                                value= task['estimated_time_unit_ammount'],
                                min_value=1
                                )
                        task['estimated_time_to_complete'] = unit_ammount * time_conversion_factors[unit.lower()]
                st.write("---")
                category_col, goal_verb_col = st.columns(2)
                genre_col, use_case_col = st.columns(2)
                task['category'] = category_col.selectbox(
                    category_dict['label'],
                    options=formatted_options(task['category'], category_dict['options']),
                    help=category_dict['help'],
                    key=f"{task['id']}_category")
                task['goal_verb'] = goal_verb_col.selectbox(
                    goal_verb_dict['label'],
                    options=formatted_options(task['goal_verb'], goal_verb_dict['options']),
                    help=goal_verb_dict['help'],
                    key=f"{task['id']}_goal_verb")
                task['genre'] = genre_col.selectbox(
                    genre_dict['label'],
                    options=formatted_options(task['genre'], genre_dict['options']),
                    help=genre_dict['help'],
                    key=f"{task['id']}_genre")
                task['use_case'] = use_case_col.selectbox(
                    use_case_dict['label'],
                    options=formatted_options(task['use_case'], use_case_dict['options']),
                    help=use_case_dict['help'],
                    key=f"{task['id']}_use_case")

                if saveeditbtn:
                    try:
                        productivity_csv.loc[productivity_csv['id'] == task_id, 'title'] = task['title']
                        productivity_csv.loc[productivity_csv['id'] == task_id, 'date_updated'] = datetime.datetime.now()
                        productivity_csv.to_csv(productivity_csv_path, index=False)

                        # update timeline.csv
                        timeline_csv = pd.read_csv(timeline_csv_path)
                        timeline_csv.loc[timeline_csv['id'] == task_id, 'title'] = task['title']
                        timeline_csv.loc[timeline_csv['id'] == task_id, 'status'] = task['status']
                        timeline_csv.loc[timeline_csv['id'] == task_id, 'priority'] = task['priority']
                        timeline_csv.loc[timeline_csv['id'] == task_id, 'no_start_date'] = task['no_start_date']
                        timeline_csv.loc[timeline_csv['id'] == task_id, 'start_date'] = task['start_date']
                        timeline_csv.loc[timeline_csv['id'] == task_id, 'no_due_date'] = task['no_due_date']
                        timeline_csv.loc[timeline_csv['id'] == task_id, 'due_date'] = task['due_date']
                        timeline_csv.loc[timeline_csv['id'] == task_id, 'estimated_time_to_complete'] = task['estimated_time_to_complete_checkbox']
                        timeline_csv.loc[timeline_csv['id'] == task_id, 'estimated_duration'] = task['estimated_time_to_complete']
                        timeline_csv.loc[timeline_csv['id'] == task_id, 'date_last_worked_on'] = datetime.datetime.now()
                        timeline_csv.to_csv(timeline_csv_path, index=False)


                        with open(path_to_json, 'w') as outfile:
                            json.dump(task, outfile, cls=CustomJSONEncoder)

                        success_func("Task edited successfully.")
                        
                    except Exception as e:
                        st.write(f'An error occurred: {e}')

def edit_milestone_func(milestone_id):
    # Load the CSV file
    productivity_csv = pd.read_csv(productivity_csv_path)

    # Get the milestone info
    milestone_info = productivity_csv[productivity_csv['id'] == milestone_id]

    if not milestone_info.empty:
        # Use the milestone_info to load the JSON file
        path_to_json = os.path.join(milestone_info['folder_dir'].values[0], "json_data", milestone_info['file_name'].values[0])

        with open(path_to_json, "r") as file:
            data = json.load(file)

        # Get the milestone inputs
        title_dict = milestone_inputs['title']
        description_dict = milestone_inputs['description']
        category_dict = milestone_inputs['category']
        goal_verb_dict = milestone_inputs['goal_verb']
        genre_dict = milestone_inputs['genre']
        use_case_dict = milestone_inputs['use_case']
        no_due_date_dict = milestone_inputs['no_due_date']
        due_date_dict = milestone_inputs['due_date']

        if data is not None:
            milestone = data
            if milestone['id'] == milestone_id:
                milestone['title'] = st.text_input(
                    title_dict['label'], 
                    value=milestone['title'],
                    help=title_dict['help'],
                    key=f"{milestone['id']}_title")
                milestone['description'] = st.text_area(
                    description_dict['label'],
                    value=milestone['description'],
                    help=description_dict['help'],
                    key=f"{milestone['id']}_description")
                st.write("---")
                milestone['no_due_date'] = st.checkbox(
                    no_due_date_dict['label'],
                    value=milestone['no_due_date'],
                    help=no_due_date_dict['help'],
                    key=f"{milestone['id']}_no_due_date")
                if not milestone['no_due_date']:
                    milestone['due_date'] = datetime.datetime.strptime(milestone['due_date'], '%Y-%m-%d')
                    milestone['due_date'] = st.date_input(
                        due_date_dict['label'],
                        value=milestone['due_date'],
                        help=due_date_dict['help'],
                        key=f"{milestone['id']}_due_date")
                st.write("---")
                category_col, goal_verb_col = st.columns(2)
                genre_col, use_case_col = st.columns(2)
                milestone['category'] = category_col.selectbox(
                    category_dict['label'],
                    options=formatted_options(milestone['category'], category_dict['options']),
                    help=category_dict['help'],
                    key=f"{milestone['id']}_category")
                milestone['goal_verb'] = goal_verb_col.selectbox(
                    goal_verb_dict['label'],
                    options=formatted_options(milestone['goal_verb'], goal_verb_dict['options']),
                    help=goal_verb_dict['help'],
                    key=f"{milestone['id']}_goal_verb")
                milestone['genre'] = genre_col.selectbox(
                    genre_dict['label'],
                    options=formatted_options(milestone['genre'], genre_dict['options']),
                    help=genre_dict['help'],
                    key=f"{milestone['id']}_genre")
                milestone['use_case'] = use_case_col.selectbox(
                    use_case_dict['label'],
                    options=formatted_options(milestone['use_case'], use_case_dict['options']),
                    help=use_case_dict['help'],
                    key=f"{milestone['id']}_use_case")
                if saveeditbtn:
                    try:
                        with open(path_to_json, 'w') as outfile:
                            json.dump(milestone, outfile, cls=CustomJSONEncoder)

                        productivity_csv.loc[productivity_csv['id'] == milestone_id, 'title'] = milestone['title']
                        productivity_csv.loc[productivity_csv['id'] == milestone_id, 'date_updated'] = datetime.datetime.now()
                        productivity_csv.to_csv(productivity_csv_path, index=False)

                        # update timeline.csv
                        timeline_csv = pd.read_csv(timeline_csv_path)
                        timeline_csv.loc[timeline_csv['id'] == milestone_id, 'title'] = milestone['title']
                        timeline_csv.loc[timeline_csv['id'] == milestone_id, 'no_due_date'] = milestone['no_due_date']
                        timeline_csv.loc[timeline_csv['id'] == milestone_id, 'due_date'] = milestone['due_date']
                        timeline_csv.loc[timeline_csv['id'] == milestone_id, 'date_last_worked_on'] = datetime.datetime.now()
                        timeline_csv.to_csv(timeline_csv_path, index=False)

                        success_func("Milestone edited successfully.")
                        
                    except Exception as e:
                        st.write(f'An error occurred: {e}')

def edit_deliverable_func(deliverable_id):
    # Load the CSV file
    productivity_csv = pd.read_csv(productivity_csv_path)

    # Get the deliverable info
    deliverable_info = productivity_csv[productivity_csv['id'] == deliverable_id]

    if not deliverable_info.empty:
        # Use the deliverable_info to load the JSON file
        path_to_json = os.path.join(deliverable_info['folder_dir'].values[0], "json_data", deliverable_info['file_name'].values[0])

        with open(path_to_json, "r") as file:
            data = json.load(file)

        # Get the deliverable inputs
        title_dict = deliverable_inputs['title']
        description_dict = deliverable_inputs['description']
        category_dict = deliverable_inputs['category']
        goal_verb_dict = deliverable_inputs['goal_verb']
        genre_dict = deliverable_inputs['genre']
        use_case_dict = deliverable_inputs['use_case']
        no_due_date_dict = deliverable_inputs['no_due_date']
        due_date_dict = deliverable_inputs['due_date']
        quality_criteria_dict = deliverable_inputs['quality_criteria']
        acceptance_criteria_dict = deliverable_inputs['acceptance_criteria']

        if data is not None:
            deliverable = data
            if deliverable['id'] == deliverable_id:
                deliverable['title'] = st.text_input(
                    title_dict['label'], 
                    value=deliverable['title'],
                    help=title_dict['help'],
                    key=f"{deliverable['id']}_title")
                deliverable['description'] = st.text_area(
                    description_dict['label'],
                    value=deliverable['description'],
                    help=description_dict['help'],
                    key=f"{deliverable['id']}_description")
                st.write("---")
                deliverable['no_due_date'] = st.checkbox(
                    no_due_date_dict['label'],
                    value=deliverable['no_due_date'],
                    help=no_due_date_dict['help'],
                    key=f"{deliverable['id']}_no_due_date")
                if not deliverable['no_due_date']:
                    deliverable['due_date'] = datetime.datetime.strptime(deliverable['due_date'], '%Y-%m-%d')
                    deliverable['due_date'] = st.date_input(
                        due_date_dict['label'],
                        value=deliverable['due_date'],
                        help=due_date_dict['help'],
                        key=f"{deliverable['id']}_due_date")
                st.write("---")
                category_col, goal_verb_col = st.columns(2)
                genre_col, use_case_col = st.columns(2)
                deliverable['category'] = category_col.selectbox(
                    category_dict['label'],
                    options=formatted_options(deliverable['category'], category_dict['options']),
                    help=category_dict['help'],
                    key=f"{deliverable['id']}_category")
                deliverable['goal_verb'] = goal_verb_col.selectbox(
                    goal_verb_dict['label'],
                    options=formatted_options(deliverable['goal_verb'], goal_verb_dict['options']),
                    help=goal_verb_dict['help'],
                    key=f"{deliverable['id']}_goal_verb")
                deliverable['genre'] = genre_col.selectbox(
                    genre_dict['label'],
                    options=formatted_options(deliverable['genre'], genre_dict['options']),
                    help=genre_dict['help'],
                    key=f"{deliverable['id']}_genre")
                deliverable['use_case'] = use_case_col.selectbox(
                    use_case_dict['label'],
                    options=formatted_options(deliverable['use_case'], use_case_dict['options']),
                    help=use_case_dict['help'],
                    key=f"{deliverable['id']}_use_case")
                st.write("---")
                deliverable['quality_criteria'] = st.text_area(
                    quality_criteria_dict['label'],
                    value=deliverable['quality_criteria'],
                    help=quality_criteria_dict['help'],
                    key=f"{deliverable['id']}_quality_criteria")
                deliverable['acceptance_criteria'] = st.text_area(
                    acceptance_criteria_dict['label'],
                    value=deliverable['acceptance_criteria'],
                    help=acceptance_criteria_dict['help'],
                    key=f"{deliverable['id']}_acceptance_criteria")

        if saveeditbtn:
            try:
                # Save the edited data back to the JSON file
                with open(path_to_json, 'w') as outfile:
                    json.dump(deliverable, outfile, cls=CustomJSONEncoder)
                
                productivity_csv.loc[productivity_csv['id'] == deliverable_id, 'title'] = deliverable['title']
                productivity_csv.loc[productivity_csv['id'] == deliverable_id, 'date_updated'] = datetime.datetime.now()
                productivity_csv.to_csv(productivity_csv_path, index=False)

                # update the timeline_csv
                timeline_csv = pd.read_csv(timeline_csv_path)
                timeline_csv.loc[timeline_csv['id'] == deliverable_id, 'title'] = deliverable['title']
                timeline_csv.loc[timeline_csv['id'] == deliverable_id, 'no_due_date'] = deliverable['no_due_date']
                timeline_csv.loc[timeline_csv['id'] == deliverable_id, 'due_date'] = deliverable['due_date']
                timeline_csv.loc[timeline_csv['id'] == deliverable_id, 'date_last_worked_on'] = datetime.datetime.now()
                timeline_csv.to_csv(timeline_csv_path, index=False)
                success_func("Deliverable edited successfully.")

            except Exception as e:
                st.write(f'An error occurred: {e}')



##################################
######### SIDEBAR  SETUP #########
##################################

folder_sidebar_area_placeholder = st.sidebar.empty()
project_sidebar_area_placeholder = st.sidebar.empty()

with folder_sidebar_area_placeholder.container():
    st.sidebar.title("Folders")
    folder_sidebar_col1, folder_sidebar_col2 = st.sidebar.columns(2)
    folder_create_button_placeholder = folder_sidebar_col1.empty()
    folder_view_button_placeholder = folder_sidebar_col2.empty()
    folder_select_selector_placeholder = st.sidebar.empty()
    st.sidebar.write("---")

with project_sidebar_area_placeholder.container():
    st.sidebar.title("Projects")
    project_sidebar_col1, project_sidebar_col2 = st.sidebar.columns(2)
    project_create_button_placeholder = project_sidebar_col1.empty()
    project_view_button_placeholder = project_sidebar_col2.empty()
    project_select_selector_placeholder = st.sidebar.empty()
    st.sidebar.write("---")

st.session_state.create_folder = True


folders, folder_data = check_if_folders_exist()
if len(folders) > 0:
    # Create SelectBox for the folders
    selected_folder_name = folder_select_selector_placeholder.selectbox('Select a folder', list(folders.keys()))
    st.session_state.selected_folder = folders[selected_folder_name]
    st.session_state.selected_folder_name = selected_folder_name
else:
    st.session_state.selected_folder = None
    st.session_state.selected_folder_name = None
    folder_select_selector_placeholder.write("No folders found. Create a folder to get started.")

projects, project_data = check_if_projects_exist()
if len(projects) > 0:
    # Create SelectBox for the projects
    selected_project_name = project_select_selector_placeholder.selectbox('Select a project', list(projects.keys()))
    st.session_state.selected_project = projects[selected_project_name]
    st.session_state.selected_project_name = selected_project_name
else:
    st.session_state.selected_project = None
    st.session_state.selected_project_name = None
    project_select_selector_placeholder.write("No projects found. Create a project to get started.")

tasks, task_data = check_if_tasks_exist()
milestones, milestone_data = check_if_milestones_exist()
deliverables, deliverable_data = check_if_deliverables_exist()



##################################
######### MAIN AREA SETUP ########
##################################


mode = None
item = None

page_layout_placeholder_b = st.empty()

with page_layout_placeholder_b.container():
    title_area_b = st.empty()

    home_mode_b = st.empty()
    view_mode_b = st.empty()
    create_mode_b = st.empty()
    edit_mode_b = st.empty()
    delete_mode_b = st.empty()
    buttons_row_b = st.empty()
    separator_b = st.empty()

with home_mode_b.container():
    main_home_area_b = st.empty()
    home_folder_area_b = st.empty()
    home_project_area_b = st.empty()
    home_task_area_b = st.empty()
    home_milestone_area_b = st.empty()
    home_deliverable_area_b = st.empty()

with view_mode_b.container():
    view_folder_area_b = st.empty()
    view_project_area_b = st.empty()
    view_task_area_b = st.empty()
    view_milestone_area_b = st.empty()
    view_deliverable_area_b = st.empty()

with view_folder_area_b.container():
    folder_view_title_b = st.empty()
    folder_view_description_b = st.empty()
    folder_view_projects_b = st.empty()
    folder_view_tasks_b = st.empty()
    folder_view_milestones_b = st.empty()
    folder_view_deliverables_b = st.empty()

with view_project_area_b.container():
    project_view_title_b = st.empty()
    project_view_description_b = st.empty()
    project_view_tasks_b = st.empty()
    project_view_milestones_b = st.empty()
    project_view_deliverables_b = st.empty()

with create_mode_b.container():
    folder_create_mode_b = st.empty()
    project_create_mode_b = st.empty()
    task_create_mode_b = st.empty()
    milestone_create_mode_b = st.empty()

with edit_mode_b.container():
    folder_edit_mode_b = st.empty()
    project_edit_mode_b = st.empty()
    task_edit_mode_b = st.empty()
    milestone_edit_mode_b = st.empty()
    deliverable_edit_mode_b = st.empty()

with delete_mode_b.container():
    folder_delete_mode_b = st.empty()
    project_delete_mode_b = st.empty()
    task_delete_mode_b = st.empty()
    milestone_delete_mode_b = st.empty()
    deliverable_delete_mode_b = st.empty()

with buttons_row_b.container():
    btn_col1b, btn_col2b, btn_col3b, btn_col4b, btn_col5b = st.columns(5)
    button1_placeholder_b = btn_col1b.empty()
    button2_placeholder_b = btn_col2b.empty()
    button3_placeholder_b = btn_col3b.empty()
    button4_placeholder_b = btn_col4b.empty()
    button5_placeholder_b = btn_col5b.empty()

with separator_b.container():
    st.write("---")
    st.write("---")
    st.write("---")





if mode == None:
    title_area_b.title("No Mode")
    main_home_area_b.title("Welcome to the Productivity App")
    create_folder_button_b = button1_placeholder_b.button("Create Folder")
    if create_folder_button_b:
        mode = "create"
        item = "folder"
        

    with home_folder_area_b.container():
        if len(folders) == 0:
            st.write("No folders found. Create one to get started.")
        for folder_name, folder_id in folders.items():
            view_folder_button_b = st.button(folder_name, key=f"view_folder_button_b_{folder_id}")
            if view_folder_button_b:
                item_id = folder_id
                item_name = folder_name
                mode = "view"
                item = "folder"






if mode == "view":
    home_mode_b.empty()
    button1_placeholder_b.empty()
    button2_placeholder_b.empty()
    button3_placeholder_b.empty()
    button4_placeholder_b.empty()
    button5_placeholder_b.empty()

    back_btn_b = button1_placeholder_b.button("Back")
    if back_btn_b:
        mode = None
        item = None
        view_mode_b.empty()
        buttons_row_b.empty()

    if item == None:
        title_area_b.title("View Mode. No Item")
    if item == "folder":
        title_area_b.title(f"View Mode. Folder: {item_name}")
        folder_view_title_b.title(item_id)



        

    if item == "project":
        title_area_b.title("View Mode. Project")
    if item == "task":
        title_area_b.title("View Mode. Task")
    if item == "milestone":
        title_area_b.title("View Mode. Milestone")
    if item == "deliverable":
        title_area_b.title("View Mode. Deliverable")
if mode == "create":
    if item == None:
        title_area_b.title("Create Mode. No Item")
    if item == "folder":
        title_area_b.title("Create Mode. Folder")
    if item == "project":
        title_area_b.title("Create Mode. Project")
    if item == "task":
        title_area_b.title("Create Mode. Task")
    if item == "milestone":
        title_area_b.title("Create Mode. Milestone")
    if item == "deliverable":
        title_area_b.title("Create Mode. Deliverable")
if mode == "edit":
    if item == None:
        title_area_b.title("Edit Mode. No Item")
    if item == "folder":
        title_area_b.title("Edit Mode. Folder")
    if item == "project":
        title_area_b.title("Edit Mode. Project")
    if item == "task":
        title_area_b.title("Edit Mode. Task")
    if item == "milestone":
        title_area_b.title("Edit Mode. Milestone")
    if item == "deliverable":
        title_area_b.title("Edit Mode. Deliverable")
if mode == "delete":
    if item == None:
        title_area_b.title("Delete Mode. No Item")
    if item == "folder":
        title_area_b.title("Delete Mode. Folder")
    if item == "project":
        title_area_b.title("Delete Mode. Project")
    if item == "task":
        title_area_b.title("Delete Mode. Task")
    if item == "milestone":
        title_area_b.title("Delete Mode. Milestone")
    if item == "deliverable":
        title_area_b.title("Delete Mode. Deliverable")




















page_layout_placeholder = st.empty()
## All screens
with page_layout_placeholder.container():
    success_and_warnings_placeholder = st.empty()
    #### Back Button
    home_and_back = st.empty()
    #### Title
    page_title_placeholder = st.empty()
    under_title_placeholder = st.empty()
    #### Divider
    section_splitter = st.empty()
    #### Button Columns
    create_area_placeholder = st.empty()

    btn1_col, btn2_col, btn3_col, btn4_col, btn5_col = st.columns(5)
    button1_placeholder = btn1_col.empty()
    button2_placeholder = btn2_col.empty()
    button3_placeholder = btn3_col.empty()
    button4_placeholder = btn4_col.empty()
    button5_placeholder = btn5_col.empty()

    delete_area_placeholder = st.empty()

    view_folder_area_placeholder = st.empty()
    view_project_area_placeholder = st.empty()
    home_screen_placeholder = st.empty()


## Home Page
with home_screen_placeholder.container():
    gannt_chart_placeholder = st.empty()

    show_folders = st.empty()
    show_projects = st.empty()
    show_tasks = st.empty()
    show_milestones = st.empty()
    show_deliverables = st.empty()

    home_page_col1a, home_page_col2a = st.columns(2)
    column_row_divider = st.empty()
    home_page_col1b, home_page_col2b, home_page_col3b = st.columns(3)

    folder_list_placeholder = home_page_col1a.empty()
    project_list_placeholder = home_page_col2a.empty()
    task_list_placeholder = home_page_col1b.empty()
    milestone_list_placeholder = home_page_col2b.empty()
    deliverable_list_placeholder = home_page_col3b.empty()


    to_do_list_placeholder = st.empty()
    next_up_placeholder = st.empty()
    data_placeholder = st.empty()
## Home Page - Gantt Chart
with gannt_chart_placeholder.container():
    timeline_df, productivity_df = load_data()
    if not timeline_df.empty:
        timeline_data = timeline_df.to_dict('records')
    if not productivity_df.empty:
        productivity_data = productivity_df.to_dict('records')

## View Item Area - under title
with under_title_placeholder.container():
    #### Progress Bar
    item_progress_placeholder = st.empty()
    #### Mark Complete Checkbox
    mark_as_complete_checkbox_placeholder = st.empty()
    #### Status and Priority Columns
    status_col, priority_col = st.columns(2)
    item_status_placeholder = status_col.empty()
    item_priority_placeholder = priority_col.empty()
## View Item Area - Other stuff
with view_project_area_placeholder.container():
    #### Time Columns
    item_time_col1, item_time_col2, item_time_col3, item_time_col4 = st.columns(4)
    item_start_date_placeholder = item_time_col1.empty()
    item_due_date_placeholder = item_time_col2.empty()
    item_estimated_time_to_complete_placeholder = item_time_col3.empty()
    #### Description
    item_description_placeholder = st.empty()
    #### Descriptor Columns
    descriptor_col1, descriptor_col2, descriptor_col3, descriptor_col4 = st.columns(4)
    item_category_placeholder = descriptor_col1.empty()
    item_goal_verb_placeholder = descriptor_col2.empty()
    item_genre_placeholder = descriptor_col3.empty()
    item_use_case_placeholder = descriptor_col4.empty()
    #### Comments and Attachments
    comments_col, attachments_col = st.columns(2)
    item_comments_placeholder = comments_col.empty()
    item_attachments_placeholder = attachments_col.empty()
    add_comment_button_placeholder = st.empty()
    add_attachment_button_placeholder = st.empty()
    #### Tasks, Milestones, and Deliverables
    tasks_col, milestones_col, deliverables_col = st.columns(3)
    item_tasks_placeholder = tasks_col.empty()
    item_milestones_placeholder = milestones_col.empty()
    item_deliverables_placeholder = deliverables_col.empty()
    attachments_in_project_placeholder = st.empty()

with attachments_in_project_placeholder.container():
    attachments_in_project_list = st.empty()

with view_folder_area_placeholder.container():
    projects_in_folder_placeholder = st.empty()
    tasks_in_folder_placeholder = st.empty()
    milestones_in_folder_placeholder = st.empty()
    deliverables_in_folder_placeholder = st.empty()
    attachments_in_folder_placeholder = st.empty()
    comments_in_folder_placeholder = st.empty()

with delete_area_placeholder.container():
    projects_to_be_deleted_title = st.empty()
    projects_to_be_deleted_placeholder = st.empty()
    tasks_to_be_deleted_title = st.empty()
    tasks_to_be_deleted_placeholder = st.empty()
    milestones_to_be_deleted_title = st.empty()
    milestones_to_be_deleted_placeholder = st.empty()
    deliverables_to_be_deleted_title = st.empty()
    deliverables_to_be_deleted_placeholder = st.empty()
    others_to_be_deleted_title = st.empty()
    comments_to_be_deleted_placeholder = st.empty()
    attachments_to_be_deleted_placeholder = st.empty()



if st.session_state.save_successful:
    success_and_warnings_placeholder.success(st.session_state.save_successful)

create_folder = folder_create_button_placeholder.button("Create Folder", disabled=not st.session_state.create_folder, key="create_folder_btn_clicked")
view_folder = folder_view_button_placeholder.button("View Folder", disabled=not st.session_state.view_folder, key="view_folder_btn_clicked")

create_project = project_create_button_placeholder.button("Create Project", disabled=not st.session_state.create_project)
view_project = project_view_button_placeholder.button("View Project", disabled=not st.session_state.view_project)


if create_folder or create_project:
    view_folder_area_placeholder.empty()
    view_project_area_placeholder.empty()
    home_screen_placeholder.empty()
    st.session_state.save_mode = True
    st.session_state.view_mode = False
    st.session_state.edit_mode = False
    st.session_state.delete_mode = False
   
    if create_folder:
        st.session_state.save_folder = True
        st.session_state.save_project = False
    
    if create_project:
        st.session_state.save_project = True
        st.session_state.save_folder = False

if view_folder or view_project:
    create_area_placeholder.empty()
    home_screen_placeholder.empty()
    st.session_state.view_mode = True
    st.session_state.edit_mode = False
    st.session_state.delete_mode = False
    st.session_state.save_mode = False

    if view_folder:
        view_project_area_placeholder.empty()
        st.session_state.view_folder = True
        st.session_state.view_selected_folder = True
        st.session_state.view_project = False
        st.session_state.view_selected_project = False

    if view_project:
        view_folder_area_placeholder.empty()
        st.session_state.view_project = True
        st.session_state.view_selected_project = True
        st.session_state.view_folder = False
        st.session_state.view_selected_folder = False

go_back_button = None

edit_folder_button = None
edit_project_button = None

add_task_button = None
add_milestone_button = None
add_deliverable_button = None

delete_folder_btn = None
delete_project_btn = None
delete_task_btn = None
delete_milestone_btn = None
delete_deliverable_btn = None


if st.session_state.view_mode == True:
    home_screen_placeholder.empty()
    if st.session_state.view_folder == True and st.session_state.view_selected_folder == True:
        go_back_button = home_and_back.button("< Back", key=f"back_btn_{st.session_state.selected_folder}")

        # get row from productivity_csv that matches the selected folder
        folder_info = productivity_csv[productivity_csv['id'] == st.session_state.selected_folder]

        # check if the folder id is in productivity csv parent column. If so, make a separate df with those rows
        children_df = productivity_csv[productivity_csv['parent'] == st.session_state.selected_folder]

        # sort those rows by type
        children_df = children_df.sort_values(by=['identifying_type'])

        # get the folder's children
        projects_in_folder = children_df[children_df['identifying_type'] == "project"]
        tasks_in_folder = children_df[children_df['identifying_type'] == "task"]
        milestones_in_folder = children_df[children_df['identifying_type'] == "milestone"]
        deliverables_in_folder = children_df[children_df['identifying_type'] == "deliverable"]
        attachments_in_folder = children_df[children_df['identifying_type'] == "attachment"]
        comments_in_folder = children_df[children_df['identifying_type'] == "comment"]


        projects_in_folder = projects_in_folder_placeholder.write(projects_in_folder)
        tasks_in_folder = tasks_in_folder_placeholder.write(tasks_in_folder)
        milestones_in_folder = milestones_in_folder_placeholder.write(milestones_in_folder)
        deliverables_in_folder = deliverables_in_folder_placeholder.write(deliverables_in_folder)
        attachments_in_folder = attachments_in_folder_placeholder.write(attachments_in_folder)
        comments_in_folder = comments_in_folder_placeholder.write(comments_in_folder)


        page_title_placeholder.title(folder_info['title'].values[0])
        section_splitter.write("---")

        edit_folder_button = button1_placeholder.button("Edit Folder", key=f"edit_folder_btn_{st.session_state.selected_folder}")
        add_project_button = button2_placeholder.button("Add Project", key=f"add_project_btn_{st.session_state.selected_folder}")
        delete_folder_btn = button3_placeholder.button("Delete Folder", key=f"delete_folder_btn_{st.session_state.selected_folder}")

    if st.session_state.view_project == True and st.session_state.view_selected_project == True:
        go_back_button = home_and_back.button("< Back", key=f"back_btn_{st.session_state.selected_project}")

        # get row from productivity_csv that matches the selected project
        project_info = productivity_csv[productivity_csv['id'] == st.session_state.selected_project]

        # use that row to get the folder_dir and file_name
        folder_dir = project_info['folder_dir'].values[0]
        file_name = project_info['file_name'].values[0]

        # use the folder_dir and file_name to load the json file
        path_to_json = os.path.join(folder_dir, "json_data", file_name)

        with open(path_to_json, "r") as file:
            data = json.load(file)

        section_divider = section_splitter.write("---")

        if data is None:
            item_description_placeholder.write("No data found")
        else:
            item_title = page_title_placeholder.title(data['title'])

            progress_bar = item_progress_placeholder.progress(0.5)

            mark_complete = mark_as_complete_checkbox_placeholder.checkbox("Mark as Complete?", value=False, key=f"mark_complete_{st.session_state.selected_project}")

            edit_project_button = button1_placeholder.button("Edit Project", key=f"edit_project_btn_{st.session_state.selected_project}")
            add_task_button = button2_placeholder.button("Add Task", key=f"add_task_btn_{st.session_state.selected_project}")
            add_milestone_button = button3_placeholder.button("Add Milestone", key=f"add_milestone_btn_{st.session_state.selected_project}")
            add_deliverable_button = button4_placeholder.button("Add Deliverable", key=f"add_deliverable_btn_{st.session_state.selected_project}")
            delete_project_btn = button5_placeholder.button("Delete Project", key=f"delete_project_btn_{st.session_state.selected_project}")

            if valid_value(data['status']):
                item_status_placeholder.write(f"Status: {data['status']}")
            if valid_value(data['priority']):
                item_priority_placeholder.write(f"Priority: {data['priority']}")
            if data['no_start_date'] == False:
                item_start_date_placeholder.write(f"Start Date: {data['start_date']}")
            if data['no_due_date'] == False:
                item_due_date_placeholder.write(f"Due Date: {data['due_date']}")
            if data['estimated_time_to_complete_checkbox'] == True:
                item_estimated_time_to_complete_placeholder.write(f"Estimated Time to Complete: {data['estimated_time_to_complete']}")

            if valid_value(data['description']):
                item_description_placeholder.write(f"Description: {data['description']}")

            if valid_value(data['category']):
                item_category_placeholder.write(f"Category: {data['category']}")
            if valid_value(data['goal_verb']):
                item_goal_verb_placeholder.write(f"Goal Verb: {data['goal_verb']}")
            if valid_value(data['genre']):
                item_genre_placeholder.write(f"Genre: {data['genre']}")
            if valid_value(data['use_case']):
                item_use_case_placeholder.write(f"Use Case: {data['use_case']}")

            if len(data['attachments']) != 0:
                # for each item in data['attachments'], find that item in productivity_csv['id'] column.
                # then, get the file_name and folder_dir from that row
                # then, use those to create a link to the file
                for attachment in data['attachments']:
                    attachment_info = productivity_csv[productivity_csv['id'] == attachment]
                    attachment_file_name = attachment_info['file_name'].values[0]
                    attachment_folder_dir = attachment_info['folder_dir'].values[0]
                    attachment_path = os.path.join(attachment_folder_dir, attachment_file_name)
                    attachment_link = item_attachments_placeholder.markdown(f"[{attachment_file_name}]({attachment_path})")

                    # if the attachment is an image, display it
                    if attachment_file_name.endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
                        attachment_image = item_attachments_placeholder.image(attachment_path)



            if len(data['comments']) != 0:
                for comment in data['comments']:
                    comment_info = productivity_csv[productivity_csv['id'] == comment]
                    comment_file_name = comment_info['file_name'].values[0]
                    comment_folder_dir = comment_info['folder_dir'].values[0]
                    comment_path = os.path.join(comment_folder_dir, comment_file_name)
                    comment_link = item_comments_placeholder.markdown(f"[{comment_file_name}]({comment_path})")


if go_back_button:
    st.session_state.clear()
    st.experimental_rerun()

if edit_project_button or edit_folder_button:
    home_and_back.empty()
    home_screen_placeholder.empty()
    view_folder_area_placeholder.empty()
    view_project_area_placeholder.empty()
    page_title_placeholder.empty()
    under_title_placeholder.empty()
    create_area_placeholder.empty()
    st.session_state.edit_mode = True
    st.session_state.view_mode = False
    st.session_state.delete_mode = False
    st.session_state.save_mode = False

    if edit_folder_button:
        st.session_state.edit_folder = True
        st.session_state.edit_selected_folder = True
    if edit_project_button:
        st.session_state.edit_project = True
        st.session_state.edit_selected_project = True

if delete_folder_btn or delete_project_btn or delete_task_btn or delete_milestone_btn or delete_deliverable_btn:
    home_and_back.empty()
    home_screen_placeholder.empty()
    view_folder_area_placeholder.empty()
    view_project_area_placeholder.empty()
    page_title_placeholder.empty()
    under_title_placeholder.empty()
    create_area_placeholder.empty()
    st.session_state.delete_mode = True
    st.session_state.view_mode = False
    st.session_state.edit_mode = False
    st.session_state.save_mode = False

    if delete_folder_btn:
        st.session_state.delete_folder = True
        st.session_state.delete_selected_folder = True
    if delete_project_btn:
        st.session_state.delete_project = True
        st.session_state.delete_selected_project = True
    if delete_task_btn:
        st.session_state.delete_task = True
        st.session_state.delete_selected_task = True
    if delete_milestone_btn:
        st.session_state.delete_milestone = True
        st.session_state.delete_selected_milestone = True
    if delete_deliverable_btn:
        st.session_state.delete_deliverable = True
        st.session_state.delete_selected_deliverable = True

if add_task_button or add_milestone_button or add_deliverable_button:
    home_and_back.empty()
    home_screen_placeholder.empty()
    view_folder_area_placeholder.empty()
    view_project_area_placeholder.empty()
    page_title_placeholder.empty()
    under_title_placeholder.empty()
    create_area_placeholder.empty()
    st.session_state.save_mode = True
    st.session_state.view_mode = False
    st.session_state.edit_mode = False
    st.session_state.delete_mode = False
    if add_task_button:
        st.session_state.save_task = True
    if add_milestone_button:
        st.session_state.save_milestone = True
    if add_deliverable_button:
        st.session_state.save_deliverable = True

if st.session_state.save_mode == True or st.session_state.edit_mode == True or st.session_state.delete_mode == True:
    button1_placeholder.empty()
    button2_placeholder.empty()
    button3_placeholder.empty()
    button4_placeholder.empty()
    button5_placeholder.empty()
    if st.session_state.save_mode == True:
        savebtn = button4_placeholder.button("Save", disabled=not st.session_state.save_mode, key=f"save_btn_{st.session_state.selected_project}")
        cancelbtn = button5_placeholder.button("Cancel", disabled=not st.session_state.save_mode, key=f"cancel_btn_{st.session_state.selected_project}")

        if cancelbtn:
            st.session_state.clear()
            st.experimental_rerun()
        if st.session_state.save_folder == True:
            page_title_placeholder.title("Add New Folder")
            with create_area_placeholder.container():
                add_new_folder_data()
        elif st.session_state.save_project == True:
            page_title_placeholder.title("Add New Project")
            with create_area_placeholder.container():
                add_new_project_data()
        elif st.session_state.save_task == True:
            page_title_placeholder.title("Add New Task")
            with create_area_placeholder.container():
                add_new_task_data()
        elif st.session_state.save_milestone == True:
            page_title_placeholder.title("Add New Milestone")
            with create_area_placeholder.container():
                add_new_milestone_data()
        elif st.session_state.save_deliverable == True:
            page_title_placeholder.title("Add New Deliverable")
            with create_area_placeholder.container():
                add_new_deliverable_data()

    if st.session_state.edit_mode == True:
        saveeditbtn = button4_placeholder.button("Save", disabled=not st.session_state.edit_mode, key=f"save_edit_btn_{st.session_state.selected_project}")
        canceleditbtn = button5_placeholder.button("Cancel", disabled=not st.session_state.edit_mode, key=f"cancel_edit_btn_{st.session_state.selected_project}")

        if canceleditbtn:
            st.session_state.clear()
            st.experimental_rerun()
        if st.session_state.edit_folder == True and st.session_state.edit_selected_folder == True:
            page_title_placeholder.title("Edit Folder")
            st.session_state.save_folder = True
            with create_area_placeholder.container():
                edit_folder_func(st.session_state.selected_folder)
        elif st.session_state.edit_project == True and st.session_state.edit_selected_project == True:
            page_title_placeholder.title("Edit Project")
            st.session_state.save_project = True
            with create_area_placeholder.container():
                edit_project_func(st.session_state.selected_project)
        elif st.session_state.edit_task == True and st.session_state.edit_selected_task == True:
            page_title_placeholder.title("Edit Task")
            st.session_state.save_task = True
            with create_area_placeholder.container():
                edit_task_func(st.session_state.selected_task)
        elif st.session_state.edit_milestone == True and st.session_state.edit_selected_milestone == True:
            page_title_placeholder.title("Edit Milestone")
            st.session_state.save_milestone = True
            with create_area_placeholder.container():
                edit_milestone_func(st.session_state.selected_milestone)
        elif st.session_state.edit_deliverable == True and st.session_state.edit_selected_deliverable == True:
            page_title_placeholder.title("Edit Deliverable")
            st.session_state.save_deliverable = True
            with create_area_placeholder.container():
                edit_deliverable_func(st.session_state.selected_deliverable)

    if st.session_state.delete_mode == True:
        if st.session_state.delete_folder == True and st.session_state.delete_selected_folder == True:
            page_title_placeholder.title("Delete Folder?")
            deletebtn = button4_placeholder.button("Delete", disabled=not st.session_state.delete_mode, key=f"delete_for_sure_folder_btn_{st.session_state.selected_folder}")
            cancelbtn = button5_placeholder.button("Cancel", disabled=not st.session_state.delete_mode, key=f"cancel_delete_folder_btn_{st.session_state.selected_folder}")

            # find all the rows in productivity_csv where the parent column matched the selected_folder
            # then, get the id column from those rows and turn it into a df
            children_df = productivity_csv[productivity_csv['parent'] == st.session_state.selected_folder]
            # sort those rows by type
            children_df = children_df.sort_values(by=['identifying_type'])
            # get the folder's children
            projects_in_folder = children_df[children_df['identifying_type'] == "project"]
            tasks_in_folder = children_df[children_df['identifying_type'] == "task"]
            milestones_in_folder = children_df[children_df['identifying_type'] == "milestone"]
            deliverables_in_folder = children_df[children_df['identifying_type'] == "deliverable"]
            attachments_in_folder = children_df[children_df['identifying_type'] == "attachment"]
            comments_in_folder = children_df[children_df['identifying_type'] == "comment"]

            # turn each of those dfs into a list of titles
            projects_in_folder_list = projects_in_folder['title'].tolist()
            tasks_in_folder_list = tasks_in_folder['title'].tolist()
            milestones_in_folder_list = milestones_in_folder['title'].tolist()
            deliverables_in_folder_list = deliverables_in_folder['title'].tolist()
            attachments_in_folder_list = attachments_in_folder['title'].tolist()
            comments_in_folder_list = comments_in_folder['title'].tolist()

            projects_to_be_deleted_title.write("##### Projects to be deleted: ")
            projects_to_be_deleted_placeholder.write(projects_in_folder_list)
            tasks_to_be_deleted_title.write("##### Tasks to be deleted: ")
            tasks_to_be_deleted_placeholder.write(tasks_in_folder_list)
            milestones_to_be_deleted_title.write("##### Milestones to be deleted: ")
            milestones_to_be_deleted_placeholder.write(milestones_in_folder_list)
            deliverables_to_be_deleted_title.write("##### Deliverables to be deleted: ")
            deliverables_to_be_deleted_placeholder.write(deliverables_in_folder_list)
            others_to_be_deleted_title.write("##### Other items to be deleted: ")
            comments_to_be_deleted_placeholder.write(comments_in_folder_list)
            attachments_to_be_deleted_placeholder.write(attachments_in_folder_list)

            success_and_warnings_placeholder.warning(f"Are you sure you want to delete folder {st.session_state.selected_folder_name}?")

            if deletebtn:
                try:
                    remove_folder(st.session_state.selected_folder)
                    success_func("Folder deleted successfully.")
                except Exception as e:
                    success_and_warnings_placeholder.write(f"An error occurred: {e}")
            elif cancelbtn:
                st.session_state.delete_mode = False
                st.session_state.delete_folder = False
                st.session_state.delete_selected_folder = False
                st.experimental_rerun()

        elif st.session_state.delete_project == True and st.session_state.delete_selected_project == True:
            page_title_placeholder.title("Delete Project?")
            success_and_warnings_placeholder.warning(f"Are you sure you want to delete {st.session_state.selected_project_name}?")
            deletebtn = button4_placeholder.button("Delete", disabled=not st.session_state.delete_mode, key=f"delete_for_sure_project_btn_{st.session_state.selected_project}")
            cancelbtn = button5_placeholder.button("Cancel", disabled=not st.session_state.delete_mode, key=f"cancel_delete_project_btn_{st.session_state.selected_project}")
            if deletebtn:
                try:
                    remove_project(st.session_state.selected_project)
                    success_func("Project deleted successfully.")
                except Exception as e:
                    success_and_warnings_placeholder.write(f"An error occurred: {e}")
            elif cancelbtn:
                st.session_state.delete_mode = False
                st.session_state.delete_project = False
                st.session_state.delete_selected_project = False
                st.experimental_rerun()
        elif st.session_state.delete_task ==True and st.session_state.delete_selected_task == True:
            page_title_placeholder.title("Delete Task?")
            success_and_warnings_placeholder.warning(f"Are you sure you want to delete {st.session_state.selected_task_name}?")
            deletebtn = button4_placeholder.button("Delete", disabled=not st.session_state.delete_mode, key=f"delete_for_sure_task_btn_{st.session_state.selected_task}")
            cancelbtn = button5_placeholder.button("Cancel", disabled=not st.session_state.delete_mode, key=f"cancel_delete_task_btn_{st.session_state.selected_task}")

            if deletebtn:
                try:
                    remove_task(st.session_state.selected_task)
                    success_func("Task deleted successfully.")
                except Exception as e:
                    success_and_warnings_placeholder.write(f"An error occurred: {e}")
            elif cancelbtn:
                st.session_state.delete_mode = False
                st.session_state.delete_task = False
                st.session_state.delete_selected_task = False
                st.experimental_rerun()

        elif st.session_state.delete_milestone ==True and st.session_state.delete_selected_milestone == True:
            page_title_placeholder.title("Delete Milestone?")
            success_and_warnings_placeholder.warning(f"Are you sure you want to delete {st.session_state.selected_milestone_name}?")
            deletebtn = button4_placeholder.button("Delete", disabled=not st.session_state.delete_mode, key=f"delete_for_sure_milestone_btn_{st.session_state.selected_milestone}")
            cancelbtn = button5_placeholder.button("Cancel", disabled=not st.session_state.delete_mode, key=f"cancel_delete_milestone_btn_{st.session_state.selected_milestone}")
            if deletebtn:
                try:
                    remove_milestone(st.session_state.selected_milestone)
                    success_func("Milestone deleted successfully.")
                except Exception as e:
                    success_and_warnings_placeholder.write(f"An error occurred: {e}")
            elif cancelbtn:
                st.session_state.delete_mode = False
                st.session_state.delete_milestone = False
                st.session_state.delete_selected_milestone = False
                st.experimental_rerun()
        elif st.session_state.delete_deliverable ==True and st.session_state.delete_selected_deliverable == True:
            page_title_placeholder.title("Delete Deliverable?")
            success_and_warnings_placeholder.warning(f"Are you sure you want to delete {st.session_state.selected_deliverable_name}?")
            deletebtn = button4_placeholder.button("Delete", disabled=not st.session_state.delete_mode, key=f"delete_for_sure_deliverable_btn_{st.session_state.selected_deliverable}")
            cancelbtn = button5_placeholder.button("Cancel", disabled=not st.session_state.delete_mode, key=f"cancel_delete_deliverable_btn_{st.session_state.selected_deliverable}")
            if deletebtn:
                try:
                    remove_deliverable(st.session_state.selected_deliverable)
                    success_func("Deliverable deleted successfully.")
                except Exception as e:
                    success_and_warnings_placeholder.write(f"An error occurred: {e}")
            elif cancelbtn:
                st.session_state.delete_mode = False
                st.session_state.delete_deliverable = False
                st.session_state.delete_selected_deliverable = False
                st.experimental_rerun()

if st.session_state.delete_mode == False and st.session_state.save_mode == False and st.session_state.edit_mode == False and st.session_state.view_mode == False:
    view_project_area_placeholder.empty()
    view_folder_area_placeholder.empty()
    create_area_placeholder.empty()
    under_title_placeholder.empty()
    home_and_back.empty()
    button1_placeholder.empty()
    button2_placeholder.empty()
    button3_placeholder.empty()
    button4_placeholder.empty()
    button5_placeholder.empty()

    page_title_placeholder.title("Productivity Tracker Home")
    section_splitter.write("---")

    # organize productivity_csv by type
    folders = {}
    projects = {}
    tasks = {}
    milestones = {}
    deliverables = {}
    attachments = {}
    comments = {}

    # make the dictionaries organized like this: {id: {title: title, parent: parent, folder_dir: folder_dir, file_name: file_name}}
    for index, row in productivity_csv.iterrows():
        if row['identifying_type'] == "folder":
            folders[row['id']] = {'title': row['title'], 'parent': row['parent'], 'folder_dir': row['folder_dir'], 'file_name': row['file_name'] }
        elif row['identifying_type'] == "project":
            projects[row['id']] = {'title': row['title'], 'parent': row['parent'], 'folder_dir': row['folder_dir'], 'file_name': row['file_name'] }
        elif row['identifying_type'] == "task":
            tasks[row['id']] = {'title': row['title'], 'parent': row['parent'], 'folder_dir': row['folder_dir'], 'file_name': row['file_name'] }
        elif row['identifying_type'] == "milestone":
            milestones[row['id']] = {'title': row['title'], 'parent': row['parent'], 'folder_dir': row['folder_dir'], 'file_name': row['file_name'] }
        elif row['identifying_type'] == "deliverable":
            deliverables[row['id']] = {'title': row['title'], 'parent': row['parent'], 'folder_dir': row['folder_dir'], 'file_name': row['file_name'] }
        elif row['identifying_type'] == "attachment":
            attachments[row['id']] = {'title': row['title'], 'parent': row['parent'], 'folder_dir': row['folder_dir'], 'file_name': row['file_name'] }
        elif row['identifying_type'] == "comment":
            comments[row['id']] = {'title': row['title'], 'parent': row['parent'], 'folder_dir': row['folder_dir'], 'file_name': row['file_name'] }





    with folder_list_placeholder.container():
        st.write("### Folders")
        if len(folders) == 0:
            st.write("No folders found. Create one to get started.")
        for folder_id, folder_dict in folders.items():
            folder_title = folder_dict['title']
            view_folder_button = st.button(folder_title, key=f"view_folder_button_{folder_id}")
            if view_folder_button:
                st.session_state.selected_folder = folder_id
                st.session_state.selected_folder_name = folder_title
                st.session_state.view_mode = True
                st.session_state.view_selected_folder = True
                st.view_selected_folder = True
                st.experimental_rerun()
        

    with project_list_placeholder.container():
        st.write("### Projects")
        if len(projects) == 0:
            st.write("No projects found. Create one to get started.")
        for project_id, project_dict in projects.items():
            project_title = project_dict['title']
            view_project_button = st.button(project_title, key=f"view_project_button_{project_id}")
            if view_project_button:
                st.session_state.selected_project = project_id
                st.session_state.selected_project_name = project_title
                st.session_state.selected_folder = project_dict['parent']
                st.session_state.selected_folder_name = folders[project_dict['parent']]['title']
                st.session_state.view_mode = True
                st.session_state.view_project = True
                st.session_state.view_selected_project = True
                st.view_selected_project = True
                st.experimental_rerun()
        
    column_row_divider.write("---")







    with task_list_placeholder.container():
        st.write("#### Tasks")
        if len(tasks) == 0:
            st.write("No tasks found. Create one to get started.")
        for task_id, task_dict in tasks.items():
            task_title = task_dict['title']
            view_task_button = st.button(task_title, key=f"view_task_button_{task_id}")
        if view_task_button:
            true_keys = ["view_mode", "view_task", "view_selected_task"]
            false_keys = ["view_project", "view_selected_project", "view_folder", "view_selected_folder"]
            ids = {
                "selected_task": task_id,
                "selected_project": task_dict['parent'],
                "selected_folder": projects[task_dict['parent']]['parent'],
            }
            names = {
                "selected_task_name": task_title,
                "selected_project_name": projects[task_dict['parent']]['title'],
                "selected_folder_name": folders[projects[task_dict['parent']]['parent']]['title'],
            }
            set_session_states(true_keys, false_keys, ids, names)


        

    with milestone_list_placeholder.container():
        st.write("#### Milestones")
        if len(milestones) == 0:
            st.write("No milestones found. Create one to get started.")
        for milestone_id, milestone_dict in milestones.items():
            milestone_title = milestone_dict['title']
            view_milestone_button = st.button(milestone_title, key=f"view_milestone_button_{milestone_id}")
            if view_milestone_button:
                st.session_state.selected_milestone = milestone_id
                st.session_state.selected_milestone_name = milestone_title
                st.session_state.selected_project = milestone_dict['parent']
                st.session_state.selected_project_name = projects[milestone_dict['parent']]['title']
                st.session_state.selected_folder = projects[milestone_dict['parent']]['parent']  
                st.session_state.selected_folder_name = folders[projects[milestone_dict['parent']]['parent']]['title']
                st.session_state.view_mode = True
                st.session_state.view_milestone = True
                st.session_state.view_selected_milestone = True
                st.experimental_rerun()

        

    with deliverable_list_placeholder.container():
        st.write("#### Deliverables")
        if len(deliverables) == 0:
            st.write("No deliverables found. Create one to get started.")
        for deliverable_id, deliverable_dicts in deliverables.items():
            deliverable_title = deliverable_dicts['title']
            view_deliverable_button = st.button(deliverable_title, key=f"view_deliverable_button_{deliverable_id}")
            if view_deliverable_button:
                st.session_state.selected_deliverable = deliverable_id
                st.session_state.selected_deliverable_name = deliverable_title
                st.session_state.selected_project = deliverable_dicts['parent']
                st.session_state.selected_project_name = projects[deliverable_dicts['parent']]['title']
                st.session_state.selected_folder = projects[deliverable_dicts['parent']]['parent']  
                st.session_state.selected_folder_name = folders[projects[deliverable_dicts['parent']]['parent']]['title']
                st.session_state.view_mode = True
                st.session_state.view_deliverable = True
                st.session_state.view_selected_deliverable = True
                st.view_selected_deliverable = True
                st.experimental_rerun()


st.write("---")
with st.expander("Raw Data"):
    st.dataframe(productivity_csv, use_container_width=True)