import streamlit as st
import pandas as pd
import numpy as np
import os
import json
import datetime
import shutil



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
                comments_col, attachments_col = st.columns([1, 2])
                with comments_col:
                    st.write("### Show comments here")
                    st.write("---")
                    st.write("#### Have ability to add, edit or remove comments")
                with attachments_col:
                    st.write("### Show attachments here")
                    st.write("---")
                    st.write("#### Have ability to add or remove attachments")
                
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
                        #update the json file
                        with open(path_to_json, "w") as file:
                            json.dump(data, file, indent=4, cls=CustomJSONEncoder)

                        # update the csv file
                        productivity_csv.loc[productivity_csv['id'] == project_id, 'title'] = project['title']
                        productivity_csv.loc[productivity_csv['id'] == project_id, 'date_updated'] = datetime.datetime.now()
                        productivity_csv.to_csv(productivity_csv_path, index=False)
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
                st.write("### Show attachments here")
                st.write("#### Have ability to add or remove attachments")
                st.write("### Show comments here")
                st.write("#### Have ability to add, edit or remove comments")

                if saveeditbtn:
                    try:
                        with open(path_to_json, 'w') as outfile:
                            json.dump(task, outfile, cls=CustomJSONEncoder)

                        productivity_csv.loc[productivity_csv['id'] == task_id, 'title'] = task['title']
                        productivity_csv.loc[productivity_csv['id'] == task_id, 'date_updated'] = datetime.datetime.now()
                        productivity_csv.to_csv(productivity_csv_path, index=False)
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



