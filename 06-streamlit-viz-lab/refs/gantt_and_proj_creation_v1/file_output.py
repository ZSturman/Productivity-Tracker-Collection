import streamlit as st
from datetime import date
import json
import os
import pandas as pd
import base64


def file_output(files, folder_path, tab):
    for file in files:
        if tab == "media_tab":
            # if the file is a csv, display it as a dataframe
            if file.endswith(".csv"):
                df = pd.read_csv(os.path.join(folder_path, file))
                st.dataframe(df)
            # if the file is a png, display it as an image
            elif file.endswith(".png"):
                st.image(os.path.join(folder_path, file))
            # if the file is a txt, display it as text
            elif file.endswith(".txt"):
                with open(os.path.join(folder_path, file), "r") as f:
                    st.text(f.read())
                    # if the file is a mp4, display it as a video
            elif file.endswith(".mp4"):
                st.video(os.path.join(folder_path, file))
            # if the file is a pdf, display it as a pdf
            elif file.endswith(".pdf"):
                with open(os.path.join(folder_path, file), "rb") as f:
                    base64_pdf = base64.b64encode(f.read()).decode('utf-8')
                    pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf">'
                    st.markdown(pdf_display, unsafe_allow_html=True)
            # if the file is a jpg, display it as an image
            elif file.endswith(".jpg"):
                st.image(os.path.join(folder_path, file))
            # if the file is a jpeg, display it as an image
            elif file.endswith(".jpeg"):
                st.image(os.path.join(folder_path, file))
            # if the file is a gif, display it as an image
            elif file.endswith(".gif"):
                st.image(os.path.join(folder_path, file))
            # if the file is a tiff, display it as an image
            elif file.endswith(".tiff"):
                st.image(os.path.join(folder_path, file))
            # if the file is a wav, display it as an audio player
            elif file.endswith(".wav"):
                audio_file = open(os.path.join(folder_path, file), 'rb')
                audio_bytes = audio_file.read()
                st.audio(audio_bytes, format='audio/wav')
            # if the file is a mp3, display it as an audio player
            elif file.endswith(".mp3"):
                audio_file = open(os.path.join(folder_path, file), 'rb')
                audio_bytes = audio_file.read()
                st.audio(audio_bytes, format='audio/mp3')

        elif tab == "overview_tab":
            st.header("Overview")
            if file.endswith(".json"):
                # display_project_json(os.path.join(folder_path, file))
                if st.checkbox("Show JSON"):
                    with open(os.path.join(folder_path, file), "r") as f:
                        st.json(json.load(f))

        elif tab == "files_tab":
            st.header("An owl")
            st.image("https://static.streamlit.io/examples/owl.jpg", width=200)
        elif tab == "media_tab":
            st.header("A dog")
            st.image("https://static.streamlit.io/examples/dog.jpg", width=200)
        elif tab == "notes_tab":
            st.header("A cat")
            st.image("https://static.streamlit.io/examples/cat.jpg", width=200)


def display_project_json(json_file_path, project_data):
    with open(json_file_path, "r") as f:
        project_data = json.load(f)
        st.header(f"Project: {project_data['title']}")

        if "description" in project_data:
            st.write(project_data["description"])

        if "optional_data" in project_data:
            optional_data = project_data["optional_data"]
            if "time" in optional_data:
                st.write("Time:", optional_data["time"])


        if st.checkbox("Show Extra Bits", value=False, key=None):
            st.write("Date Created:", project_data["date_created"])
            if "date_modified" in project_data:
                st.write("Date Modified:", project_data["date_modified"])

        if st.checkbox("Show JSON", value=False, key=None):
            try:
                st.json(project_data)
            except KeyError:
                st.write("No JSON found.")




class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, date):
            return obj.isoformat()
        return super(DateEncoder, self).default(obj)