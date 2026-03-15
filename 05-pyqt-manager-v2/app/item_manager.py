### item_manager.py

import streamlit as st
import json
from app.buttons import Buttons

class ItemManager:
    def load_json(self):
        pass

    def save_json(self, data):
        print(data)
        with open('data.json', 'w') as f:
            json.dump(data, f)

    def load_csv(self):
        pass

    def save_csv(self):
        pass

    def load_data(self, id):
        data = {
            'type': 'folder',
            'id': '111',
            'title': 'Folder 1'
        }

        if data['id'] == id:
            item = data
        return item


class Item:
    def __init__(self):
        self.buttons = Buttons()

    def create(self, item_type):
        save_btn = self.buttons.save_button(item_type)
        if save_btn:
            st.success(f"Successfully created {item_type}")
        cancel_btn = self.buttons.cancel_button(item_type)

    def edit(self, id):
        self.buttons.save_button(id)
        self.buttons.cancel_button(id)

    def view(self, id):
        self.buttons.edit_button(id)
        self.buttons.delete_button(id)

    def delete(self, id):
        self.buttons.save_button(id)
        self.buttons.cancel_button(id)



class Folder(Item):
    @classmethod
    def set_folder_inputs(cls):
        folder_input_fields = {
            'title': st.text_input('Folder Title')
        }
        return folder_input_fields

    def create(self):
        folder_inputs = self.set_folder_inputs()
        data = {input_field: input_value for input_field, input_value in folder_inputs.items()}
        return data



    def view(self, id):
        data = ItemManager.load_data(self, id)
        st.write(data)
        super(Folder, self).view(id)
