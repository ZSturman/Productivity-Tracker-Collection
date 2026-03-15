import os
import pandas as pd
import streamlit as st
from managers import FolderManager


class Navigation:
    def __init__(self, folder_manager):
        self.folder_manager = folder_manager

    def home_screen(self):
        st.subheader('Home')
        if not self.folder_manager.folders:  # If no folders exist
            st.write('Welcome to Folder Manager. No folders exist yet. Please select an action from the sidebar.')
        else:
            st.write('Welcome to Folder Manager. There are some folders already created. Please select an action from the sidebar.')

    def create_screen(self):
        st.subheader('Create a new folder')
        data = self.folder_manager.get_folder_inputs()
        if st.button('Create Folder'):
            self.folder_manager.create_folder(data)
        if st.button('Cancel'):
            st.session_state.home = True
            # make then sidebar choice 'Home' active
            st.experimental_rerun()


    def view_screen(self):
        st.subheader('View existing folders')
        if not self.folder_manager.folders:  # If no folders exist
            st.write('No folders exist yet.')
        else:
            for name, folder in self.folder_manager.folders.items():
                st.write(f'Folder Name: {name}, Items: {folder.items}')


menu = ['Home', 'Create', 'View']

# if the items in the menu list are  not in the session state, add them to the session state
if not hasattr(st.session_state, 'home'):
    st.session_state.home = False
if not hasattr(st.session_state, 'create'):
    st.session_state.create = False
if not hasattr(st.session_state, 'view'):
    st.session_state.view = False


# Initialize a FolderManager object
folder_manager = FolderManager()

# Initialize a Navigation object
nav = Navigation(folder_manager)

# Create a sidebar for navigation

choice = st.sidebar.selectbox('Menu', menu)

# Call the appropriate method of the Navigation object based on the user's choice
if choice == 'Home' or st.session_state.home == True:
    st.session_state.create = False
    st.session_state.view = False
    nav.home_screen()
if choice == 'Create' or st.session_state.create == True:
    st.session_state.home = False
    st.session_state.view = False
    nav.create_screen()
if choice == 'View' or st.session_state.view == True:
    st.session_state.create = False
    st.session_state.home = False
    nav.view_screen()



