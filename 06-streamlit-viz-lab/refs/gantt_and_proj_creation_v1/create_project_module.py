import datetime
import uuid
from typing import Optional


class Project:
    def __init__(self):
        self.id = self.safe_id()
        self.date_created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.date_modified = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.editable_data = {}


    def safe_id(self):
        self.id = str(uuid.uuid4())
        self.id = self.id.replace("-", "_")
        self.id = self.id.replace(" ", "_")
        return self.id

    def edit_title_and_identifying_type(self, new_title: str, new_identifying_type: str):
        self.editable_data["required"] = {
            "title": new_title,
            "identifying_type": new_identifying_type,
        }


    def add_time(self, completed: Optional[bool] = False, date_completed: Optional[str] = None, time_completed: Optional[str] = None, started: Optional[bool] = False, date_started: Optional[str] = None, date_due: Optional[str] = None, time_period: Optional[str] = None, time_estimate: Optional[str] = None, time_spent: Optional[str] = None):
        self.editable_data["time"] = {
            "completed": False,
            "date_completed": date_completed,
            "time_completed": time_completed,
            "started": False,
            "date_started": date_started,
            "date_due": date_due,
            "time_period": time_period,
            "time_estimate": None,
            "time_spent": None,
        }

    def add_tools(self, language: Optional[str] = None, file_output: Optional[str] = None, medium: Optional[str] = None):
        self.editable_data["tools"] = {
            "language": language,
            "file_output": file_output,
            "medium": medium,
            "hardware_requirements": None,
            "software_requirements": None,
        }

    def add_descriptors(self, description: Optional[str] = None, category: Optional[str] = None, goal_verb: Optional[str] = None, genre: Optional[str] = None,use_case: Optional[str] = None, priority: Optional[str] = None, target_audience: Optional[str] = None, educational_topic: Optional[str] = None, social_impact: Optional[str] = None):
        self.editable_data["descriptors"] = {
            "description": description,
            "category": category,
            "goal_verb": goal_verb,
            "genre": genre,
            "use_case": use_case,
            "priority": priority,
            "target_audience": target_audience,
            "educational_topic": educational_topic,
            "social_impact": social_impact
        }

    def add_people(self, collaborators: Optional[list] = None, stakeholders: Optional[list] = None):
        self.editable_data["people"] = {
            "collaborators": collaborators,
            "stakeholders": stakeholders,
        }

    def add_progress(self, completion_percentage: Optional[int] = None, milestones: Optional[list] = None, status: Optional[str] = None):
        self.editable_data["progress"] = {
            "completion_percentage": completion_percentage,
            "milestones": milestones,
            "status": status,
        }

    def add_resources(self, budget: Optional[int] = None, expenses: Optional[int] = None, revenue: Optional[int] = None):
        self.editable_data["resources"] = {
            "budget": budget,
            "expenses": expenses,
            "revenue": revenue,
        }

    def add_notes(self, comments: Optional[str] = None, attachments: Optional[list] = None):
        self.editable_data["notes"] = {
            "comments": comments,
            "attachments": attachments,
        }

    def add_scheduling(self, is_recurring: Optional[bool] = None, recurrence_pattern: Optional[str] = None):
        self.editable_data["scheduling"] = {
            "is_recurring": is_recurring,
            "recurrence_pattern": recurrence_pattern,
        }


    def add_relationships(self, parent: Optional[str] = None, children: Optional[list] = None, look_ups: Optional[list] = None):
        self.editable_data["relationships"] = {
            "parent": parent,
            "children": children,
            "look_ups": look_ups,
        }











sections = {
        "required": [
            "required.title",
            "required.identifying_type"
        ],
        "time": [
            "time.completed",
            "time.date_completed",
            "time.time_completed",
            "time.started",
            "time.date_started",
            "time.time_started",
            "time.date_due",
            "time.due_day",
            "time.due_time_of_day",
            "time.time_period",
            "time.time_estimate",
            "time.time_spent"
        ],
        "tools": [
            "tools.language",
            "tools.file_output",
            "tools.medium",
            "tools.hardware_requirements",
            "tools.software_requirements"
        ],
        "descriptors": [
            "descriptors.description",
            "descriptors.category",
            "descriptors.goal_verb",
            "descriptors.genre",
            "descriptors.use_case",
            "descriptors.priority",
            "descriptors.target_audience",
            "descriptors.educational_topic",
            "descriptors.social_impact"
        ],
        "people": [
            "people.collaborators",
            "people.stakeholders"
        ],
        "progress": [
            "progress.completion_percentage",
            "progress.milestones",
            "progress.status"
        ],
        "resources": [
            "resources.budget",
            "resources.expenses",
            "resources.revenue"
        ],
        "notes": [
            "notes.comments",
            "notes.attachments"
        ],
        "scheduling": [
            "scheduling.is_recurring",
            "scheduling.recurrence_pattern"
        ]
    }

