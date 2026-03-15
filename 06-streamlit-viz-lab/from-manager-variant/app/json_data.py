new_project_json_template = {
    "id": None,
    "date_created": None,
    "date_modified": None,
    "folder_dir": None,
    "identifying_type": "project",

    "actual_time_to_complete": None,

    "title": None,
    "description": None,
    "status": None,

    "priority": None,

    "completed": False,
    "datetime_completed": None,
    "no_start_date": False,
    "start_date": None,
    "estimated_time_to_complete_checkbox": False,
    "estimated_time_to_complete": None,
    "no_due_date": False,
    "datetime_due": None,

    "deliverables": [],
    "tasks": [],
    "milestones": [],

    "category": None,
    "goal_verb": None,
    "genre": None,
    "use_case": None,
    
    "comments": [],
    "attachments": [],
}

new_task_json_template = {
    "id": None,
    "date_created": None,
    "date_modified": None,
    "title": None,
    "description": None,
    "folder_dir": None,
    "identifying_type": "task",
    "priority": None,
    "status": None,

    "category": None,
    "goal_verb": None,
    "genre": None,
    "use_case": None,

    "completed": False,
    "datetime_completed": None,

    "no_start_date": False,
    "start_date": None,

    "estimated_time_to_complete_checkbox": False,
    "estimated_time_to_complete": None,

    "no_due_date": False,
    "datetime_due": None,

    "dependencies": [],
    "desired_outcome": None,
    "actual_outcome": None
}

new_deliverable_json_template = {
    "id": None,
    "date_created": None,
    "date_modified": None,
    "title": None,
    "folder_dir": None,
    "identifying_type": "deliverable",

    "description": None,
    "category": None,
    "goal_verb": None,
    "genre": None,
    "use_case": None,

    "completed": False,
    "datetime_completed": None,
    "no_due_date": False,
    "datetime_due": None,

    "dependencies": [],
    "quality_criteria": [],
    "acceptance_criteria": []
}

new_milestone_json_template = {
    "id": None,
    "date_created": None,
    "date_modified": None,
    "title": None,
    "description": None,

    "folder_dir": None,
    "identifying_type": "milestone",

    "category": None,
    "goal_verb": None,
    "genre": None,
    "use_case": None,

    "completed": False,
    "datetime_completed": None,
    "no_due_date": False,
    "datetime_due": None,

    "dependencies": []
}






productivity_json_template = {
    "folders": [
        {
            "id": None,
            "title": None,
            "projects": [
                {
                    "id": None,
                    "title": None,
                    "tasks": [
                        {
                            "id": None,
                            "title": None,
                        }
                    ],
                    "milestones": [
                        {
                            "id": None,
                            "title": None,
                        }
                    ],
                    "deliverables": [
                        {
                            "id": None,
                            "title": None,
                        }
                    ]
                }
            ]
        }
    ]
}