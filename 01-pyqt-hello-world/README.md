# PyQt Hello World

> The smallest possible starting point — a PyQt window with a button.

| Detail | Value |
|--------|-------|
| **Date** | May 25, 2023 |
| **Status** | Archived Prototype |
| **Stack** | Python, PyQt5 |

---

## The Story

This is where it all started, and it is almost comically small. A single Python file that opens a window with a button widget called `ButtonHolder`. That's it.

But it matters as evidence. Before any database schema, before any project management ambition, before any of the later complexity, the first concrete step was just getting a desktop interface to appear on screen. The question at this point wasn't "how do I model productivity?" — it was "can I make a window that responds to a click?"

Two days later the answer would become a full folder-project-task organizer. But on May 25, 2023, it was this: a loop, a widget, and proof that the work had moved from idea to application.

## What It Does

Launches a minimal PyQt5 desktop window containing a `ButtonHolder` widget. No persistence, no data model, no navigation — just the UI event loop running.

## What's Inside

```
01-pyqt-hello-world/
├── main.py              # Entry point — creates QApplication and ButtonHolder window
├── Pipfile              # Python dependencies (PyQt5)
└── Pipfile.lock         # Dependency lock file
```

## What I Learned

That starting is the hardest part, and the first version doesn't need to be impressive. It just needs to exist. The jump from "thinking about building something" to "having a running window" is the biggest jump in the whole archive, even though the code is the smallest.

---

← Start of Collection | [Collection Home](../README.md) | [Next: #02 PyQt Folder Manager](../02-pyqt-folder-manager/) →
