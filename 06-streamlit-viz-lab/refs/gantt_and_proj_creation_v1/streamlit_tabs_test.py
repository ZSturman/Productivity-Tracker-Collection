import streamlit as st
from pathlib import Path

css_file = Path("gantt_and_proj_creation_v1/custom.css").read_text()

st.markdown(f"<style>{css_file}</style>", unsafe_allow_html=True)

if "edit_mode" not in st.session_state:
    st.session_state.edit_mode = False

if "edit_general" not in st.session_state:
    st.session_state.edit_general = False

if "edit_time" not in st.session_state:
    st.session_state.edit_time = False

if "edit_tools" not in st.session_state:
    st.session_state.edit_tools = False

if "save_successful" not in st.session_state:
    st.session_state.save_successful = False

if st.session_state.save_successful:
    st.success("Saved!")
    st.session_state.save_successful = False





def save(tab):
    st.session_state.edit_mode = False
    st.session_state.edit_general = False
    st.session_state.edit_time = False
    st.session_state.edit_tools = False
    st.session_state.save_successful = True

def edit_general(add_value=None):
    st.session_state.edit_mode = True
    st.session_state.edit_general = True
    st.session_state.edit_time = False
    st.session_state.edit_tools = False
    if add_value:
        st.text_input("Add to general", key=1)
        st.button("Save General", key=11, on_click=save, args=("General",))

def edit_time(add_value=None):
    st.session_state.edit_mode = True
    st.session_state.edit_general = False
    st.session_state.edit_time = True
    st.session_state.edit_tools = False

def edit_tools(add_value=None):
    st.session_state.edit_mode = True
    st.session_state.edit_general = False
    st.session_state.edit_time = False
    st.session_state.edit_tools = True




general_tab, time_tab, tools_tab = st.tabs(["General", "Time", "Tools"])


if st.session_state.edit_mode:
    if st.session_state.edit_general:
        st.write("Edit General")
        st.button("Save General", on_click=save, args=("General",))
    elif st.session_state.edit_time:
        st.write("Edit Time")
        st.button("Save Time", on_click=save, args=("Time",))
    elif st.session_state.edit_tools:
        st.write("Edit Tools")
        st.button("Save Tools", on_click=save, args=("Tools",))



with general_tab:
    if not st.session_state.edit_mode:
        st.write("Content for Tab 1")
        if st.session_state.edit_general:
            st.text_input("Add to general", key=1)
            st.button("Save General", key=11, on_click=save, args=("General",))


        st.button("Edit General", key=5, on_click=edit_general)
        st.button("Add To General", key=8, on_click=edit_general, args=(1,))
with time_tab:
    st.write("Content for Tab 2")
    if not st.session_state.edit_mode:
        st.button("Edit Time", key=6, on_click=edit_time)
        st.button("Add To Time", key=9, on_click=edit_time, args=(1,))
with tools_tab:
    st.write("Content for Tab 3")
    if not st.session_state.edit_mode:
        st.button("Edit Tools", key=7, on_click=edit_tools)
        st.button("Add To Tools", key=10, on_click=edit_tools, args=(1,))






