    # Check if dataframe is empty
    if df.empty:
        st.write("No data available")
    else:
        # Continue with your code if dataframe is not empty
        df['Task'] = df['title']
        df['Start'] = df['started']
        df['Finish'] = df['end_date_estimated']
        df['Resource'] = 'Estimated'
        estimated_tasks = df[['Task', 'Start', 'Finish', 'Resource']].to_dict('records')

        df['Start'] = df['started']
        df['Finish'] = df['end_date_actual']
        df['Resource'] = 'Actual'
        actual_tasks = df[['Task', 'Start', 'Finish', 'Resource']].to_dict('records')

        # Combine both lists
        tasks = estimated_tasks + actual_tasks

        # Check if tasks list is empty
        if not tasks:
            st.write("No tasks available")
        else:
            # Create a Gantt chart
            fig = ff.create_gantt(tasks, colors=['#333F44', '#93e4c1'], index_col='Resource', show_colorbar=True, group_tasks=True)

            # Add a vertical line indicating the current date
            fig.add_shape(
                type='line',
                x0=datetime.now(),
                x1=datetime.now(),
                y0=0,
                y1=1,
                yref='paper',
                line=dict(color='grey', width=3, dash='dot'),
            )

            # Display it in Streamlit
            st.plotly_chart(fig)