import csv
import pandas as pd
from typing import List, Optional


class Task:
    def __init__(self, task_id: int, name: str, category: str, time_period: str, priority: str, goal: str, task_type: str, genre: str, start_date: str, end_date: str, duration: int, percent_complete: int, predecessor: Optional[int], platform: Optional[str], device: Optional[str], language: Optional[str], framework: Optional[str], target_audience: Optional[str], medium: Optional[str], task_status: Optional[str], task_relationship: Optional[str], topic: Optional[str]):
        self.task_id = task_id
        self.name = name
        self.category = category
        self.time_period = time_period
        self.priority = priority
        self.goal = goal
        self.task_type = task_type
        self.genre = genre
        self.start_date = start_date
        self.end_date = end_date
        self.duration = duration
        self.percent_complete = percent_complete
        self.predecessor = predecessor
        self.platform = platform
        self.device = device
        self.language = language
        self.framework = framework
        self.target_audience = target_audience
        self.medium = medium
        self.task_status = task_status
        self.task_relationship = task_relationship
        self.topic = topic


class Goal:
    def __init__(self, goal_id: int, name: str, category: str, time_period: str, priority: str, goal: str, task_type: str, genre: str, start_date: str, end_date: str, duration: int, percent_complete: int, predecessor: Optional[int], platform: Optional[str], device: Optional[str], language: Optional[str], framework: Optional[str], target_audience: Optional[str], medium: Optional[str], task_status: Optional[str], task_relationship: Optional[str], topic: Optional[str]):
        self.goal_id = goal_id
        self.name = name
        self.category = category
        self.time_period = time_period
        self.priority = priority
        self.goal = goal
        self.task_type = task_type
        self.genre = genre
        self.start_date = start_date
        self.end_date = end_date
        self.duration = duration
        self.percent_complete = percent_complete
        self.predecessor = predecessor
        self.platform = platform
        self.device = device
        self.language = language
        self.framework = framework
        self.target_audience = target_audience
        self.medium = medium
        self.task_status = task_status
        self.task_relationship = task_relationship
        self.topic = topic
        self.tasks: List[Task] = []

    def add_task(self, task: Task):
        self.tasks.append(task)


class Project:
    def __init__(self, name: str, status: str = "Idea", progress_percentage: int = 0):
        self.name = name
        self.status = status
        self.progress_percentage = progress_percentage
        self.goals: List[Goal] = []

    def add_goal(self, goal: Goal):
        self.goals.append(goal)

    def update_status(self, new_status: str):
        self.status = new_status

    def update_progress_percentage(self, new_progress_percentage: int):
        self.progress_percentage = new_progress_percentage

    def export_to_csv(self, filename: str):
        data = []
        for goal in self.goals:
            goal_data = [goal.goal_id, goal.name, "Goal"] + [getattr(goal, attr) for attr in vars(goal) if attr not in ["goal_id", "name", "tasks"]]
            data.append(goal_data)

            for task in goal.tasks:
                task_data = [task.task_id, task.name, f"Task (Goal {goal.goal_id})"] + [getattr(task, attr) for attr in vars(task) if attr not in ["task_id", "name"]]
                data.append(task_data)

        columns = ["Item ID", "Item Name", "Item Type", "Category", "Time Period", "Priority", "Goal", "Task Type", "Genre", "Start Date", "End Date", "Duration (Days)", "% Complete", "Predecessor", "Platform", "Device", "Language", "Framework", "Target Audience", "Medium", "Task Status", "Task Relationship", "Topic"]
        df = pd.DataFrame(data, columns=columns)
        df.to_csv(filename, index=False)

# Create a project and add goals and tasks
my_project = Project("My Project", "Idea", 0)
""" my_project.update_status("Planning")
my_project.update_progress_percentage(20) """
goal_1 = Goal(1, "Goal 1", "Health", "By end of the month", "High", "Do", "Habit", "Physical", "01/01/2023", "31/01/2023", 31, 0, None, None, None, None, None, None, None, None, None, None)
task_1_1 = Task(2, "Task 1.1", "Health", "By end of the week", "High", "Do", "Project", "Physical", "01/01/2023", "07/01/2023", 7, 0, None, None, None, None, None, None, None, None, None, None)
goal_1.add_task(task_1_1)
my_project.add_goal(goal_1)
# Export the project data to a CSV file
my_project.export_to_csv("projects.csv")