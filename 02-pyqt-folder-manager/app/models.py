from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    content = Column(Text)
    project_id = Column(Integer, ForeignKey('projects.id'))
    project = relationship('Project', backref='comments')

class Attachment(Base):
    __tablename__ = 'attachments'

    id = Column(Integer, primary_key=True)
    path = Column(String)
    project_id = Column(Integer, ForeignKey('projects.id'))
    project = relationship('Project', backref='attachments')
    folder_dir = Column(String)

class TaskDependency(Base):
    __tablename__ = 'task_dependencies'

    id = Column(Integer, primary_key=True)
    dependency_id = Column(Integer)
    task_id = Column(Integer, ForeignKey('tasks.id'))
    task = relationship('Task', backref='dependencies')

class MilestoneDependency(Base):
    __tablename__ = 'milestone_dependencies'

    id = Column(Integer, primary_key=True)
    dependency_id = Column(Integer)
    dependency_type = Column(String)
    milestone_id = Column(Integer, ForeignKey('milestones.id'))
    milestone = relationship('Milestone', backref='dependencies')

class DeliverableDependency(Base):
    __tablename__ = 'deliverable_dependencies'

    id = Column(Integer, primary_key=True)
    dependency = Column(String)
    deliverable_id = Column(Integer, ForeignKey('deliverables.id'))
    deliverable = relationship('Deliverable', backref='dependencies')

class QualityCriteria(Base):
    __tablename__ = 'quality_criteria'

    id = Column(Integer, primary_key=True)
    criteria = Column(Text)
    deliverable_id = Column(Integer, ForeignKey('deliverables.id'))
    deliverable = relationship('Deliverable', backref='quality_criteria')

class AcceptanceCriteria(Base):
    __tablename__ = 'acceptance_criteria'

    id = Column(Integer, primary_key=True)
    criteria = Column(Text)
    deliverable_id = Column(Integer, ForeignKey('deliverables.id'))
    deliverable = relationship('Deliverable', backref='acceptance_criteria')


class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True)
    date_created = Column(DateTime)
    date_modified = Column(DateTime)
    folder_dir = Column(String)
    identifying_type = Column(String, default="project")
    actual_time_to_complete = Column(Integer)
    title = Column(String)
    description = Column(Text)
    status = Column(String)
    priority = Column(String)
    completed = Column(Boolean, default=False)
    datetime_completed = Column(DateTime)
    no_start_date = Column(Boolean, default=False)
    start_date = Column(DateTime)
    estimated_time_to_complete_checkbox = Column(Boolean, default=False)
    estimated_time_to_complete = Column(Integer)
    no_due_date = Column(Boolean, default=False)
    datetime_due = Column(DateTime)
    category = Column(String)
    goal_verb = Column(String)
    genre = Column(String)
    use_case = Column(String)
    deliverables = relationship('Deliverable', back_populates='project')
    tasks = relationship('Task', back_populates='project')
    milestones = relationship('Milestone', back_populates='project')

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    date_created = Column(DateTime)
    date_modified = Column(DateTime)
    title = Column(String)
    description = Column(Text)
    folder_dir = Column(String)
    identifying_type = Column(String, default="task")
    priority = Column(String)
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
    estimated_time_to_complete = Column(Integer)
    no_due_date = Column(Boolean, default=False)
    datetime_due = Column(DateTime)
    desired_outcome = Column(String)
    actual_outcome = Column(String)
    project_id = Column(Integer, ForeignKey('projects.id'))
    project = relationship('Project', back_populates='tasks')

class Deliverable(Base):
    __tablename__ = 'deliverables'

    id = Column(Integer, primary_key=True)
    date_created = Column(DateTime)
    date_modified = Column(DateTime)
    title = Column(String)
    folder_dir = Column(String)
    identifying_type = Column(String, default="deliverable")
    description = Column(Text)
    category = Column(String)
    goal_verb = Column(String)
    genre = Column(String)
    use_case = Column(String)
    completed = Column(Boolean, default=False)
    datetime_completed = Column(DateTime)
    no_due_date = Column(Boolean, default=False)
    datetime_due = Column(DateTime)
    project_id = Column(Integer, ForeignKey('projects.id'))
    project = relationship('Project', back_populates='deliverables')

class Milestone(Base):
    __tablename__ = 'milestones'

    id = Column(Integer, primary_key=True)
    date_created = Column(DateTime)
    date_modified = Column(DateTime)
    title = Column(String)
    description = Column(Text)
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
    project_id = Column(Integer, ForeignKey('projects.id'))
    project = relationship('Project', back_populates='milestones')