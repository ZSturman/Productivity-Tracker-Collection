import plotly.figure_factory as ff
import plotly.graph_objects as go
from datetime import datetime

def create_gantt_chart(tasks, title="Gantt Chart"):
    # Define color codes for each area
    area_colors = {
        'Health': 'rgb(255, 99, 71)',
        'Wealth': 'rgb(75, 192, 192)',
        'Relationship': 'rgb(255, 206, 86)',
        'Career': 'rgb(54, 162, 235)',
        'Personal Growth': 'rgb(153, 102, 255)',
        'Spirituality': 'rgb(201, 203, 207)',
        'Social Life': 'rgb(255, 159, 64)',
        'Family': 'rgb(255, 99, 132)',
        'Fun & Recreation': 'rgb(51, 255, 51)',
        'Contribution': 'rgb(0, 191, 255)'
    }




    # Prepare data for Gantt chart
    gantt_data = []
    for task in tasks:
        start = datetime.strptime(task['start'], '%Y-%m-%d')
        end = datetime.strptime(task['end'], '%Y-%m-%d')
        progress_duration = (end - start) * task['progress']
        progress_end = start + progress_duration
        gantt_data.append(dict(Task=task['name'],
                               Start=start,
                               Finish=end,
                               Complete=task['progress'],
                               Area=task['area'],
                               Quadrant=task['quadrant'],
                               Resource=task['resource'],
                               Color=area_colors[task['area']],
                               ProgressEnd=progress_end))

    # Create Gantt chart
    fig = ff.create_gantt(gantt_data, colors=area_colors, index_col='Area',
                          show_colorbar=True, group_tasks=True, showgrid_x=True, showgrid_y=True,
                          title=title, bar_width=0.2, show_hover_fill=True)
    
    # Add progress to each task
    for index, task in enumerate(gantt_data):
        fig.add_shape(type='rect', xref='x', yref='y',
                      x0=task['Start'], x1=task['ProgressEnd'],
                      y0=index - 0.1, y1=index + 0.1,
                      fillcolor=area_colors[task['Area']], opacity=0.6, layer='above')

        fig.add_annotation(x=task['Start'], y=index,
                           text=f"{task['Quadrant']} Quadrant",
                           showarrow=False, font=dict(color=area_colors[task['Area']]))



    # Customize layout
    fig.update_layout(autosize=True, hovermode='x unified')

    return fig


# Example tasks data
tasks = [
    {
        'name': 'Task 1',
        'start': '2023-04-01',
        'end': '2023-04-10',
        'progress': 1.0,
        'area': 'Health',
        'quadrant': 'I',
        'resource': 'User1'
    },
    {
        'name': 'Task 2',
        'start': '2023-04-11',
        'end': '2023-04-20',
        'progress': 0.5,
        'area': 'Wealth',
        'quadrant': 'II',
        'resource': 'User2'
    },
    {
        'name': 'Task 3',
        'start': '2023-04-15',
        'end': '2023-04-25',
        'progress': 0.8,
        'area': 'Career',
        'quadrant': 'III',
        'resource': 'User3'
    },
    {
        'name': 'Task 4',
        'start': '2023-04-21',
        'end': '2023-04-30',
        'progress': 0.2,
        'area': 'Personal Growth',
        'quadrant': 'IV',
        'resource': 'User4'
    }
    ]

gantt_chart = create_gantt_chart(tasks)
gantt_chart.show()