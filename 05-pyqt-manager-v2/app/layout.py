## layout.py

import streamlit as st
from app.buttons import Buttons
from app.item_manager import Folder

class Layout:
    def __init__(self, session_manager):
        self.session_manager = session_manager
        self.buttons = Buttons()

    def show(self, action, item):
        if action is None:
            self.default_layout()
        elif action == "create" and item == "folder":
            self.create_folder()

    def default_layout(self):
        st.write("Default Layout, No Items Yet")
        create_button = self.buttons.create_button('folder')
        if create_button:
            st.session_state.create_folder = True
            self.session_manager.showLayout()

    def create_folder(self):
        st.title("Create Folder")
        folder = Folder()
        data = folder.create()
        print(data)


