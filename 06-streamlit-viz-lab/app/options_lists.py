import streamlit as st

category_options = ["None","Career", "Contribution", "Education", "Family", "Finance", "Fun & Recreation", "Health", "Hobbies", "Personal", "Personal Growth", "Relationship", "Social", "Spiritual", "Travel", "Wealth", "Work"]

goal_verb_options = ["None","Achieve", "Be", "Become", "Build", "Buy", "Complete", "Create", "Decrease", "Design", "Develop", "Discover", "Do", "Draw", "Earn", "Enjoy", "Experience", "Explore", "Finish", "Fix", "Grow", "Hate", "Have", "Help", "Improve", "Increase", "Invent", "Learn", "Love", "Maintain", "Make", "Master", "Move", "Obtain", "Organize", "Paint", "Plan", "Play", "Prepare", "Produce", "Publish", "Quit", "Research", "Review", "Run", "Save", "Sell", "Shop", "Sing", "Solve", "Spend", "Start", "Stop", "Streamline", "Study", "Support", "Teach", "Train", "Travel", "Walk", "Win", "Work", "Write"]

genre_options = ["None","Adventurous", "Analytical", "Creative", "Cultural", "Educational", "Emotional", "Environmental", "Financial", "Health", "Intellectual", "Occupational", "Physical", "Recreational", "Relationship", "Social", "Spiritual"]

use_case_options = ["None","Calendar", "Diary", "Goal tracking", "Habit tracking", "Journaling", "Note taking", "Planner", "Project management", "Reminder", "Scheduling", "Task list", "Task management", "Task manager", "Task organizer", "Task planner", "Task reminder", "Task scheduler", "Task timer", "Task tracker", "Time tracking", "To-do list"]

status_options = ["None","Canceled", "Deployment", "Design", "Development", "Idea", "Maintenance", "On Hold", "Planning", "Testing"]

time_conversion_factors = {
    "minutes": 1,
    "hours": 60,
    "days": 60*24,
    "weeks": 60*24*7,
    "months": 60*24*30,
    "years": 60*24*365
}


project_inputs = {
    "title": {
        "type": "text_input",
        "label": "Project Title *",
        "placeholder": "Enter Project title",
        "value": None,
        "help": "Enter the title of the project",
        "required": True
    },
    "description": {
        "type": "text_area",
        "label": "Project Description",
        "placeholder": "Enter Project description",
        "value": None,
        "help": "Enter the description of the project",
        "required": False
    },
    "status": {
        "type": "selectbox",
        "label": "Status",
        "placeholder": "Select Project status",
        "value": None,
        "help": "Select the status of the project",
        "required": False,
        "options": status_options
    },
    "priority": {
        "type": "number_input",
        "label": "Priority",
        "placeholder": "Enter Project priority",
        "value": None,
        "help": "Enter the priority of the project. (0 = lowest priority, 10 = highest priority)",
        "min_value": 0,
        "max_value": 10,
        "required": False
    },
    "category": {
        "type": "selectbox",
        "label": "Category",
        "placeholder": "Select Project category",
        "value": None,
        "help": "Select the category of the project",
        "required": False,
        "options": category_options
    },
    "goal_verb": {
        "type": "selectbox",
        "label": "Goal Verb",
        "placeholder": "Select Project goal verb",
        "value": None,
        "help": "Select the goal verb of the project",
        "required": False,
        "options": goal_verb_options
    },
    "genre": {
        "type": "selectbox",
        "label": "Genre",
        "placeholder": "Select Project genre",
        "value": None,
        "help": "Select the genre of the project",
        "required": False,
        "options": genre_options
    },
    "use_case": {
        "type": "selectbox",
        "label": "Use Case",
        "placeholder": "Select Project use case",
        "value": None,
        "help": "Select the use case of the project",
        "required": False,
        "options": use_case_options
    },
    "no_start_date": {
        "type": "checkbox",
        "label": "No Start Date",
        "placeholder": "Select Project no start date",
        "value": False,
        "help": "Select if the project has no start date",
        "required": False
    },
    "start_date": {
        "type": "date_input",
        "label": "Start Date",
        "placeholder": "Select Project start date",
        "value": None,
        "help": "Select the start date of the project",
        "required": False
    },
    "no_due_date": {
        "type": "checkbox",
        "label": "No Due Date",
        "placeholder": "Select Project no due date",
        "value": False,
        "help": "Select if the project has no due date",
        "required": False
    },
    "due_date": {
        "type": "date_input",
        "label": "Due Date",
        "placeholder": "Select Project due date",
        "value": None,
        "help": "Select the due date of the project",
        "required": False
    },
    "estimated_time_to_complete_checkbox": {
        "type": "checkbox",
        "label": "Estimated Time to Complete",
        "placeholder": "Select Project estimated time to complete",
        "value": False,
        "help": "Select if the project has an estimated time to complete",
        "required": False
    },
    "estimated_time_to_complete": {
        "type": "number_input",
        "label": "Estimated Time to Complete",
        "placeholder": "Enter Project estimated time to complete",
        "value": None,
        "help": "Enter the estimated time to complete the project",
        "required": False
    },
    "actual_time_to_complete": {
        "type": "number_input",
        "label": "Actual Time to Complete",
        "placeholder": "Enter Project actual time to complete",
        "value": None,
        "help": "Enter the actual time to complete the project",
        "required": False
    },
    "completed": {
        "type": "checkbox",
        "label": "Completed",
        "placeholder": "Select Project completed",
        "value": False,
        "help": "Select if the project is completed",
        "required": False
    },
    "datetime_completed": {
        "type": "datetime_input",
        "label": "Date and Time Completed",
        "placeholder": "Select Project date and time completed",
        "value": None,
        "help": "Select the date and time the project was completed",
        "required": False
    },
    "tasks": {
        "type": "list",
        "label": "Tasks",
        "placeholder": "Enter Project tasks",
        "value": [],
        "help": "Enter the tasks of the project",
        "required": False
    },
    "milestones": {
        "type": "list",
        "label": "Milestones",
        "placeholder": "Enter Project milestones",
        "value": [],
        "help": "Enter the milestones of the project",
        "required": False
    },
    "deliverables": {
        "type": "list",
        "label": "Deliverables",
        "placeholder": "Enter Project deliverables",
        "value": [],
        "help": "Enter the deliverables of the project",
        "required": False
    },
    "attachments": {
        "type": "file_uploader",
        "label": "Attachments",
        "placeholder": "Upload Project attachments",
        "value": [],
        "help": "Upload the attachments of the project",
        "required": False
    },
    "comments": {
        "type": "text_area",
        "label": "Comments",
        "placeholder": "Enter Project comments",
        "value": [],
        "help": "Enter the comments of the project",
        "required": False
    }
}




task_inputs = {
    "title": {
        "type": "text_input",
        "label": "Task Title *",
        "placeholder": "Enter Task title",
        "value": None,
        "help": "Enter the title of the task",
        "required": True
    },
    "description": {
        "type": "text_area",
        "label": "Task Description",
        "placeholder": "Enter Task description",
        "value": None,
        "help": "Enter the description of the task",
        "required": False
    },
    "status": {
        "type": "selectbox",
        "label": "Status",
        "placeholder": "Select Task status",
        "value": None,
        "help": "Select the status of the task",
        "required": False,
        "options": status_options
    },
    "priority": {
        "type": "number_input",
        "label": "Priority",
        "placeholder": "Enter Task priority",
        "value": None,
        "help": "Enter the priority of the task. (0 = lowest priority, 10 = highest priority)",
        "min_value": 0,
        "max_value": 10,
        "required": False
    },
    "category": {
        "type": "selectbox",
        "label": "Category",
        "placeholder": "Select Task category",
        "value": None,
        "help": "Select the category of the task",
        "required": False,
        "options": category_options
    },
    "goal_verb": {
        "type": "selectbox",
        "label": "Goal Verb",
        "placeholder": "Select Task goal verb",
        "value": None,
        "help": "Select the goal verb of the task",
        "required": False,
        "options": goal_verb_options
    },
    "genre": {
        "type": "selectbox",
        "label": "Genre",
        "placeholder": "Select Task genre",
        "value": None,
        "help": "Select the genre of the task",
        "required": False,
        "options": genre_options
    },
    "use_case": {
        "type": "selectbox",
        "label": "Use Case",
        "placeholder": "Select Task use case",
        "value": None,
        "help": "Select the use case of the task",
        "required": False,
        "options": use_case_options
    },
    "no_start_date": {
        "type": "checkbox",
        "label": "No Start Date",
        "placeholder": "Select Task no start date",
        "value": False,
        "help": "Select if the task has no start date",
        "required": False
    },
    "start_date": {
        "type": "date_input",
        "label": "Start Date",
        "placeholder": "Select Task start date",
        "value": None,
        "help": "Select the start date of the task",
        "required": False
    },
    "no_due_date": {
        "type": "checkbox",
        "label": "No Due Date",
        "placeholder": "Select Task no due date",
        "value": False,
        "help": "Select if the task has no due date",
        "required": False
    },
    "due_date": {
        "type": "date_input",
        "label": "Due Date",
        "placeholder": "Select Task due date",
        "value": None,
        "help": "Select the due date of the task",
        "required": False
    },
    "estimated_time_to_complete_checkbox": {
        "type": "checkbox",
        "label": "Estimated Time to Complete",
        "placeholder": "Select Task estimated time to complete",
        "value": False,
        "help": "Select if the task has an estimated time to complete",
        "required": False
    },
    "estimated_time_to_complete": {
        "type": "number_input",
        "label": "Estimated Time to Complete",
        "placeholder": "Enter Task estimated time to complete",
        "value": None,
        "help": "Enter the estimated time to complete the task",
        "required": False
    },
    "actual_time_to_complete": {
        "type": "number_input",
        "label": "Actual Time to Complete",
        "placeholder": "Enter Task actual time to complete",
        "value": None,
        "help": "Enter the actual time to complete the task",
        "required": False
    },
    "completed": {
        "type": "checkbox",
        "label": "Completed",
        "placeholder": "Select Task completed",
        "value": False,
        "help": "Select if the task is completed",
        "required": False
    },
    "datetime_completed": {
        "type": "datetime_input",
        "label": "Date and Time Completed",
        "placeholder": "Select Task date and time completed",
        "value": None,
        "help": "Select the date and time the task was completed",
        "required": False
    },
    "dependencies": {
        "type": "list",
        "label": "Dependencies",
        "placeholder": "Enter Task dependencies",
        "value": [],
        "help": "Enter the dependencies of the task",
        "required": False
    },
    "attachments": {
        "type": "file_uploader",
        "label": "Attachments",
        "placeholder": "Upload Task attachments",
        "value": [],
        "help": "Upload the attachments of the task",
        "required": False
    },
    "comments": {
        "type": "text_area",
        "label": "Comments",
        "placeholder": "Enter Task comments",
        "value": [],
        "help": "Enter the comments of the task",
        "required": False
    }
}






milestone_inputs = {
    "title": {
        "type": "text_input",
        "label": "Milestone Title *",
        "placeholder": "Enter Milestone title",
        "value": None,
        "help": "Enter the title of the milestone",
        "required": True
    },
    "description": {
        "type": "text_area",
        "label": "Milestone Description",
        "placeholder": "Enter Milestone description",
        "value": None,
        "help": "Enter the description of the milestone",
        "required": False
    },
    "category": {
        "type": "selectbox",
        "label": "Category",
        "placeholder": "Select Milestone category",
        "value": None,
        "help": "Select the category of the milestone",
        "required": False,
        "options": category_options
    },
    "goal_verb": {
        "type": "selectbox",
        "label": "Goal Verb",
        "placeholder": "Select Milestone goal verb",
        "value": None,
        "help": "Select the goal verb of the milestone",
        "required": False,
        "options": goal_verb_options
    },
    "genre": {
        "type": "selectbox",
        "label": "Genre",
        "placeholder": "Select Milestone genre",
        "value": None,
        "help": "Select the genre of the milestone",
        "required": False,
        "options": genre_options
    },
    "use_case": {
        "type": "selectbox",
        "label": "Use Case",
        "placeholder": "Select Milestone use case",
        "value": None,
        "help": "Select the use case of the milestone",
        "required": False,
        "options": use_case_options
    },
    "no_due_date": {
        "type": "checkbox",
        "label": "No Due Date",
        "placeholder": "Select Milestone no due date",
        "value": False,
        "help": "Select if the milestone has no due date",
        "required": False
    },
    "due_date": {
        "type": "date_input",
        "label": "Due Date",
        "placeholder": "Select Milestone due date",
        "value": None,
        "help": "Select the due date of the milestone",
        "required": False
    },
    "completed": {
        "type": "checkbox",
        "label": "Completed",
        "placeholder": "Select Milestone completed",
        "value": False,
        "help": "Select if the milestone is completed",
        "required": False
    },
    "datetime_completed": {
        "type": "datetime_input",
        "label": "Date and Time Completed",
        "placeholder": "Select Milestone date and time completed",
        "value": None,
        "help": "Select the date and time the milestone was completed",
        "required": False
    }
}



deliverable_inputs = {
    "title": {
        "type": "text_input",
        "label": "Deliverable Title *",
        "placeholder": "Enter Deliverable title",
        "value": None,
        "help": "Enter the title of the deliverable",
        "required": True
    },
    "description": {
        "type": "text_area",
        "label": "Deliverable Description",
        "placeholder": "Enter Deliverable description",
        "value": None,
        "help": "Enter the description of the deliverable",
        "required": False
    },
    "category": {
        "type": "selectbox",
        "label": "Category",
        "placeholder": "Select Deliverable category",
        "value": None,
        "help": "Select the category of the deliverable",
        "required": False,
        "options": category_options
    },
    "goal_verb": {
        "type": "selectbox",
        "label": "Goal Verb",
        "placeholder": "Select Deliverable goal verb",
        "value": None,
        "help": "Select the goal verb of the deliverable",
        "required": False,
        "options": goal_verb_options
    },
    "genre": {
        "type": "selectbox",
        "label": "Genre",
        "placeholder": "Select Deliverable genre",
        "value": None,
        "help": "Select the genre of the deliverable",
        "required": False,
        "options": genre_options
    },
    "use_case": {
        "type": "selectbox",
        "label": "Use Case",
        "placeholder": "Select Deliverable use case",
        "value": None,
        "help": "Select the use case of the deliverable",
        "required": False,
        "options": use_case_options
    },
    "no_due_date": {
        "type": "checkbox",
        "label": "No Due Date",
        "placeholder": "Select Deliverable no due date",
        "value": False,
        "help": "Select if the deliverable has no due date",
        "required": False
    },
    "due_date": {
        "type": "date_input",
        "label": "Due Date",
        "placeholder": "Select Deliverable due date",
        "value": None,
        "help": "Select the due date of the deliverable",
        "required": False
    },
    "completed": {
        "type": "checkbox",
        "label": "Completed",
        "placeholder": "Select Deliverable completed",
        "value": False,
        "help": "Select if the deliverable is completed",
        "required": False
    },
    "datetime_completed": {
        "type": "datetime_input",
        "label": "Date and Time Completed",
        "placeholder": "Select Deliverable date and time completed",
        "value": None,
        "help": "Select the date and time the deliverable was completed",
        "required": False
    },
    "dependencies": {
        "type": "list",
        "label": "Dependencies",
        "placeholder": "Enter Deliverable dependencies",
        "value": [],
        "help": "Enter the dependencies of the deliverable",
        "required": False
    },
    "quality_criteria": {
        "type": "text_area",
        "label": "Quality Criteria",
        "placeholder": "Enter Deliverable quality criteria",
        "value": None,
        "help": "Enter the quality criteria of the deliverable",
        "required": False
    },
    "acceptance_criteria": {
        "type": "text_area",
        "label": "Acceptance Criteria",
        "placeholder": "Enter Deliverable acceptance criteria",
        "value": None,
        "help": "Enter the acceptance criteria of the deliverable",
        "required": False
    },
}
