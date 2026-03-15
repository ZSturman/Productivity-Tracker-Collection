import streamlit as st
import json

# Function to read JSON data from a file
def read_json_data(file_name):
    with open(file_name, 'r') as file:
        data = json.load(file)
    return data

# Function to write JSON data to a file
def write_json_data(file_name, data):
    with open(file_name, 'w') as file:
        json.dump(data, file)

def edit_data(json_path, key, old_data, new_data):
    # Load data from JSON file
    data = read_json_data(json_path)

    if key in data and data[key] == old_data:
        data[key] = new_data
        write_json_data(json_path, data)
        st.experimental_rerun()



if "edit_mode" not in st.session_state:
    st.session_state.edit_mode = False

if st.button("Edit"):
    st.session_state.edit_mode = True

