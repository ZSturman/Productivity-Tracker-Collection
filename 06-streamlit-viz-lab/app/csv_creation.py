import os
import pandas as pd
import streamlit as st

def create_csvs(directory_path, csv_folder):
    # load csv file
    productivity_csv_path = f"{directory_path}/{csv_folder}/productivity.csv"

    try:
        if os.stat(productivity_csv_path).st_size == 0:
            raise ValueError("Empty CSV file")
        productivity_csv = pd.read_csv(productivity_csv_path)
        updated_productivity_csv = productivity_csv[productivity_csv["folder_dir"].apply(lambda x: os.path.exists(x))]
        if not updated_productivity_csv.empty:
            updated_productivity_csv.to_csv(productivity_csv_path, index=False)
    except (FileNotFoundError, ValueError):
        df = pd.DataFrame(columns=["id", "date_created", "date_updated", "folder_dir", "file_name", "identifying_type", "title"])
        df.to_csv(productivity_csv_path, index=False)
        st.experimental_rerun()

        # load csv file
    relationships_csv_path = f"{directory_path}/{csv_folder}/relationships.csv"

    try:
        if os.stat(relationships_csv_path).st_size == 0:
            raise ValueError("Empty CSV file")
        relationships_csv = pd.read_csv(relationships_csv_path)
    except (FileNotFoundError, ValueError):
        df = pd.DataFrame(columns=["parent_id", "parent_type", "child_id", "child_type"])
        df.to_csv(relationships_csv_path, index=False)
        st.experimental_rerun()

    timeline_csv_path = f"{directory_path}/{csv_folder}/timeline.csv"

    try:
        if os.stat(timeline_csv_path).st_size == 0:
            raise ValueError("Empty CSV file")
        timeline_csv = pd.read_csv(timeline_csv_path)
    except (FileNotFoundError, ValueError):
        df = pd.DataFrame(columns=["id", "completed", "type", "title", "started", "estimated_duration", "actual_duration", "due_date"])
        df.to_csv(timeline_csv_path, index=False)
        st.experimental_rerun()

    return productivity_csv_path, relationships_csv_path, timeline_csv_path


