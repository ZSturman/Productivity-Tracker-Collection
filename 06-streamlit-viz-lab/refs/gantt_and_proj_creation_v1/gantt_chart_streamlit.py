import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
import numpy as np

# make streamlit wide
st.set_page_config(layout="wide")

# Set page title
st.title("Gantt Chart with Nested Tasks")

# Read the CSV file into a Pandas DataFrame
#df = pd.read_csv("project_gantt_chart_v2/gantt_data.csv")


def create_gannt_chart():
    df = pd.DataFrame([
        dict(Project="Project A", Task="Project A Task 1", Start='2017-01-01', Finish='2017-02-02', Resource='Complete'),
        dict(Project="Project A", Task="Project A Task 2", Start='2017-02-15', Finish='2017-03-15', Resource='Incomplete'),
        dict(Project="Project B", Task="Project B Task 1", Start='2017-01-17', Finish='2017-02-17', Resource='Not Started'),
        dict(Project="Project B", Task="Project B Task 2", Start='2017-01-17', Finish='2017-02-17', Resource='Complete'),
        dict(Project="Project C", Task="Project C Task 1", Start='2017-03-10', Finish='2017-03-20', Resource='Not Started'),
        dict(Project="Project C", Task="Project C Task 2", Start='2017-04-01', Finish='2017-04-20', Resource='Not Started'),
        dict(Project="Project C", Task="Project C Task 3", Start='2017-05-18', Finish='2017-06-18', Resource='Not Started'),
        dict(Project="Project D", Task="Project D Task 1", Start='2017-01-14', Finish='2017-03-14', Resource='Complete')
    ])


    # Create a Gantt chart with nested tasks
    fig = px.timeline(df, x_start="Start", x_end="Finish", y="Project", color="Resource", title="Gantt Chart with Nested Tasks")

    fig.update_yaxes(autorange="reversed")  # otherwise tasks are listed from the bottom up

    st.plotly_chart(fig, use_container_width=True)

    # Display the raw data
    st.subheader("Raw Data")
    st.write(df)














# Add histogram data
x1 = np.random.randn(200) - 2
x2 = np.random.randn(200)
x3 = np.random.randn(200) + 2

# Group data together
hist_data = [x1, x2, x3]

group_labels = ['Group 1', 'Group 2', 'Group 3']

# Create distplot with custom bin_size
fig = ff.create_distplot(
        hist_data, group_labels, bin_size=[.1, .25, .5])

# Plot!
st.plotly_chart(fig, use_container_width=True)