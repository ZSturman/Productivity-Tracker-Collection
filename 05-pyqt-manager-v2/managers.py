import os
import streamlit as st
import pandas as pd

class Folder:
    def __init__(self, name, color=None, size=None, created_at=None):
        self.name = name
        self.color = color
        self.size = size
        self.created_at = created_at
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def edit_item(self, item_index, new_item):
        if 0 <= item_index < len(self.items):
            self.items[item_index] = new_item

    def delete_item(self, item_index):
        if 0 <= item_index < len(self.items):
            self.items.pop(item_index)


class FolderManager:
    def __init__(self):
        self.folders = {}

    def create_folder(self, data):
        st.write(data)
        folder_title = data['title']
        folder_color = data['color']
        folder_size = data['size']
        folder_created_at = data['created_at']
        folder = Folder(folder_title, folder_color, folder_size, folder_created_at)
        self.folders[folder_title] = folder
        os.makedirs(folder_title, exist_ok=True)
        st.success(f"Successfully created folder {folder_title}")

    def delete_folder(self, name):
        if name in self.folders:
            del self.folders[name]
            os.rmdir(name)

    def save_to_csv(self, filename):
        data = {'FolderName': [], 'Items': [], 'Color': [], 'Size': [], 'CreatedAt': []}
        for folder_name, folder in self.folders.items():
            data['FolderName'].append(folder_name)
            data['Items'].append(','.join(folder.items))
            data['Color'].append(folder.color)
            data['Size'].append(folder.size)
            data['CreatedAt'].append(folder.created_at)

        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)

    def get_folder_inputs(self):
        input_fields = {
            'title': st.text_input('Folder Title'),
            'color': st.color_picker('Folder Color'),
            'size': st.number_input('Folder Size', min_value=0, max_value=1000),
            'created_at': st.date_input('Folder Created At')
        }
        return input_fields
