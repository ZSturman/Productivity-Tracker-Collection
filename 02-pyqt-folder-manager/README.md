# PyQt Folder Manager

> Two days after the first window: database-backed folders, projects, and tasks.

| Detail | Value |
|--------|-------|
| **Date** | May 27, 2023 |
| **Status** | Archived Prototype |
| **Stack** | Python, PyQt5, SQLAlchemy, SQLite |

---

## The Story

Two days after the bare window, the project already looked completely different. The single button was gone. In its place: a `FolderApp` with list widgets for folders, projects, and tasks, all backed by a SQLAlchemy database with models for `Session`, `Folder`, `Project`, and `Task`.

The speed of this jump says something about how urgently I wanted structure. I didn't stay in the toy stage for long. As soon as the interface existed, I wanted relationships, metadata, and persistence. This is the first version that acts like an organizer instead of a demo.

What it doesn't yet include is the broader life-modeling ambition that shows up later. It is still recognizably a productivity app in the conventional sense — create a folder, add a project, add tasks, mark things done. But the skeleton for something bigger is already forming in the data model.

## What It Does

- Creates and deletes folders
- Creates projects within folders and marks them complete
- Creates tasks within projects and marks them complete
- Persists everything to a SQLite database via SQLAlchemy ORM
- Refreshes list widgets to reflect current state

## What's Inside

```
02-pyqt-folder-manager/
├── main.py              # FolderApp — PyQt5 window with list widgets and CRUD controls
├── Pipfile              # Dependencies (PyQt5, SQLAlchemy)
└── Pipfile.lock
```

## What I Learned

That moving from UI proof-of-concept to database-backed persistence is the moment a prototype becomes useful. This version taught me that the real complexity isn't in the interface — it's in deciding how things relate to each other. Folders contain projects contain tasks. That hierarchy would echo through every later version, even when the names changed to action states, triggers, and executions.

---

← [Prev: #01 PyQt Hello World](../01-pyqt-hello-world/) | [Collection Home](../README.md) | [Next: #03 PyQt Productivity Suite](../03-pyqt-productivity-suite/) →
