import random
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.models import Base  # import the base from your models module

engine = create_engine('sqlite:///productivity_app/data/test.db', echo=True)

Base.metadata.create_all(bind=engine)

from datetime import datetime, timedelta
from models.models import Folder, Project, Task, Deliverable, Attachment, Note, SubTask, ToDo, Milestone
from user_settings.combo_lists import status_options, category_options, goal_verb_options, genre_options, use_case_options

Session = sessionmaker(bind=engine)
session = Session()

# creating a test folder
folder = Folder(
    title="Test Folder",
    folder_dir="test/folder/dir",)
session.add(folder)
session.commit()

# creating a test project
project = Project(
    folder_id=folder.id,
    date_created=datetime.now(),
    date_modified=datetime.now(),
    folder_dir="test/folder/dir",
    title="Test Project",
    description="This is a test project",
    status=random.choice(status_options),
    priority="High",
    start_date=datetime.now(),
    due_date=datetime.now() + timedelta(days=7),
    category=random.choice(category_options),
    goal_verb=random.choice(goal_verb_options),
    genre=random.choice(genre_options),
    use_case=random.choice(use_case_options),
)
session.add(project)
session.commit()

# creating a test task
task = Task(
    date_created=datetime.now(),
    date_modified=datetime.now(),
    title="Test Task",
    description="This is a test task",
    folder_dir="test/folder/dir/task",
    priority="Medium",
    status=random.choice(status_options),
    category = random.choice(category_options),
    goal_verb = random.choice(goal_verb_options),
    genre = random.choice(genre_options),
    use_case = random.choice(use_case_options),
    start_date=datetime.now(),
    due_date=datetime.now() + timedelta(days=3),
    project_id=project.id
)
session.add(task)
session.commit()


# creating a test deliverable
deliverable = Deliverable(
    date_created=datetime.now(),
    date_modified=datetime.now(),
    title="Test Deliverable",
    folder_dir="test/folder/dir/deliverable",
    description="This is a test deliverable",
    category = random.choice(category_options),
    goal_verb = random.choice(goal_verb_options),
    genre = random.choice(genre_options),
    use_case = random.choice(use_case_options),
    due_date=datetime.now() + timedelta(days=5),
    project_id=project.id,
    status = random.choice(status_options),
    priority = "High"
)
session.add(deliverable)
session.commit()

# creating a test milestone
milestone = Milestone(
    date_created=datetime.now(),
    date_modified=datetime.now(),
    title="Test Milestone",
    description="This is a test milestone",
    folder_dir="test/folder/dir/milestone",
    category = random.choice(category_options),
    goal_verb = random.choice(goal_verb_options),
    genre = random.choice(genre_options),
    use_case = random.choice(use_case_options),
    due_date=datetime.now() + timedelta(days=10),
    project_id=project.id,
    status = random.choice(status_options),
    priority = "High"
)
session.add(milestone)
session.commit()

# creating a test note
note = Note(
    title="Test Note",
    content="This is a test note",
    folder_id=folder.id,
    project_id=project.id,
    task_id=task.id,
    deliverable_id=deliverable.id,
    milestone_id=milestone.id,
    folder_dir="test/folder/dir/note"
)
session.add(note)
session.commit()

# creating a test attachment
attachment = Attachment(
    title="Test Attachment",
    folder_dir="test/folder/dir/attachment",
    folder_id=folder.id,
    project_id=project.id
)
session.add(attachment)
session.commit()

# creating a test subtask
subtask = SubTask(
    title="Test SubTask",
    due_date=datetime.now() + timedelta(days=1),
    task_id=task.id,
    status = random.choice(status_options),
    category=random.choice(category_options),
    goal_verb=random.choice(goal_verb_options),
    genre=random.choice(genre_options),
    use_case=random.choice(use_case_options),
    priority = "Low",
    folder_dir="test/folder/dir/subtask"
)
session.add(subtask)
session.commit()

# creating a test todo list item
todo_list_item = ToDo(
    title="Test ToDoListItem",
    folder_id=folder.id,
    due_date=datetime.now() + timedelta(days=2),
    status = random.choice(status_options),
    category=random.choice(category_options),
    goal_verb=random.choice(goal_verb_options),
    genre=random.choice(genre_options),
    use_case=random.choice(use_case_options),
    priority = "Low",
    folder_dir="test/folder/dir/todo" 
)
session.add(todo_list_item)
session.commit()







# Test Data for Folder
folder1 = Folder(
    title="Folder 1",
    folder_dir="/home/user/documents/folder1",
)

session.add(folder1)
session.commit()

folder2 = Folder(
    title="Folder 2",
    folder_dir="/home/user/documents/folder2",
)

session.add(folder2)
session.commit()

# Test Data for Project
project1 = Project(
    folder_id=1,
    date_created=datetime.now(),
    date_modified=datetime.now(),
    folder_dir="/home/user/documents/folder1",
    title="Project 1",
    description="This is Project 1",
    status=random.choice(status_options),
    priority="Low",
    start_date=datetime.now(),
    due_date=datetime.now() + timedelta(days=17),
    category = random.choice(category_options),
    goal_verb = random.choice(goal_verb_options),
    genre = random.choice(genre_options),
    use_case = random.choice(use_case_options),
)

project2 = Project(
    folder_id=2,
    date_created=datetime.now(),
    date_modified=datetime.now(),
    folder_dir="/home/user/documents/folder2",
    title="Project 2",
    description="This is Project 2",
    status=random.choice(status_options),
    priority="Low",
    start_date=datetime.now(),
    due_date=datetime.now() + timedelta(days=27),
    category = random.choice(category_options),
    goal_verb = random.choice(goal_verb_options),
    genre = random.choice(genre_options),
    use_case = random.choice(use_case_options),
)

# Test Data for Task
task1 = Task(
    date_created=datetime.now(),
    date_modified=datetime.now(),
    title="Task 1",
    description="This is Task 1",
    folder_dir="/home/user/documents/folder1",
    priority="High",
    status=random.choice(status_options),
    project_id=1,
    category = random.choice(category_options),
    goal_verb = random.choice(goal_verb_options),
    genre = random.choice(genre_options),
    use_case = random.choice(use_case_options),
    start_date=datetime.now() + timedelta(days=1),
    due_date=datetime.now() + timedelta(days=3),
)

task2 = Task(
    date_created=datetime.now(),
    date_modified=datetime.now(),
    title="Task 2",
    description="This is Task 2",
    folder_dir="/home/user/documents/folder2",
    priority="Medium",
    status=random.choice(status_options),
    project_id=2,
    category = random.choice(category_options),
    goal_verb = random.choice(goal_verb_options),
    genre = random.choice(genre_options),
    use_case = random.choice(use_case_options),
    start_date=datetime.now() + timedelta(days=2),
    due_date=datetime.now() + timedelta(days=4),
)

# Test Data for Deliverable
deliverable1 = Deliverable(
    date_created=datetime.now(),
    date_modified=datetime.now(),
    title="Deliverable 1",
    folder_dir="/home/user/documents/folder1",
    description="This is Deliverable 1",
    project_id=1,
    category = random.choice(category_options),
    goal_verb = random.choice(goal_verb_options),
    genre = random.choice(genre_options),
    use_case = random.choice(use_case_options),
    due_date=datetime.now() + timedelta(days=3),
    status = random.choice(status_options),
    priority = "High",
)

deliverable2 = Deliverable(
    date_created=datetime.now(),
    date_modified=datetime.now(),
    title="Deliverable 2",
    folder_dir="/home/user/documents/folder2",
    description="This is Deliverable 2",
    project_id=2,
    category = random.choice(category_options),
    goal_verb = random.choice(goal_verb_options),
    genre = random.choice(genre_options),
    use_case = random.choice(use_case_options),
    due_date=datetime.now() + timedelta(days=5),
    status = random.choice(status_options),
    priority = "High",
)

# Test Data for Milestone
milestone1 = Milestone(
    date_created=datetime.now(),
    date_modified=datetime.now(),
    title="Milestone 1",
    description="This is Milestone 1",
    folder_dir="/home/user/documents/folder1",
    project_id=1,
    category = random.choice(category_options),
    goal_verb = random.choice(goal_verb_options),
    genre = random.choice(genre_options),
    use_case = random.choice(use_case_options),
    due_date=datetime.now() + timedelta(days=9),
    status = random.choice(status_options),
    priority = "Low",
)

milestone2 = Milestone(
    date_created=datetime.now(),
    date_modified=datetime.now(),
    title="Milestone 2",
    description="This is Milestone 2",
    folder_dir="/home/user/documents/folder2",
    project_id=2,
    category = random.choice(category_options),
    goal_verb = random.choice(goal_verb_options),
    genre = random.choice(genre_options),
    use_case = random.choice(use_case_options),
    due_date=datetime.now() + timedelta(days=7),
    status = random.choice(status_options),
    priority = "High",
)

# Test Data for Note
note1 = Note(
    title="Note 1",
    content="This is Note 1",
    folder_dir="/home/user/documents/folder1",
    folder_id=1,
)

note2 = Note(
    title="Note 2",
    content="This is Note 2",
    folder_dir="/home/user/documents/folder2",
    folder_id=2,
)

# Test Data for Attachment
attachment1 = Attachment(
    title="Attachment 1",
    folder_dir="/home/user/documents/folder1",
    folder_id=1,
)

attachment2 = Attachment(
    title="Attachment 2",
    folder_dir="/home/user/documents/folder2",
    folder_id=2,
)

# Test Data for SubTask
subtask1 = SubTask(
    title="SubTask 1",
    due_date=datetime.now(),
    folder_dir="/home/user/documents/folder1",
    task_id=1,
    status = random.choice(status_options),
    category=random.choice(category_options),
    goal_verb=random.choice(goal_verb_options),
    genre=random.choice(genre_options),
    use_case=random.choice(use_case_options),
    priority = "Low",
)

subtask2 = SubTask(
    title="SubTask 2",
    due_date=datetime.now(),
    folder_dir="/home/user/documents/folder2",
    task_id=2,
    status = random.choice(status_options),
    category=random.choice(category_options),
    goal_verb=random.choice(goal_verb_options),
    genre=random.choice(genre_options),
    use_case=random.choice(use_case_options),
    priority = "Medium",
)

# Test Data for ToDoList
todolist1 = ToDo(
    title="ToDoList 1",
    folder_dir="/home/user/documents/folder1",
    folder_id=1,
    due_date=datetime.now(),
    status = random.choice(status_options),
    category=random.choice(category_options),
    goal_verb=random.choice(goal_verb_options),
    genre=random.choice(genre_options),
    use_case=random.choice(use_case_options),
    priority = "Medium",
)

todolist2 = ToDo(
    title="ToDoList 2",
    folder_dir="/home/user/documents/folder2",
    folder_id=2,
    due_date=datetime.now(),
    status = random.choice(status_options),
    category=random.choice(category_options),
    goal_verb=random.choice(goal_verb_options),
    genre=random.choice(genre_options),
    use_case=random.choice(use_case_options),
    priority = "High",
)

session.add(project1)
session.commit()

session.add(project2)
session.commit()

session.add(task1)
session.commit()

session.add(task2)
session.commit()

session.add(deliverable1)
session.commit()

session.add(deliverable2)
session.commit()

session.add(milestone1)
session.commit()

session.add(milestone2)
session.commit()

session.add(note1)
session.commit()

session.add(note2)
session.commit()

session.add(attachment1)
session.commit()

session.add(attachment2)
session.commit()

session.add(subtask1)
session.commit()

session.add(subtask2)
session.commit()

session.add(todolist1)
session.commit()

session.add(todolist2)
session.commit()



print("Data added successfully.")