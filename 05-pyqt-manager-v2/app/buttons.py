## buttons.py

import streamlit as st

class Buttons:
    def create_button(self, item_type):
        return st.button(f'Create {item_type}', key=f'{item_type}-create-button')

    def save_button(self, id):
        return st.button('Save', key=f'{id}-save-button')
    
    def cancel_button(self, id):
        return st.button('Cancel', key=f'{id}-cancel-button')
    
    def edit_button(self, id):
        return st.button('Edit', key=f'{id}-edit-button')
    
    def delete_button(self, id):
        return st.button('Delete', key=f'{id}-delete-button')
