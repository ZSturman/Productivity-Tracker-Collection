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

                        #if value is not None and input_type not in ["self_made_list", "text_markdown", "self_made_list_file"]:
                            #data["editable_data"][section][field] = value


    else:
        if old_value == "" or old_value == "None" or old_value == None or old_value == "null" or old_value == "Null" or old_value == "NULL" or old_value == "none" or old_value == "NoneType" or old_value == "NoneType" or old_value == False:
            pass








def edit_tab(tab, project_id, path, project_data):
    st.session_state.edit_mode = tab
    st.write(f"Editing {tab} tab")



def selected_folder_tabs(path, project_data):



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





