#### ss2.py

import streamlit as st
from app.item_manager import Folder
from app.layout import Layout
from app.buttons import Buttons

class SessionManager:
    def __init__(self):
        self.actions = ['create', 'edit', 'delete', 'view']
        self.items = ['folder', 'project', 'task', 'milestone', 'deliverable']
        self.extra_states = ['selected_id', 'selected_name']
        self.layout = Layout(self)
        self.initialize_states()

    def initialize_states(self):
        for action in self.actions:
            for item in self.items:
                st.session_state[f"{action}_{item}"] = False
        for extra in self.extra_states:
            for item in self.items:
                st.session_state[f"{extra}_{item}"] = None

    def checkSession(self):
        for action in self.actions:
            if any([st.session_state[f"{action}_{item}"] for item in self.items]):
                for other_action in [a for a in self.actions if a != action]:
                    for item in self.items:
                        st.session_state[f"{other_action}_{item}"] = False
        ss_action = None
        ss_item = None
        for action in self.actions:
            for item in self.items:
                if st.session_state[f"{action}_{item}"]:
                    ss_action =  action
                    ss_item = item
        return ss_action, ss_item

    def showLayout(self):
        action, item = self.checkSession()
        st.write("action: ", action, "item: ", item)
        self.layout.show(action, item)


app = SessionManager()

if __name__ == "__main__":
    app.showLayout()
