from datetime import datetime, timedelta
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import random


Base = declarative_base()

def generate_unique_id():
    random_id = random.randint(10000000, 99999999)  # Generate a random 8-digit number
    return random_id

class Folder(Base):
    __tablename__ = 'folders'

    # produce a random number for the folder id
    id = Column(Integer, primary_key=True, default=generate_unique_id)
    title = Column(String(64), nullable=False)
    folder_dir = Column(String, nullable=False)
    date_modified = Column(DateTime, default=datetime.utcnow)
    
    projects = relationship('Project', backref='folder')
    attachments = relationship('Attachment', backref='folder')
    notes = relationship('Note', backref='folder')

class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True, default=generate_unique_id)
    date_created = Column(DateTime, default=datetime.utcnow)
    date_modified = Column(DateTime, default=datetime.utcnow)
    identifying_type = Column(String, default="project")

    completed = Column(Boolean, default=False)
    datetime_completed = Column(DateTime, nullable=True)
    actual_time_to_complete = Column(Integer, nullable=True)

    # Page 1
    folder_id = Column(Integer, ForeignKey('folders.id'))
    folder_dir = Column(String, nullable=False)
    title = Column(String, nullable=False)
    
    # Page 2
    description = Column(String, nullable=True)
    priority = Column(String, default="None")
    status = Column(String, default="None")

    # Page 3
    estimated_time_to_complete_checkbox = Column(Boolean, default=False)
    estimated_time_to_complete = Column(Integer, nullable=True)
    no_start_date = Column(Boolean, default=False)
    start_date = Column(DateTime, nullable=True)
    no_due_date = Column(Boolean, default=False)
    due_date = Column(DateTime, nullable=True)

    # Page 4
    category = Column(String, default="None")
    goal_verb = Column(String, default="None")
    genre = Column(String, default="None")
    use_case = Column(String, default="None")

    deliverables = relationship('Deliverable', backref='project')
    tasks = relationship('Task', backref='project')
    milestones = relationship('Milestone', backref='project')

    notes = relationship('Note', backref='project')
    attachments = relationship('Attachment', backref='project')

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, default=generate_unique_id)
    date_created = Column(DateTime, default=datetime.utcnow)
    date_modified = Column(DateTime, default=datetime.utcnow)
    completed = Column(Boolean, default=False)
    datetime_completed = Column(DateTime, nullable=True)
    actual_outcome = Column(String, nullable=True)

    folder_dir = Column(String, nullable=False)
    identifying_type = Column(String, default="task")

    title = Column(String)
    description = Column(String)

    category = Column(String, default="None")
    goal_verb = Column(String, default="None")
    genre = Column(String, default="None")
    use_case = Column(String, default="None")

    status = Column(String, default="None")
    priority = Column(String, default="None")

    no_start_date = Column(Boolean, default=False)
    start_date = Column(DateTime, nullable=True)

    estimated_time_to_complete_checkbox = Column(Boolean, default=False)
    estimated_time_to_complete = Column(Integer, nullable=True)

    no_due_date = Column(Boolean, default=False)
    due_date = Column(DateTime, nullable=True)

    dependencies = Column(String, nullable=True)
    desired_outcome = Column(String, nullable=True)

    project_id = Column(Integer, ForeignKey('projects.id'))

    subtasks = relationship('SubTask', backref='task')

class SubTask(Base):
    __tablename__ = 'subtasks'
    
    id = Column(Integer, primary_key=True, default=generate_unique_id)
    identifying_type = Column(String, default="subtask")
    date_created = Column(DateTime, default=datetime.utcnow)
    date_modified = Column(DateTime, default=datetime.utcnow)
    completed = Column(Boolean, default=False)

    folder_dir = Column(String, nullable=False)
    title = Column(String(64), nullable=False)

    priority = Column(String, default="None")
    status = Column(String, default="None")

    no_due_date = Column(Boolean, default=False)
    due_date = Column(DateTime, nullable=True)

    category = Column(String, default="None")
    goal_verb = Column(String, default="None")
    genre = Column(String, default="None")
    use_case = Column(String, default="None")

    task_id = Column(Integer, ForeignKey('tasks.id'))

class Deliverable(Base):
    __tablename__ = 'deliverables'

    id = Column(Integer, primary_key=True, default=generate_unique_id)
    date_created = Column(DateTime, default=datetime.utcnow)
    date_modified = Column(DateTime, default=datetime.utcnow)
    title = Column(String)
    folder_dir = Column(String, nullable=False)
    identifying_type = Column(String, default="deliverable")

    description = Column(String, nullable=True)

    category = Column(String, default="None")
    goal_verb = Column(String, default="None")
    genre = Column(String, default="None")
    use_case = Column(String, default="None")

    completed = Column(Boolean, default=False)
    datetime_completed = Column(DateTime)
    no_due_date = Column(Boolean, default=False)
    due_date = Column(DateTime, nullable=True)

    status = Column(String, default="None")
    priority = Column(String, default="None")

    dependencies = Column(String, nullable=True)
    quality_criteria = Column(String, nullable=True)
    acceptance_criteria = Column(String, nullable=True)

    project_id = Column(Integer, ForeignKey('projects.id'))

class Milestone(Base):
    __tablename__ = 'milestones'

    id = Column(Integer, primary_key=True, default=generate_unique_id)
    date_created = Column(DateTime, default=datetime.utcnow)
    date_modified = Column(DateTime, default=datetime.utcnow)
    title = Column(String)
    description = Column(String)

    folder_dir = Column(String, nullable=False)
    identifying_type = Column(String, default="milestone")

    category = Column(String, default="None")
    goal_verb = Column(String, default="None")
    genre = Column(String, default="None")
    use_case = Column(String, default="None")

    completed = Column(Boolean, default=False)
    datetime_completed = Column(DateTime)

    dependencies = Column(String, nullable=True)

    project_id = Column(Integer, ForeignKey('projects.id'))


class ToDo(Base):
    __tablename__ = 'todos'
    
    id = Column(Integer, primary_key=True, default=generate_unique_id)
    date_created = Column(DateTime, default=datetime.utcnow)
    date_modified = Column(DateTime, default=datetime.utcnow)
    title = Column(String(64), nullable=False)
    completed = Column(Boolean, default=False)
    identifying_type = Column(String, default="todo")

class Note(Base):
    __tablename__ = 'notes'

    id = Column(Integer, primary_key=True, default=generate_unique_id)
    title = Column(String)
    content = Column(String)
    folder_dir = Column(String, nullable=False)
    folder_id = Column(Integer, ForeignKey('folders.id'))
    project_id = Column(Integer, ForeignKey('projects.id'))
    task_id = Column(Integer, ForeignKey('tasks.id'))
    deliverable_id = Column(Integer, ForeignKey('deliverables.id'))
    milestone_id = Column(Integer, ForeignKey('milestones.id'))
    identifying_type = Column(String, default="note")

class Attachment(Base):
    __tablename__ = 'attachments'

    id = Column(Integer, primary_key=True, default=generate_unique_id)
    title = Column(String)
    folder_dir = Column(String, nullable=False)
    folder_id = Column(Integer, ForeignKey('folders.id'))
    project_id = Column(Integer, ForeignKey('projects.id'))
    identifying_type = Column(String, default="attachment")
