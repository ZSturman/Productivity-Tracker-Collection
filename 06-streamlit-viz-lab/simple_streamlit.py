import os
import streamlit as st

def create_folder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        st.success(f"Folder '{folder_name}' created successfully.")
        return True
    else:
        st.warning(f"Folder '{folder_name}' already exists.")
        return False

def show_folder_details(folder_name):
    folder_path = os.path.abspath(folder_name)
    st.write(f"Folder name: {folder_name}")
    st.write(f"Folder path: {folder_path}")
    st.write("Contents:")
    for item in os.listdir(folder_name):
        st.write(f" - {item}")

st.set_page_config(page_title="Folder App")
st.title("Folder App")

st.sidebar.title("Create Folder")

folder_name = st.sidebar.text_input("Folder Name")
create_button = st.sidebar.button("Create Folder")

folder_list = [folder for folder in os.listdir() if os.path.isdir(folder)]

selected_folder = None

if create_button:
    if folder_name:
        folder_created = create_folder(folder_name)
        if folder_created:
            folder_list.append(folder_name)
            selected_folder = folder_name
    else:
        st.sidebar.warning("Please enter a folder name.")

if folder_list:
    st.sidebar.title("Select Folder")
    selected_folder = st.sidebar.selectbox("Choose a folder", folder_list, index=folder_list.index(selected_folder) if selected_folder else 0)

    if selected_folder:
        show_folder_details(selected_folder)
else:
    st.write("No folders available.")
