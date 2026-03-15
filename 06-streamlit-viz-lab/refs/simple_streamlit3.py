import streamlit as st

# create a function that takes in one var, removes it from a list, and returns the list
def return_other_items_from_list(item, list):
    if type(item) == list:
        for i in item:
            if i in list:
                list.remove(i)
    elif item in list:
        list.remove(item)
    return list

abilities = ["enabled", "disabled", "active"] 
modes = ["save", "create", "select", "cancel", "edit", "delete"]
items = ["folders","folder", "project", "task", "milestone", "deliverable"]

# Initializing session states
for mode in modes:
    if mode not in st.session_state:
        st.session_state[mode] = 'disabled'

for item in items:
    if item not in st.session_state:
        st.session_state[item] = 'disabled'





folders = []
projects = []
tasks = []
milestones = []
deliverables = []

create_folder = st.empty()
create_project = st.empty()
create_task = st.empty()
create_milestone = st.empty()
create_deliverable = st.empty()

save = st.empty()
cancel = st.empty()
edit = st.empty()
delete = st.empty()

save_btn = None
cancel_btn = None


if len(folders) == 0:
    disabled_modes = return_other_items_from_list("create", modes)
    disabled_items = return_other_items_from_list("folder", items)
    for item in disabled_modes:
        st.session_state[item] = 'disabled'
    for item in disabled_items:
        st.session_state[item] = 'disabled'
    st.session_state['create'] = 'enabled'
    st.session_state['folder'] = 'enabled'
elif len(projects) == 0:
    disabled_modes = return_other_items_from_list(["create", "edit"], modes)
    disabled_items = return_other_items_from_list(["folder", "project"], items)


create_folder_btn = create_folder.button('Create Folder', key='create_folder_btn')

# Handle Create action
if create_folder_btn:
    st.session_state['create'] = 'active'
    st.session_state['folder'] = 'active'

    # Enable Save and Cancel actions

if st.session_state['create'] == 'active':
    st.session_state['save'] = 'enabled'
    st.session_state['cancel'] = 'enabled'
    st.session_state['select'] = 'disabled'
    st.session_state['edit'] = 'disabled'
    st.session_state['delete'] = 'disabled'

if st.session_state['save'] == 'enabled':
    save_btn = save.button('Save', key='new_folder_save_btn')
    cancel_btn = cancel.button('Cancel', key='cancel_btn')

if save_btn:
    st.session_state['save'] = 'active'
    st.session_state['cancel'] = 'disabled'
    st.session_state['select'] = 'disabled'
    st.session_state['edit'] = 'disabled'
    st.session_state['delete'] = 'disabled'

if cancel_btn:
    st.experimental_rerun()




st.session_state





