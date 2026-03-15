# Streamlit Viz Lab

> Gantt charts, dashboards, and schema experiments — a laboratory for seeing projects over time.

| Detail | Value |
|--------|-------|
| **Date** | ~June 2023 |
| **Status** | Archived Prototype |
| **Stack** | Python 3.11, Streamlit, Plotly, Pandas, PyQt6, SQLAlchemy |

---

## The Story

This folder reads like a companion laboratory to the earlier desktop prototypes — not a single application, but a workshop full of interface and structure experiments. The questions had shifted. I wasn't just asking "how do I create and complete tasks?" anymore. I was asking "how do I represent projects visually?", "how do I see them over time?", "how do I browse structural hierarchies?", and "which interface technology makes these questions easiest to answer?"

Streamlit and Plotly became the tools of choice here because they let me prototype visualizations fast — gantt charts, timeline views, folder browsers — without getting stuck in the layout complexity of PyQt. There are multiple versions of gantt chart implementations, a schema design experiment, and various UI test files exploring selectboxes, page layouts, and data-driven dashboards.

I read this folder as a transitional layer between the first desktop organizer ideas and the later analytics-heavy thinking. It's less polished than the more defined branches, but it represents a real move toward visualization and schema design that informed everything after it.

## What It Does

- **Streamlit folder browser** (`simple_streamlit.py`) — dynamic folder creation with sidebar navigation
- **Dashboard and gantt visualization** (`main_page_design_stuff.py`) — Plotly timelines with project/task hierarchy, tabbed interface (Overview, Files, Tasks, Media, Notes)
- **Gantt chart v1** (`project_gantt_chart_v1/`) — Plotly-based gantt from CSV and JSON data
- **Gantt chart v2** (`project_gantt_chart_v2/`) — Streamlit-native gantt implementation
- **Project schema design** (`project_schema_v0/`) — early data structure experiments
- **CRUD operations** (`app/add_edit_delete_funcs.py`) — folder/project/task/milestone creation with JSON storage and CSV relationship tracking
- **Session state experiments** — Streamlit session management and selectbox UI patterns

## What's Inside

```
06-streamlit-viz-lab/
├── simple_streamlit.py              # Streamlit folder app
├── main_page_design_stuff.py        # Dashboard and gantt visualization experiments
├── ss4.py                           # UI experiment
├── ss5.py                           # UI experiment (from manager variant)
├── temp_selectbox_stuff.py          # Selectbox UI patterns
├── create_session_state.py          # Session state management
├── pythonic_layout_struct.py        # Python layout structure experiments
├── temp_gannt.py                    # Gantt chart experiment
├── data.json                        # Sample data
├── list.txt                         # Hierarchical taxonomy of categories
├── session_modes_table.csv          # Session configuration
├── to_do_list.txt                   # Task list data
├── Pipfile                          # Dependencies (plotly, pandas, streamlit)
├── app/                             # Core application CRUD logic
├── gantt_and_proj_creation_v1/      # Combined gantt and project creation
├── project_gantt_chart_v1/          # Plotly gantt (CSV + JSON)
├── project_gantt_chart_v2/          # Streamlit gantt
├── project_schema_v0/              # Early schema design
├── productivity/                    # Core productivity module with CSV data
├── old_py_files/                    # Archive of earlier approaches
├── refs/                            # Reference material
└── from-manager-variant/            # Files from a parallel version (app, productivity, refs, ss4.py)
```

## What I Learned

That visualization isn't decoration — it's discovery. Seeing tasks on a timeline revealed structural problems that a flat list never could. This laboratory also taught me that testing multiple interface technologies in parallel (Streamlit vs. PyQt) is faster than committing to one too early. The best tool depends on the question you're asking, not the tool you already know.

---

← [Prev: #05 PyQt Manager v2](../05-pyqt-manager-v2/) | [Collection Home](../README.md) | [Next: #07 macOS Activity Tracker](../07-macos-activity-tracker/) →
