
st.session_state.prev_selected_folder = st.session_state.selected_folder


# using productivity csv create a df of all folders organized by date_updated
folders_df = productivity_csv[productivity_csv["identifying_type"] == "folder"].sort_values(by=["date_updated"], ascending=False)

if folders_df.empty:
    st.session_state.selected_folder = None
else:
    if st.session_state.selected_folder == False:
        st.session_state.selected_folder = folders_df["id"].values[0]
        st.session_state.selected_folder_name = folders_df["title"].values[0]

    find_folder = folder_select_selector_placeholder.selectbox("Find Folder", list(folders_df["title"]))

    if find_folder != st.session_state.prev_selected_folder:
        st.session_state.selected_folder = folders[find_folder]
        st.session_state.selected_folder_name = find_folder

        

st.session_state.create_folder = True


if st.session_state.selected_folder:
    # using relationships csv create a df of all projects whose parent is the selected folder
    projects_df = relationships_csv[relationships_csv["parent_id"] == st.session_state.selected_folder]
    projects_df = projects_df[projects_df["parent_type"] == "folder"]
    projects_df = projects_df[projects_df["child_type"] == "project"]
    projects_df = projects_df.merge(productivity_csv, left_on="child_id", right_on="id")

    if projects_df.empty:
        st.session_state.selected_project = None
    else:
        find_project = project_select_selector_placeholder.selectbox("Find Project", list(projects_df["title"]))
        st.session_state.selected_project = projects_df[projects_df["title"] == find_project]["id"].values[0]
        st.session_state.selected_project_name = find_project

        if valid_value(st.session_state.selected_project):
            selected_project = st.session_state.selected_project
            selected_project_name = st.session_state.selected_project_name
            for session_state in session_states:
                st.session_state.session_state = False
            st.session_state.selected_project = selected_project
            st.session_state.selected_project_name = selected_project_name
            st.session_state.edit_project = True
            st.session_state.delete_project = True
        else:
            st.session_state.selected_project = None
            st.session_state.selected_project_name = None
            st.session_state.edit_project = False
            st.session_state.delete_project = False
    
    st.session_state.create_project = True


if st.session_state.selected_project:
    # using relationships csv create a df of all tasks whose parent is the selected project
    tasks_df = relationships_csv[relationships_csv["parent_id"] == st.session_state.selected_project]
    tasks_df = tasks_df[tasks_df["parent_type"] == "project"]
    tasks_df = tasks_df[tasks_df["child_type"] == "task"]
    tasks_df = tasks_df.merge(productivity_csv, left_on="child_id", right_on="id")

    if tasks_df.empty:
        st.session_state.selected_task = None
    else:
        find_task = task_select_selector_placeholder.selectbox("Find Task", list(tasks_df["title"]))
        st.session_state.selected_task = tasks_df[tasks_df["title"] == find_task]["id"].values[0]
        st.session_state.selected_task_name = find_task

        if st.session_state.selected_task != st.session_state.prev_selected_task:
            selected_task = st.session_state.selected_task
            selected_task_name = st.session_state.selected_task_name
            st.session_state.selected_task = selected_task
            st.session_state.selected_task_name = selected_task_name
            st.session_state.edit_task = True
            st.session_state.delete_task = True

    st.session_state.create_task = True


if st.session_state.selected_project:
    # using relationships csv create a df of all milestones whose parent is the selected project
    milestones_df = relationships_csv[relationships_csv["parent_id"] == st.session_state.selected_project]
    milestones_df = milestones_df[milestones_df["parent_type"] == "project"]
    milestones_df = milestones_df[milestones_df["child_type"] == "milestone"]
    milestones_df = milestones_df.merge(productivity_csv, left_on="child_id", right_on="id")

    if milestones_df.empty:
        st.session_state.selected_milestone = None
    else:
        find_milestone = milestone_select_selector_placeholder.selectbox("Find Milestone", list(milestones_df["title"]))
        st.session_state.selected_milestone = milestones_df[milestones_df["title"] == find_milestone]["id"].values[0]
        st.session_state.selected_milestone_name = find_milestone

        if st.session_state.selected_milestone != st.session_state.prev_selected_milestone:
            selected_milestone = st.session_state.selected_milestone
            selected_milestone_name = st.session_state.selected_milestone_name
            st.session_state.selected_milestone = selected_milestone
            st.session_state.selected_milestone_name = selected_milestone_name
            st.session_state.edit_milestone = True
            st.session_state.delete_milestone = True

    st.session_state.create_milestone = True


if st.session_state.selected_project:
    # using relationships csv create a df of all deliverables whose parent is the selected project
    deliverables_df = relationships_csv[relationships_csv["parent_id"] == st.session_state.selected_project]
    deliverables_df = deliverables_df[deliverables_df["parent_type"] == "project"]
    deliverables_df = deliverables_df[deliverables_df["child_type"] == "deliverable"]
    deliverables_df = deliverables_df.merge(productivity_csv, left_on="child_id", right_on="id")

    if deliverables_df.empty:
        st.session_state.selected_deliverable = None
    else:
        find_deliverable = deliverable_select_selector_placeholder.selectbox("Find Deliverable", list(deliverables_df["title"]))
        st.session_state.selected_deliverable = deliverables_df[deliverables_df["title"] == find_deliverable]["id"].values[0]
        st.session_state.selected_deliverable_name = find_deliverable

        if st.session_state.selected_deliverable != st.session_state.prev_selected_deliverable:
            selected_deliverable = st.session_state.selected_deliverable
            selected_deliverable_name = st.session_state.selected_deliverable_name
            st.session_state.selected_deliverable = selected_deliverable
            st.session_state.selected_deliverable_name = selected_deliverable_name
            st.session_state.edit_deliverable = True
            st.session_state.delete_deliverable = True

    st.session_state.create_deliverable = True





    relationships_csv = pd.read_csv(relationships_csv_path)
    relationships_csv = relationships_csv[relationships_csv["parent_id"] != folder_id]


    
    relationships_csv.to_csv(relationships_csv_path, index=False)
