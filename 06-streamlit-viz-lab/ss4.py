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

# make streamlit wide
st.set_page_config(layout="wide")

edit_delete_selected_session_states = ["delete_selected_folder", "delete_selected_project", "delete_selected_task",  "delete_selected_milestone", "delete_selected_deliverable", "edit_selected_folder", "edit_selected_project", "edit_selected_task", "edit_selected_milestone", "edit_selected_deliverable"]
selected_session_states = ["selected_folder", "selected_folder_name", "selected_project", "selected_project_name", "selected_task", "selected_task_name","selected_milestone", "selected_milestone_name", "selected_deliverable", "selected_deliverable_name"]
view_session_stated = ["view_mode", "view_selected_project", "view_project"]
create_session_states = ["create_folder", "create_project", "create_task", "create_milestone", "create_deliverable"]
edit_session_states = ["edit_mode", "edit_folder", "edit_project", "edit_task", "edit_milestone", "edit_deliverable"]
delete_session_states = ["delete_mode", "delete_folder", "delete_project", "delete_task", "delete_milestone", "delete_deliverable"]
save_session_states = ["save_mode", "save_successful", "save_folder", "save_project", "save_task", "save_milestone", "save_deliverable"]
previously_selected_session_states = ["prev_selected_project", "prev_selected_task", "prev_selected_milestone", "prev_selected_deliverable"]

# combine all the session_state lists into one list

session_states = edit_delete_selected_session_states + selected_session_states + create_session_states + edit_session_states + delete_session_states + save_session_states + previously_selected_session_states + view_session_stated
    
for session_state in session_states:
    if session_state not in st.session_state:
        st.session_state[session_state] = False


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


directory_path = "productivity"
if not os.path.exists(directory_path):
    os.makedirs(directory_path)

csv_folder = "csvs"
if not os.path.exists(os.path.join(directory_path, csv_folder)):
    os.makedirs(os.path.join(directory_path, csv_folder))

productivity_csv_path, relationships_csv_path, timeline_csv_path = create_csvs(directory_path, csv_folder)
productivity_csv = pd.read_csv(productivity_csv_path)
relationships_csv = pd.read_csv(relationships_csv_path)
timeline_csv = pd.read_csv(timeline_csv_path)


def save_comment_to_md_file(selected_folder_name, selected_item_name, comment, comment_id):
    folder_dir = f"{directory_path}/{selected_folder_name}/comments/{selected_item_name}"
    if not os.path.exists(folder_dir):
        os.makedirs(folder_dir)
    file_name = f"comment_{comment_id}.md"
    md_file_path = os.path.join(folder_dir, file_name)
    with open(md_file_path, "w") as f:
        f.write(comment)
    return folder_dir, file_name

def add_comment_to_item(selected_folder_name, selected_item_name, selected_item, comment, selected_item_type):
    comment_id = make_safe()
    folder_dir, file_name = save_comment_to_md_file(selected_folder_name, selected_item_name, comment, comment_id)

    # add comment to relationships.csv
    new_relationships_csv_data = {
        "parent_id": [selected_item],
        "parent_type": [selected_item_type],
        "child_id": [comment_id],
        "child_type": ["comment"]
    }
    new_relationships_csv = pd.DataFrame(new_relationships_csv_data)
    new_relationships_csv.to_csv(relationships_csv_path, mode="a", header=False, index=False)

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
        "title": [comment_preview]
    }
    new_comment_csv = pd.DataFrame(new_comment_csv_data)
    new_comment_csv.to_csv(productivity_csv_path, mode="a", header=False, index=False)

    return comment_id


def save_attachment_to_file(selected_folder_name, selected_item_name, file):
    if file.type == "application/pdf":
        folder_dir = f"{directory_path}/{selected_folder_name}/attachments/{selected_item_name}/pdfs"
    elif file.type == "image/png" or file.type == "image/jpeg":
        folder_dir = f"{directory_path}/{selected_folder_name}/attachments/{selected_item_name}/images"
    elif file.type == "text/plain":
        folder_dir = f"{directory_path}/{selected_folder_name}/attachments/{selected_item_name}/text"
    else:
        folder_dir = f"{directory_path}/{selected_folder_name}/attachments/{selected_item_name}/other"
    if not os.path.exists(folder_dir):
        os.makedirs(folder_dir)
    file_name = file.name
    file_path = os.path.join(folder_dir, file_name)
    with open(file_path, "wb") as f:
        f.write(file.getbuffer())
    return folder_dir, file_name



def save_attachment(selected_folder_name, selected_item_name, selected_item, file, selected_item_type):
    attachment_id = make_safe()
    folder_dir, file_name = save_attachment_to_file(selected_folder_name, selected_item_name, file)

    # add attachment to relationships.csv
    new_relationships_csv_data = {
        "parent_id": [selected_item],
        "parent_type": [selected_item_type],
        "child_id": [attachment_id],
        "child_type": ["attachment"]
    }
    new_relationships_csv = pd.DataFrame(new_relationships_csv_data)
    new_relationships_csv.to_csv(relationships_csv_path, mode="a", header=False, index=False)

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
        "title": [file_name]
    }
    new_attachment_csv = pd.DataFrame(new_attachment_csv_data)
    new_attachment_csv.to_csv(productivity_csv_path, mode="a", header=False, index=False)

    return attachment_id


folder_sidebar_area_placeholder = st.sidebar.empty()
project_sidebar_area_placeholder = st.sidebar.empty()
task_sidebar_area_placeholder = st.sidebar.empty()
milestone_sidebar_area_placeholder = st.sidebar.empty()
deliverable_sidebar_area_placeholder = st.sidebar.empty()

with folder_sidebar_area_placeholder.container():
    st.sidebar.title("Folders")
    folder_create_button_placeholder = st.sidebar.empty()
    folder_select_selector_placeholder = st.sidebar.empty()
    folder_sidebar_col1, folder_sidebar_col2 = st.sidebar.columns(2)
    edit_folder_btn_placeholder = folder_sidebar_col1.empty()
    delete_folder_btn_placeholder = folder_sidebar_col2.empty()
    st.sidebar.write("---")

with project_sidebar_area_placeholder.container():
    st.sidebar.title("Projects")
    project_create_button_placeholder = st.sidebar.empty()
    project_view_button_placeholder = st.sidebar.empty()
    project_select_selector_placeholder = st.sidebar.empty()
    project_sidebar_col1, project_sidebar_col2 = st.sidebar.columns(2)
    edit_project_btn_placeholder = project_sidebar_col1.empty()
    delete_project_btn_placeholder = project_sidebar_col2.empty()
    st.sidebar.write("---")

with task_sidebar_area_placeholder.container():
    st.sidebar.title("Tasks")
    task_create_button_placeholder = st.sidebar.empty()
    task_select_selector_placeholder = st.sidebar.empty()
    task_sidebar_col1, task_sidebar_col2 = st.sidebar.columns(2)
    edit_task_btn_placeholder = task_sidebar_col1.empty()
    delete_task_btn_placeholder = task_sidebar_col2.empty()
    st.sidebar.write("---")

with milestone_sidebar_area_placeholder.container():
    st.sidebar.title("Milestones")
    milestone_create_button_placeholder = st.sidebar.empty()
    milestone_select_selector_placeholder = st.sidebar.empty()
    milestone_sidebar_col1, milestone_sidebar_col2 = st.sidebar.columns(2)
    edit_milestone_btn_placeholder = milestone_sidebar_col1.empty()
    delete_milestone_btn_placeholder = milestone_sidebar_col2.empty()
    st.sidebar.write("---")

with deliverable_sidebar_area_placeholder.container():
    st.sidebar.title("Deliverables")
    deliverable_create_button_placeholder = st.sidebar.empty()
    deliverable_select_selector_placeholder = st.sidebar.empty()
    deliverable_sidebar_col1, deliverable_sidebar_col2 = st.sidebar.columns(2)
    edit_deliverable_btn_placeholder = deliverable_sidebar_col1.empty()
    delete_deliverable_btn_placeholder = deliverable_sidebar_col2.empty()




productivity_data = productivity_csv
relationships_data = relationships_csv

st.session_state.create_folder = True

# Filter by identifying_type for folder
folder_data = productivity_csv[productivity_csv['identifying_type'] == 'folder'].sort_values(by=['date_updated'], ascending=False)

# Create a dictionary of folder titles and ids from the csv file
folders = {row["title"]: row["id"] for _, row in folder_data.iterrows()}

# If no folder in the csv, selected_folder will be None
if len(folder_data) == 0:
    st.session_state.selected_folder = None
    st.session_state.edit_folder = False
    st.session_state.delete_folder = False

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

    st.session_state.selected_folder = folder_data.iloc[0]['id']
    st.session_state.selected_folder_name = folder_data.iloc[0]['title']
        
    # Create SelectBox for the folders
    selected_folder_name = folder_select_selector_placeholder.selectbox('Select a folder', list(folders.keys()))
    st.session_state.selected_folder = folders[selected_folder_name]
    st.session_state.selected_folder_name = selected_folder_name





project_data = productivity_csv[productivity_csv['identifying_type'] == 'project'].sort_values(by=['date_updated'], ascending=False)

# get all the rows from relationships_cse where parent_id == selected_folder
project_relationships_data = relationships_csv[relationships_csv['parent_id'] == st.session_state.selected_folder]

# now filter project_data to have only rows whose id is in project_relationships_data['child_id']
project_data = project_data[project_data['id'].isin(project_relationships_data['child_id'])]

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

    # Create SelectBox for the projects
    selected_project_name = project_select_selector_placeholder.selectbox('Select a project', list(projects.keys()))
    st.session_state.selected_project = projects[selected_project_name]
    st.session_state.selected_project_name = selected_project_name



task_data = productivity_csv[productivity_csv['identifying_type'] == 'task'].sort_values(by=['date_updated'], ascending=False)

# get all the rows from relationships_cse where parent_id == selected_project
task_relationships_data = relationships_csv[relationships_csv['parent_id'] == st.session_state.selected_project]

# now filter task_data to have only rows whose id is in task_relationships_data['child_id']
task_data = task_data[task_data['id'].isin(task_relationships_data['child_id'])]

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

    # Create SelectBox for the tasks
    selected_task_name = task_select_selector_placeholder.selectbox('Select a task', list(tasks.keys()))
    st.session_state.selected_task = tasks[selected_task_name]
    st.session_state.selected_task_name = selected_task_name



milestone_data = productivity_csv[productivity_csv['identifying_type'] == 'milestone'].sort_values(by=['date_updated'], ascending=False)

# get all the rows from relationships_cse where parent_id == selected_project
milestone_relationships_data = relationships_csv[relationships_csv['parent_id'] == st.session_state.selected_project]

# now filter milestone_data to have only rows whose id is in milestone_relationships_data['child_id']
milestone_data = milestone_data[milestone_data['id'].isin(milestone_relationships_data['child_id'])]

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

    # Create SelectBox for the milestones
    selected_milestone_name = milestone_select_selector_placeholder.selectbox('Select a milestone', list(milestones.keys()))
    st.session_state.selected_milestone = milestones[selected_milestone_name]
    st.session_state.selected_milestone_name = selected_milestone_name



deliverable_data = productivity_csv[productivity_csv['identifying_type'] == 'deliverable'].sort_values(by=['date_updated'], ascending=False)

# get all the rows from relationships_cse where parent_id == selected_project
deliverable_relationships_data = relationships_csv[relationships_csv['parent_id'] == st.session_state.selected_project]

# now filter deliverable_data to have only rows whose id is in deliverable_relationships_data['child_id']
deliverable_data = deliverable_data[deliverable_data['id'].isin(deliverable_relationships_data['child_id'])]

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

    # Create SelectBox for the deliverables
    selected_deliverable_name = deliverable_select_selector_placeholder.selectbox('Select a deliverable', list(deliverables.keys()))
    st.session_state.selected_deliverable = deliverables[selected_deliverable_name]
    st.session_state.selected_deliverable_name = selected_deliverable_name








create_folder = folder_create_button_placeholder.button("Create Folder", disabled=not st.session_state.create_folder, key="create_folder_btn_clicked")
edit_folder = edit_folder_btn_placeholder.button("Edit Folder", disabled=not st.session_state.edit_folder)
delete_folder_btn = delete_folder_btn_placeholder.button("Delete Folder", disabled=not st.session_state.delete_folder)

create_project = project_create_button_placeholder.button("Create Project", disabled=not st.session_state.create_project)
view_project = project_view_button_placeholder.button("View Project", disabled=not st.session_state.view_project)
edit_project = edit_project_btn_placeholder.button("Edit Project", disabled=not st.session_state.edit_project)
delete_project_btn = delete_project_btn_placeholder.button("Delete Project", disabled=not st.session_state.delete_project)


create_task = task_create_button_placeholder.button("Create Task", disabled=not st.session_state.create_task)
edit_task = edit_task_btn_placeholder.button("Edit Task", disabled=not st.session_state.edit_task)
delete_task_btn = delete_task_btn_placeholder.button("Delete Task", disabled=not st.session_state.delete_task)

create_milestone = milestone_create_button_placeholder.button("Create Milestone", disabled=not st.session_state.create_milestone)
edit_milestone = edit_milestone_btn_placeholder.button("Edit Milestone", disabled=not st.session_state.edit_milestone)
delete_milestone_btn = delete_milestone_btn_placeholder.button("Delete Milestone", disabled=not st.session_state.delete_milestone)


create_deliverable = deliverable_create_button_placeholder.button("Create Deliverable", disabled=not st.session_state.create_deliverable)
edit_deliverable = edit_deliverable_btn_placeholder.button("Edit Deliverable", disabled=not st.session_state.edit_deliverable)
delete_deliverable_btn = delete_deliverable_btn_placeholder.button("Delete Deliverable", disabled=not st.session_state.delete_deliverable)


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
    attachments_dict = task_inputs['attachments']
    comments_dict = task_inputs['comments']
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
        "actual_time_to_complete": None,
        "completed": False,
        "datetime_completed": None,
        "comments": comments,
        "attachments": attachments
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
            "title": [title]
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
            attachment_id = save_attachment(st.session_state.selected_folder_name, new_data['title'], new_data['id'], attachment, "project")
            attachment_ids_list.append(attachment_id)
        new_data['attachments'] = []
        for att_id in attachment_ids_list:
            new_data['attachments'].append(att_id)


    if valid_value(new_data['comments']):
        comment_id = add_comment_to_item(st.session_state.selected_folder_name, new_data['title'], new_data['id'], new_data['comments'], "project")
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
        "title": [new_data['title']]
    }

    new_project_csv = pd.DataFrame(new_project_csv_data)
    new_project_csv.to_csv(productivity_csv_path, mode="a", header=False, index=False)

    # add project to relationships.csv
    new_relationships_csv_data = {
        "parent_id": [st.session_state.selected_folder],
        "parent_type": ["folder"],
        "child_id": [new_data['id']],
        "child_type": ["project"]
    }
    new_relationships_csv = pd.DataFrame(new_relationships_csv_data)
    new_relationships_csv.to_csv(relationships_csv_path, mode="a", header=False, index=False)

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

    if new_data['attachments'] is not None:
        attachment_ids_list = []
        for attachment in new_data['attachments']:
            attachment_id = save_attachment(st.session_state.selected_folder_name, new_data['title'], new_data['id'], attachment, "task")
            attachment_ids_list.append(attachment_id)
        new_data['attachments'] = []
        for att_id in attachment_ids_list:
            new_data['attachments'].append(att_id)

    if valid_value(new_data['comments']):
        comment_id = add_comment_to_item(st.session_state.selected_folder_name, new_data['title'], new_data['id'], new_data['comments'], "task")
        new_data['comments'] = []
        new_data['comments'].append(comment_id)

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
        "title": [new_data['title']]
    }
    new_task_csv = pd.DataFrame(new_task_csv_data)
    new_task_csv.to_csv(productivity_csv_path, mode="a", header=False, index=False)

    # add task to relationships.csv
    new_relationships_csv_data = {
        "parent_id": [st.session_state.selected_project],
        "parent_type": ["project"],
        "child_id": [new_data['id']],
        "child_type": ["task"]
    }
    new_relationships_csv = pd.DataFrame(new_relationships_csv_data)
    new_relationships_csv.to_csv(relationships_csv_path, mode="a", header=False, index=False)

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
        "title": [new_data['title']]
    }
    new_milestone_csv = pd.DataFrame(new_milestone_csv_data)
    new_milestone_csv.to_csv(productivity_csv_path, mode="a", header=False, index=False)

    # add milestone to relationships.csv
    new_relationships_csv_data = {
        "parent_id": [st.session_state.selected_project],
        "parent_type": ["project"],
        "child_id": [new_data['id']],
        "child_type": ["milestone"]
    }
    new_relationships_csv = pd.DataFrame(new_relationships_csv_data)
    new_relationships_csv.to_csv(relationships_csv_path, mode="a", header=False, index=False)

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
        "title": [new_data['title']]
    }
    new_deliverable_csv = pd.DataFrame(new_deliverable_csv_data)
    new_deliverable_csv.to_csv(productivity_csv_path, mode="a", header=False, index=False)

    # add deliverable to relationships.csv
    new_relationships_csv_data = {
        "parent_id": [st.session_state.selected_project],
        "parent_type": ["project"],
        "child_id": [new_data['id']],
        "child_type": ["deliverable"]
    }
    new_relationships_csv = pd.DataFrame(new_relationships_csv_data)
    new_relationships_csv.to_csv(relationships_csv_path, mode="a", header=False, index=False)

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

    # load the csv files
    productivity_csv = pd.read_csv(productivity_csv_path)
    relationships_csv = pd.read_csv(relationships_csv_path)

    # initialize a list with ids to delete
    ids_to_delete = [folder_id]

    # find all the child_ids
    children = relationships_csv[relationships_csv["parent_id"] == folder_id]
    child_ids = children['child_id'].tolist()
    
    for child_id in child_ids:
        child_type = children[children['child_id'] == child_id]['child_type'].values[0]
        if child_type == 'project':
            # If the child is a project, find all tasks, milestones or deliverables under this project
            project_children = relationships_csv[relationships_csv["parent_id"] == child_id]
            project_child_ids = project_children['child_id'].tolist()
            ids_to_delete.extend(project_child_ids)

    # extend ids_to_delete with the child_ids
    ids_to_delete.extend(child_ids)

    # delete all the rows where id is in ids_to_delete
    productivity_csv = productivity_csv[~productivity_csv['id'].isin(ids_to_delete)]
    productivity_csv.to_csv(productivity_csv_path, index=False)

    # delete all the rows where parent_id or child_id is in ids_to_delete
    relationships_csv = relationships_csv[~relationships_csv['parent_id'].isin(ids_to_delete) & ~relationships_csv['child_id'].isin(ids_to_delete)]
    relationships_csv.to_csv(relationships_csv_path, index=False)

def remove_project(project_id):
    # load the csv files
    productivity_csv = pd.read_csv(productivity_csv_path)
    relationships_csv = pd.read_csv(relationships_csv_path)

    # initialize a list with ids to delete
    ids_to_delete = [project_id]

    # find all the child_ids
    children = relationships_csv[relationships_csv["parent_id"] == project_id]
    child_ids = children['child_id'].tolist()

    # extend ids_to_delete with the child_ids
    ids_to_delete.extend(child_ids)

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

    # delete all the rows where parent_id or child_id is in ids_to_delete
    relationships_csv = relationships_csv[~relationships_csv['parent_id'].isin(ids_to_delete) & ~relationships_csv['child_id'].isin(ids_to_delete)]
    relationships_csv.to_csv(relationships_csv_path, index=False)

def remove_task(task_id):
    # load the csv files
    productivity_csv = pd.read_csv(productivity_csv_path)
    relationships_csv = pd.read_csv(relationships_csv_path)

    # get the task info and delete the json file
    task_info = productivity_csv[productivity_csv['id'] == task_id]
    if not task_info.empty:
        folder_dir = task_info['folder_dir'].values[0]
        file_name = task_info['file_name'].values[0]
        file_path = os.path.join(folder_dir, "json_data", file_name)

        if os.path.exists(file_path):
            os.remove(file_path)

    # delete the task row in the csv files
    productivity_csv = productivity_csv[productivity_csv['id'] != task_id]
    productivity_csv.to_csv(productivity_csv_path, index=False)

    relationships_csv = relationships_csv[(relationships_csv['parent_id'] != task_id) & (relationships_csv['child_id'] != task_id)]
    relationships_csv.to_csv(relationships_csv_path, index=False)

def remove_milestone(milestone_id):
    # load the csv files
    productivity_csv = pd.read_csv(productivity_csv_path)
    relationships_csv = pd.read_csv(relationships_csv_path)

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

    relationships_csv = relationships_csv[(relationships_csv['parent_id'] != milestone_id) & (relationships_csv['child_id'] != milestone_id)]
    relationships_csv.to_csv(relationships_csv_path, index=False)

def remove_deliverable(deliverable_id):
    # load the csv files
    productivity_csv = pd.read_csv(productivity_csv_path)
    relationships_csv = pd.read_csv(relationships_csv_path)

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

    relationships_csv = relationships_csv[(relationships_csv['parent_id'] != deliverable_id) & (relationships_csv['child_id'] != deliverable_id)]
    relationships_csv.to_csv(relationships_csv_path, index=False)

def edit_folder_func(folder_id):
    if folder_id != st.session_state.selected_folder:
        st.experimental_rerun()
        return

    # load the csv files
    productivity_csv = pd.read_csv(productivity_csv_path)
    relationships_csv = pd.read_csv(relationships_csv_path)

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
                    # update the folder title
                    productivity_csv.loc[productivity_csv['id'] == folder_id, 'title'] = folder_title
                    productivity_csv.loc[productivity_csv['id'] == folder_id, 'file_name'] = folder_title
                    productivity_csv.loc[productivity_csv['id'] == folder_id, 'date_updated'] = datetime.datetime.now()
                    productivity_csv.loc[productivity_csv['id'] == folder_id, 'folder_dir'] = folder_title  # Update the folder_dir of the folder

                    # Recursive function to update the children
                    def update_children(parent_id, parent_dir):
                        child_elements = relationships_csv[relationships_csv['parent_id'] == parent_id]['child_id'].values

                        for child_id in child_elements:
                            child_type = productivity_csv.loc[productivity_csv['id'] == child_id, 'identifying_type'].values[0]
                            if child_type == 'project':
                                new_dir = f"{parent_dir}/{productivity_csv.loc[productivity_csv['id'] == child_id, 'file_name'].values[0]}"
                            else:  # For tasks, milestones, and deliverables
                                new_dir = parent_dir

                            productivity_csv.loc[productivity_csv['id'] == child_id, 'folder_dir'] = new_dir
                            update_children(child_id, new_dir)  # Call the function recursively for each child

                    # Update the folder_dir of child elements
                    update_children(folder_id, folder_title)

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
                        if add_attachments is not None:
                            for attachment in add_attachments:
                                attachment_id = save_attachment(st.session_state.selected_folder_name, project['title'], project['id'], attachment, "project")
                                project['attachments'].append(attachment_id)
                        if valid_value(add_comments):
                            comment_id = add_comment_to_item(st.session_state.selected_folder_name, project['title'], project['id'], add_comments, "project")
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
        attachments_dict = task_inputs['attachments']
        comments_dict = task_inputs['comments']

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

                if saveeditbtn:
                    try:


                        productivity_csv.loc[productivity_csv['id'] == task_id, 'title'] = task['title']
                        productivity_csv.loc[productivity_csv['id'] == task_id, 'date_updated'] = datetime.datetime.now()
                        productivity_csv.to_csv(productivity_csv_path, index=False)

                        if add_attachments is not None:
                            for attachment in add_attachments:
                                attachment_id = save_attachment(st.session_state.selected_folder_name, task['title'], task['id'], attachment, "task")
                                task['attachments'].append(attachment_id)
                        if valid_value(add_comments):
                            comment_id = add_comment_to_item(st.session_state.selected_folder_name, task['title'], task['id'], add_comments, "task")
                            task['comments'].append(comment_id)

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
                success_func("Deliverable edited successfully.")

            except Exception as e:
                st.write(f'An error occurred: {e}')




if view_project:
    st.session_state.view_mode = True
    st.session_state.view_project = True
    st.session_state.view_selected_project = True


view_project_area = st.empty()

with view_project_area.container():
    project_view_back_btn = st.empty
    project_title_placeholder = st.empty()



view_mode_off = None
if st.session_state.view_mode == True:
    if st.session_state.view_project == True and st.session_state.view_selected_project == True:
        view_mode_off = project_view_back_btn.button("< Back", key=f"back_btn_{st.session_state.selected_project}")
        project_title_placeholder.title(st.session_state.selected_project_name)
        st.write("---")
        st.header("Milestones")
        st.write("---")
        st.header("Tasks")
        st.write("---")
        st.header("Deliverables")
        st.write("---")

if view_mode_off:
    st.session_state.view_mode = False
    st.session_state.view_project = False
    st.session_state.view_selected_project = False








if create_folder:
    st.session_state.save_mode = True
    st.session_state.save_folder = True
elif create_project:
    st.session_state.save_mode = True
    st.session_state.save_project = True
elif create_task:
    st.session_state.save_mode = True
    st.session_state.save_task = True
elif create_milestone:
    st.session_state.save_mode = True
    st.session_state.save_milestone = True
elif create_deliverable:
    st.session_state.save_mode = True
    st.session_state.save_deliverable = True





save_col, cancel_col = st.columns(2)

button_placeholder = save_col.empty()

if st.session_state.delete_mode == True or st.session_state.save_mode == True or st.session_state.edit_mode == True:
    cancel_btn = cancel_col.button("Cancel", key="cancel_btn_clicked")

    if cancel_btn:
        for session_state in session_states:
            st.session_state[session_state] = False
        st.experimental_rerun()

if st.session_state.delete_mode == True:
    deletebtn = button_placeholder.button("Delete", disabled=not st.session_state.delete_mode)
else:
    deletebtn = None

if st.session_state.save_mode == True:
    savebtn = button_placeholder.button("Save", disabled=not st.session_state.save_mode)
else:
    savebtn = None

if st.session_state.edit_mode == True:

    saveeditbtn = button_placeholder.button("Save", disabled=not st.session_state.edit_mode)
else:
    saveeditbtn = None


if st.session_state.save_mode == True:
    if st.session_state.save_folder == True:
        add_new_folder_data()
    elif st.session_state.save_project == True:
        add_new_project_data()
    elif st.session_state.save_task == True:
        add_new_task_data()
    elif st.session_state.save_milestone == True:
        add_new_milestone_data()
    elif st.session_state.save_deliverable == True:
        add_new_deliverable_data()










if delete_folder_btn:
    selected_folder = st.session_state.selected_folder
    selected_folder_name = st.session_state.selected_folder_name
    delete_selected_folder = st.session_state.delete_selected_folder
    st.session_state.clear()
    st.session_state.selected_folder = selected_folder
    st.session_state.selected_folder_name = selected_folder_name
    st.session_state.delete_selected_folder = delete_selected_folder
    st.session_state.delete_mode = True
    st.session_state.delete_folder = True
    st.session_state.delete_selected_folder = True
    st.experimental_rerun()

if delete_project_btn:
    selected_folder = st.session_state.selected_folder
    selected_folder_name = st.session_state.selected_folder_name
    selected_project = st.session_state.selected_project
    selected_project_name = st.session_state.selected_project_name
    delete_selected_project = st.session_state.delete_selected_project
    st.session_state.clear()
    st.session_state.selected_folder = selected_folder
    st.session_state.selected_folder_name = selected_folder_name
    st.session_state.selected_project = selected_project
    st.session_state.selected_project_name = selected_project_name
    st.session_state.delete_mode = True
    st.session_state.delete_project = True
    st.session_state.delete_selected_project = True
    st.experimental_rerun()

if delete_task_btn:
    selected_folder = st.session_state.selected_folder
    selected_folder_name = st.session_state.selected_folder_name
    selected_project = st.session_state.selected_project
    selected_project_name = st.session_state.selected_project_name
    selected_task = st.session_state.selected_task
    selected_task_name = st.session_state.selected_task_name
    delete_selected_task = st.session_state.delete_selected_task
    st.session_state.clear()
    st.session_state.selected_folder = selected_folder
    st.session_state.selected_folder_name = selected_folder_name
    st.session_state.selected_project = selected_project
    st.session_state.selected_project_name = selected_project_name
    st.session_state.selected_task = selected_task
    st.session_state.selected_task_name = selected_task_name
    st.session_state.delete_selected_task = delete_selected_task
    st.session_state.delete_mode = True
    st.session_state.delete_task = True
    st.session_state.delete_selected_task = True
    st.experimental_rerun()

if delete_milestone_btn:
    selected_folder = st.session_state.selected_folder
    selected_folder_name = st.session_state.selected_folder_name
    selected_project = st.session_state.selected_project
    selected_project_name = st.session_state.selected_project_name
    selected_milestone = st.session_state.selected_milestone
    selected_milestone_name = st.session_state.selected_milestone_name
    delete_selected_milestone = st.session_state.delete_selected_milestone
    st.session_state.clear()
    st.session_state.selected_folder = selected_folder
    st.session_state.selected_folder_name = selected_folder_name
    st.session_state.selected_project = selected_project
    st.session_state.selected_project_name = selected_project_name
    st.session_state.selected_milestone = selected_milestone
    st.session_state.selected_milestone_name = selected_milestone_name
    st.session_state.delete_selected_milestone = delete_selected_milestone
    st.session_state.delete_mode = True
    st.session_state.delete_milestone = True
    st.session_state.delete_selected_milestone = True
    st.experimental_rerun()

if delete_deliverable_btn:
    selected_folder = st.session_state.selected_folder
    selected_folder_name = st.session_state.selected_folder_name
    selected_project = st.session_state.selected_project
    selected_project_name = st.session_state.selected_project_name
    selected_deliverable = st.session_state.selected_deliverable
    selected_deliverable_name = st.session_state.selected_deliverable_name
    delete_selected_deliverable = st.session_state.delete_selected_deliverable
    st.session_state.clear()
    st.session_state.selected_folder = selected_folder
    st.session_state.selected_folder_name = selected_folder_name
    st.session_state.selected_project = selected_project
    st.session_state.selected_project_name = selected_project_name
    st.session_state.selected_deliverable = selected_deliverable
    st.session_state.selected_deliverable_name = selected_deliverable_name
    st.session_state.delete_selected_deliverable = delete_selected_deliverable
    st.session_state.delete_mode = True
    st.session_state.delete_deliverable = True
    st.session_state.delete_selected_deliverable = True
    st.experimental_rerun()



if st.session_state.delete_mode == True:
    if st.session_state.delete_folder == True and st.session_state.delete_selected_folder == True:
        # find all rows in relationships.csv where the selected_folder = parent_id
        is_parent_of = relationships_csv[relationships_csv['parent_id'] == st.session_state.selected_folder]
        # using the is_parent_of df, find all the rows in productivity_csv where the child_id matches id
        if is_parent_of.empty:
            pass
        else:
            # turn all child_id values into a list
            child_id_list = is_parent_of['child_id'].tolist()

            # using child_id_list, find all rows in productivity_csv where the child_id matches id
            is_child_of = productivity_csv[productivity_csv['id'].isin(child_id_list)]
            st.write(is_child_of)

            # give a warning saying which identifying_type and title will be deleted from is_child_of
            st.warning(f"Are you sure you want to delete folder {st.session_state.selected_folder_name}? This will also delete the following:")
            for index, row in is_child_of.iterrows():
                st.warning(f"- {(row['identifying_type']).capitalize()} : {row['title']}")
        st.warning(f"Are you sure you want to delete folder {st.session_state.selected_folder_name}?")

        if deletebtn:
            try:
                remove_folder(st.session_state.selected_folder)
                success_func("Folder deleted successfully.")
            except Exception as e:
                st.write(f"An error occurred: {e}")
    elif st.session_state.delete_project == True and st.session_state.delete_selected_project == True:
        st.warning(f"Are you sure you want to delete {st.session_state.selected_project_name}?")
        if deletebtn:
            try:
                remove_project(st.session_state.selected_project)
                success_func("Project deleted successfully.")
            except Exception as e:
                st.write(f"An error occurred: {e}")
    elif st.session_state.delete_task ==True and st.session_state.delete_selected_task == True:
        st.warning(f"Are you sure you want to delete {st.session_state.selected_task_name}?")
        if deletebtn:
            try:
                remove_task(st.session_state.selected_task)
                success_func("Task deleted successfully.")
            except Exception as e:
                st.write(f"An error occurred: {e}")
    elif st.session_state.delete_milestone ==True and st.session_state.delete_selected_milestone == True:
        st.warning(f"Are you sure you want to delete {st.session_state.selected_milestone_name}?")
        if deletebtn:
            try:
                remove_milestone(st.session_state.selected_milestone)
                success_func("Milestone deleted successfully.")
            except Exception as e:
                st.write(f"An error occurred: {e}")
    elif st.session_state.delete_deliverable ==True and st.session_state.delete_selected_deliverable == True:
        st.warning(f"Are you sure you want to delete {st.session_state.selected_deliverable_name}?")
        if deletebtn:
            try:
                remove_deliverable(st.session_state.selected_deliverable)
                success_func("Deliverable deleted successfully.")
            except Exception as e:
                st.write(f"An error occurred: {e}")




if edit_folder:
    selected_folder = st.session_state.selected_folder
    selected_folder_name = st.session_state.selected_folder_name
    edit_selected_folder = st.session_state.edit_selected_folder
    st.session_state.clear()
    st.session_state.selected_folder = selected_folder
    st.session_state.selected_folder_name = selected_folder_name
    st.session_state.edit_selected_folder = edit_selected_folder
    st.session_state.edit_mode = True
    st.session_state.edit_folder = True
    st.session_state.edit_selected_folder = True
    st.experimental_rerun()

if edit_project:
    selected_folder = st.session_state.selected_folder
    selected_folder_name = st.session_state.selected_folder_name
    selected_project = st.session_state.selected_project
    selected_project_name = st.session_state.selected_project_name
    edit_selected_project = st.session_state.edit_selected_project
    st.session_state.clear()
    st.session_state.selected_folder = selected_folder
    st.session_state.selected_folder_name = selected_folder_name
    st.session_state.selected_project = selected_project
    st.session_state.selected_project_name = selected_project_name
    st.session_state.edit_selected_project = edit_selected_project
    st.session_state.edit_mode = True
    st.session_state.edit_project = True
    st.session_state.edit_selected_project = True
    st.experimental_rerun()

if edit_task:
    selected_folder = st.session_state.selected_folder
    selected_folder_name = st.session_state.selected_folder_name
    selected_project = st.session_state.selected_project
    selected_project_name = st.session_state.selected_project_name
    selected_task = st.session_state.selected_task
    selected_task_name = st.session_state.selected_task_name
    edit_selected_task = st.session_state.edit_selected_task
    st.session_state.clear()
    st.session_state.selected_folder = selected_folder
    st.session_state.selected_folder_name = selected_folder_name
    st.session_state.selected_project = selected_project
    st.session_state.selected_project_name = selected_project_name
    st.session_state.selected_task = selected_task
    st.session_state.selected_task_name = selected_task_name
    st.session_state.edit_selected_task = edit_selected_task
    st.session_state.edit_mode = True
    st.session_state.edit_task = True
    st.session_state.edit_selected_task = True
    st.experimental_rerun()

if edit_milestone:
    selected_folder = st.session_state.selected_folder
    selected_folder_name = st.session_state.selected_folder_name
    selected_project = st.session_state.selected_project
    selected_project_name = st.session_state.selected_project_name
    selected_milestone = st.session_state.selected_milestone
    selected_milestone_name = st.session_state.selected_milestone_name
    edit_selected_milestone = st.session_state.edit_selected_milestone
    st.session_state.clear()
    st.session_state.selected_folder = selected_folder
    st.session_state.selected_folder_name = selected_folder_name
    st.session_state.selected_project = selected_project
    st.session_state.selected_project_name = selected_project_name
    st.session_state.selected_milestone = selected_milestone
    st.session_state.selected_milestone_name = selected_milestone_name
    st.session_state.edit_selected_milestone = edit_selected_milestone
    st.session_state.edit_mode = True
    st.session_state.edit_milestone = True
    st.session_state.edit_selected_milestone = True
    st.experimental_rerun()

if edit_deliverable:
    selected_folder = st.session_state.selected_folder
    selected_folder_name = st.session_state.selected_folder_name
    selected_project = st.session_state.selected_project
    selected_project_name = st.session_state.selected_project_name
    selected_deliverable = st.session_state.selected_deliverable
    selected_deliverable_name = st.session_state.selected_deliverable_name
    edit_selected_deliverable = st.session_state.edit_selected_deliverable
    st.session_state.clear()
    st.session_state.selected_folder = selected_folder
    st.session_state.selected_folder_name = selected_folder_name
    st.session_state.selected_project = selected_project
    st.session_state.selected_project_name = selected_project_name
    st.session_state.selected_deliverable = selected_deliverable
    st.session_state.selected_deliverable_name = selected_deliverable_name
    st.session_state.edit_selected_deliverable = edit_selected_deliverable
    st.session_state.edit_mode = True
    st.session_state.edit_deliverable = True
    st.session_state.edit_selected_deliverable = True
    st.experimental_rerun()


if st.session_state.edit_mode == True:
    if st.session_state.edit_folder == True and st.session_state.edit_selected_folder == True:
        st.session_state.save_folder = True
        edit_folder_func(st.session_state.selected_folder)
    elif st.session_state.edit_project == True and st.session_state.edit_selected_project == True:
        st.session_state.save_project = True
        edit_project_func(st.session_state.selected_project)
    elif st.session_state.edit_task == True and st.session_state.edit_selected_task == True:
        st.session_state.save_task = True
        edit_task_func(st.session_state.selected_task)
    elif st.session_state.edit_milestone == True and st.session_state.edit_selected_milestone == True:
        st.session_state.save_milestone = True
        edit_milestone_func(st.session_state.selected_milestone)
    elif st.session_state.edit_deliverable == True and st.session_state.edit_selected_deliverable == True:
        st.session_state.save_deliverable = True
        edit_deliverable_func(st.session_state.selected_deliverable)




