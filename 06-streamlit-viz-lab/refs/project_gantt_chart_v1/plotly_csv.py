import pandas as pd
import plotly.graph_objects as go

# Read the CSV file into a Pandas DataFrame
df = pd.read_csv("project_schema_v2/gantt_data.csv")

# Get unique and sorted projects
projects = sorted(df['Project'].unique())

# Create a Gantt chart with nested tasks
fig = go.Figure()

# Iterate through projects and add tasks as shapes
for i, project in enumerate(projects):
    project_data = df[df['Project'] == project]

    for _, row in project_data.iterrows():
        task = row['Task']
        start = row['Start']
        finish = row['Finish']

        fig.add_shape(
            type="rect",
            x0=start,
            x1=finish,
            y0=i - 0.4,
            y1=i + 0.4,
            yref="y",
            fillcolor="blue",
            opacity=0.5,
            line=dict(width=0),
            layer="below",
            name=task
        )
        fig.add_annotation(
            x=(pd.to_datetime(start) + (pd.to_datetime(finish) - pd.to_datetime(start)) / 2),
            y=i,
            text=task,
            showarrow=False,
            font=dict(size=10, color="white"),
            xref="x",
            yref="y"
        )

# Update y-axis with project names
fig.update_yaxes(
    tickvals=list(range(len(projects))),
    ticktext=projects,
    title_text="Projects"
)

# Update x-axis and layout
fig.update_xaxes(title_text="Date", type='date')  # Make sure the x-axis is set to 'date'
fig.update_layout(title="Gantt Chart with Nested Tasks", plot_bgcolor="white")

# Display the Gantt chart
fig.show()
