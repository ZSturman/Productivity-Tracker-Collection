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

json_file = "data.json"

# Load data from JSON file
data = read_json_data(json_file)

if "text" not in st.session_state:
    st.session_state.text = data['text']

if "edit_mode" not in st.session_state:
    st.session_state.edit_mode = False

st.markdown(f"**{st.session_state.text}**")

if st.button("Edit"):
    st.session_state.edit_mode = True

if st.session_state.edit_mode:
    with st.form("edit_text_form"):
        user_input = st.text_input("Edit the text", value=st.session_state.text)
        save_button = st.form_submit_button("Save")
        if save_button:
            if user_input.strip():  # Check if the input text is not empty
                st.session_state.text = user_input
                st.session_state.edit_mode = False
                
                # Update data and save it to the JSON file
                data['text'] = user_input
                write_json_data(json_file, data)
                
                st.experimental_rerun()
            else:
                st.warning("Text cannot be empty")  # Display warning message if the text is empty
