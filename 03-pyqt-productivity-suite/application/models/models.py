from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Folder(Base):
    __tablename__ = 'folders'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    
    projects = relationship('Project', backref='folder')
    todo_lists = relationship('ToDoList', backref='folder')
    attachments = relationship('Attachment', backref='folder')
    notes = relationship('Note', backref='folder')

class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True)
    folder_id = Column(Integer, ForeignKey('folders.id'))
    date_created = Column(DateTime)
    date_modified = Column(DateTime)
    folder_dir = Column(String)
    identifying_type = Column(String, default="project")
    actual_time_to_complete = Column(DateTime)

    title = Column(String)
    description = Column(String)
    status = Column(String)

    priority = Column(Integer)

    completed = Column(Boolean, default=False)
    datetime_completed = Column(DateTime)
    no_start_date = Column(Boolean, default=False)
    start_date = Column(DateTime)
    estimated_time_to_complete_checkbox = Column(Boolean, default=False)
    estimated_time_to_complete = Column(DateTime)
    no_due_date = Column(Boolean, default=False)
    datetime_due = Column(DateTime)

    deliverables = relationship('Deliverable', backref='project')
    tasks = relationship('Task', backref='project')
    milestones = relationship('Milestone', backref='project')

    category = Column(String)
    goal_verb = Column(String)
    genre = Column(String)
    use_case = Column(String)

    notes = relationship('Note', backref='project')
    attachments = relationship('Attachment', backref='project')


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    date_created = Column(DateTime)
    date_modified = Column(DateTime)
    title = Column(String)
    description = Column(String)
    folder_dir = Column(String)
    identifying_type = Column(String, default="task")
    priority = Column(Integer)
    status = Column(String)

    category = Column(String)
    goal_verb = Column(String)
    genre = Column(String)
    use_case = Column(String)

    completed = Column(Boolean, default=False)
    datetime_completed = Column(DateTime)

    no_start_date = Column(Boolean, default=False)
    start_date = Column(DateTime)

    estimated_time_to_complete_checkbox = Column(Boolean, default=False)
    estimated_time_to_complete = Column(DateTime)

    no_due_date = Column(Boolean, default=False)
    due_date = Column(DateTime)

    dependencies = Column(String)
    desired_outcome = Column(String)
    actual_outcome = Column(String)

    project_id = Column(Integer, ForeignKey('projects.id'))


class Deliverable(Base):
    __tablename__ = 'deliverables'

    id = Column(Integer, primary_key=True)
    date_created = Column(DateTime)
    date_modified = Column(DateTime)
    title = Column(String)
    folder_dir = Column(String)
    identifying_type = Column(String, default="deliverable")

    description = Column(String)
    category = Column(String)
    goal_verb = Column(String)
    genre = Column(String)
    use_case = Column(String)

    completed = Column(Boolean, default=False)
    datetime_completed = Column(DateTime)
    no_due_date = Column(Boolean, default=False)
    datetime_due = Column(DateTime)

    dependencies = Column(String)
    quality_criteria = Column(String)
    acceptance_criteria = Column(String)

    project_id = Column(Integer, ForeignKey('projects.id'))


class Milestone(Base):
    __tablename__ = 'milestones'

    id = Column(Integer, primary_key=True)
    date_created = Column(DateTime)
    date_modified = Column(DateTime)
    title = Column(String)
    description = Column(String)

    folder_dir = Column(String)
    identifying_type = Column(String, default="milestone")

    category = Column(String)
    goal_verb = Column(String)
    genre = Column(String)
    use_case = Column(String)

    completed = Column(Boolean, default=False)
    datetime_completed = Column(DateTime)
    no_due_date = Column(Boolean, default=False)
    datetime_due = Column(DateTime)

    dependencies = Column(String)

    project_id = Column(Integer, ForeignKey('projects.id'))


class Note(Base):
    __tablename__ = 'notes'

    id = Column(Integer, primary_key=True)
    content = Column(String)
    folder_id = Column(Integer, ForeignKey('folders.id'))
    project_id = Column(Integer, ForeignKey('projects.id'))
    task_id = Column(Integer, ForeignKey('tasks.id'))
    deliverable_id = Column(Integer, ForeignKey('deliverables.id'))
    milestone_id = Column(Integer, ForeignKey('milestones.id'))



class Attachment(Base):
    __tablename__ = 'attachments'

    id = Column(Integer, primary_key=True)
    file_path = Column(String)
    folder_id = Column(Integer, ForeignKey('folders.id'))
    project_id = Column(Integer, ForeignKey('projects.id'))




class SubTask(Base):
    __tablename__ = 'subtasks'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    due_date = Column(DateTime)
    completed = Column(Boolean, default=False)
    task_id = Column(Integer, ForeignKey('tasks.id'))

class ToDoList(Base):
    __tablename__ = 'todo_lists'
    
    id = Column(Integer, primary_key=True)
    item_name = Column(String(64), nullable=False)
    folder_id = Column(Integer, ForeignKey('folders.id'))
    completed = Column(Boolean, default=False)
    due_date = Column(DateTime)

