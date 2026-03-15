


# Set page title
st.title("Gantt Chart with Nested Tasks")

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


if selected_folder:
    def render_folder_content(selected_folder):
        files = get_files(os.path.join(directory_path, selected_folder))
        folder_path = os.path.join(directory_path, selected_folder)
        st.sidebar.title(selected_folder)

        overview_tab, files_tab, tasks_tab, media_tab, notes_tab = st.sidebar.tabs(["Overview", "Files", "Tasks", "Media", "Notes"])

        with st.sidebar.expander("Select a different folder", expanded=False):
            new_selected_folder = st.sidebar.selectbox("Select a different folder", folder_list, index=folder_list.index(selected_folder) if selected_folder else 0)

        if new_selected_folder != selected_folder:
            selected_folder = new_selected_folder
            render_folder_content(selected_folder)  # Call the function to re-render the content of the newly selected folder

        with overview_tab:
            tab = "overview_tab"
            st.write(f"Overview of {selected_folder}")

        with files_tab:
            tab = "files_tab"
            st.write(f"Files in {selected_folder}")

        with tasks_tab:
            tab = "tasks_tab"
            st.write(f"Tasks in {selected_folder}")

        with media_tab:
            tab = "media_tab"
            st.write(f"Media in {selected_folder}")

        with notes_tab:
            tab = "notes_tab"
            st.write(f"Notes in {selected_folder}")


    render_folder_content(selected_folder)
