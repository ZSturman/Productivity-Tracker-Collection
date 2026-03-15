import streamlit as st
import json
from datetime import datetime
from app.json_data import new_project_json_template, new_deliverable_json_template, new_milestone_json_template
from app.administrative import make_safe, valid_value, formatted_options, CustomJSONEncoder, make_sure_items_are_in_csv

# Dummy data
folders = ['Folder 1', 'Folder 2', 'Folder 3']
categories = ['Category 1', 'Category 2', 'Category 3']
goal_verbs = ['Verb 1', 'Verb 2', 'Verb 3']
genres = ['Genre 1', 'Genre 2', 'Genre 3']
use_cases = ['Use Case 1', 'Use Case 2', 'Use Case 3']

def generate_id():
    # Implement your own id generation logic here
    return 1

def save_to_json(data, filename):
    # Implement your own saving logic here
    pass

def read_from_json(filename):
    # Implement your own reading logic here
    pass

# Sidebar
st.sidebar.header('Folders')
selected_folder = st.sidebar.selectbox('Select folder', folders)

if selected_folder:
    st.sidebar.header('Projects')
    selected_project = st.sidebar.selectbox('Select project', [])

    if st.sidebar.button('Create new project'):
        with st.form("new_project_form"):
            st.write('Add New Project')

            new_project_json_template["id"] = generate_id()
            new_project_json_template["date_created"] = datetime.now().isoformat()
            new_project_json_template["date_modified"] = datetime.now().isoformat()
            new_project_json_template["title"] = st.text_input('Title')
            new_project_json_template["folder_dir"] = selected_folder
            new_project_json_template["description"] = st.text_area('Description')
            new_project_json_template["priority"] = st.selectbox('Priority', ['High', 'Medium', 'Low'])
            new_project_json_template["status"] = st.selectbox('Status', ['Active', 'Inactive', 'Completed'])
            new_project_json_template["no_due_date"] = st.checkbox('No Due Date')
            new_project_json_template["datetime_due"] = None if new_project_json_template["no_due_date"] else st.date_input('Due Date')
            new_project_json_template["start_date"] = st.date_input('Goal Start Date')
            st.write("---")
            with st.expander("Add Descriptors"):
                new_project_json_template["category"] = st.selectbox('Category', categories)
                new_project_json_template["goal_verb"] = st.selectbox('Goal Verb', goal_verbs)
                new_project_json_template["genre"] = st.selectbox('Genre', genres)
                new_project_json_template["use_case"] = st.selectbox('Use Case', use_cases)
            with st.expander("Add Comments"):
                new_project_json_template["comments"] = st.text_area('Comments')
            with st.expander("Add Attachments"):
                new_project_json_template["attachments"] = st.text_area('Attachments')
            st.write("Add Tasks, Milestones, and Deliverables after project is created")


            if st.form_submit_button('Submit'):
                save_to_json(new_project_json_template, f'{new_project_json_template["title"]}.json')
                st.success('New project created!')
