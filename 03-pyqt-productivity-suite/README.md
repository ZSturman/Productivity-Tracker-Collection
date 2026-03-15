# PyQt Productivity Suite

> The most ambitious early branch — kanban, gantt, calendar views, and a rich data schema.

| Detail | Value |
|--------|-------|
| **Date** | May 28, 2023 |
| **Status** | Archived Prototype |
| **Stack** | Python, PyQt5/6, SQLAlchemy, SQLite, Qt Designer (.ui files) |

---

## The Story

This is where the ambition became obvious. One day after the folder manager, the codebase explodes in scope. The UI loads from a `.ui` file designed in Qt Designer and organizes the application around five major sections: home, dashboard, productivity, data collection, and settings. Inside the productivity section alone it branches into kanban, gantt, calendar, table, and directory views. Even if some of those layouts were not fully finished, the intent is unmistakable: I was already trying to build a system that did much more than list tasks.

The database schema makes the same point even more clearly. By this point the data model includes Folder, Project, Task, Deliverable, Milestone, Note, Attachment, SubTask, and ToDoList. There are fields for creation and modification dates, status, priority, due dates, estimated completion, dependencies, desired outcome, actual outcome, acceptance criteria, and quality criteria. That is not a casual schema. It shows I was trying to capture not just whether something existed, but what kind of work it was, how it related to other work, and how expectations compared to reality.

This branch is the first point in the archive where the system stretches toward project management, planning, evidence collection, and analysis all at once. It was also the first time the ambition clearly exceeded the architecture — a pattern that would repeat.

## What It Does

- Multi-section desktop application with tab-based navigation
- Multiple project views: kanban board, gantt chart, calendar, table, and directory browser
- Rich entity schema with relationships and metadata
- Data collection section (foundations for tracking beyond tasks)
- Settings management
- Qt Designer `.ui` file for layout

## What's Inside

```
03-pyqt-productivity-suite/
├── main.py                      # Entry point — loads .ui, wires section navigation
├── main.ui                      # Qt Designer layout file
├── productivity.db              # SQLite database
├── application/
│   └── models/
│       └── models.py            # SQLAlchemy models (Folder, Project, Task, Deliverable,
│                                #   Milestone, Note, Attachment, SubTask, ToDoList)
├── Pipfile
└── Pipfile.lock
```

## What I Learned

That it's easy to design a schema that captures everything you want and hard to build a UI that makes all of it usable. The May 28 build has the most complete data model of any early version, but the interface couldn't keep up with the ambition. The lesson: a broad schema is a wish list. A finished product is the subset of that wish list you can actually ship.

This was also the first time I experienced the pull between "make it correct" and "make it work." The schema was correct — it modeled real project management concepts. But making it work as an application required more time than the rapid prototyping pace allowed.

---

← [Prev: #02 PyQt Folder Manager](../02-pyqt-folder-manager/) | [Collection Home](../README.md) | [Next: #04 PyQt Experiment](../04-pyqt-experiment/) →
