# Productivity Tracker Collection

> An archive of twenty attempts to measure life, work, attention, and well-being well enough to improve them.

[![Productivity analytics workspace banner](https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=1600&q=80)](https://unsplash.com/photos/person-using-macbook-pro-on-brown-wooden-table-XJXWbfSo2f0)

This is not one product. It is a collection of twenty separate attempts, built across different languages, frameworks, and levels of ambition, all circling the same question:

> *If I could capture enough variables about my day, behavior, environment, work, and internal state, could I understand wshat helps, what hurts, and what needs to change?*

Some folders hold working prototypes. Some hold specifications that never became code. Some are machine learning experiments. Some are research notes and photographed sketches. Together they span May 2023 through September 2024 and move through Python desktop apps, Streamlit dashboards, macOS telemetry scripts, computer vision experiments, seven SwiftUI/Core Data iOS branches, neuroscience research, and two full product specifications.

Think of the repository as an anthology rather than a single application. Each numbered folder is self-contained. They share a thematic thread, but they are not chapters of one codebase. Some are sequels, some are dead ends, and some are the clearest version of an idea at that moment.

## At a Glance

- **What this repo is:** an archive of experiments around productivity, self-tracking, behavioral telemetry, and personal analytics.
- **What this repo is not:** one installable monolith with a single build path.
- **Best way to browse:** start at any folder README, or read in chronological order from `01` to `20`.
- **Most mature implementation concept:** the SwiftUI action-state line and the macOS activity tracker.
- **Best long-form narrative:** [STORY.md](STORY.md).

## How to Navigate This Collection

Each project folder is numbered in roughly chronological order and named to hint at what's inside:

| # | Project | Date | Status | What It Is |
|---|---------|------|--------|------------|
| 01 | [PyQt Hello World](01-pyqt-hello-world/) | May 25, 2023 | Archived Prototype | The smallest possible starting point — a PyQt window with a button |
| 02 | [PyQt Folder Manager](02-pyqt-folder-manager/) | May 27, 2023 | Archived Prototype | Two days later: database-backed folders, projects, and tasks |
| 03 | [PyQt Productivity Suite](03-pyqt-productivity-suite/) | May 28, 2023 | Archived Prototype | The most ambitious early branch — kanban, gantt, calendar, rich schema |
| 04 | [PyQt Experiment](04-pyqt-experiment/) | May 31, 2023 | Archived Prototype | A lighter experiment that didn't replace the May 28 build |
| 05 | [PyQt Manager v2](05-pyqt-manager-v2/) | ~June 2023 | Archived Prototype | A modularized revision of the desktop manager concept |
| 06 | [Streamlit Viz Lab](06-streamlit-viz-lab/) | ~June 2023 | Archived Prototype | Gantt charts, dashboards, and schema experiments in Streamlit and Plotly |
| 07 | [macOS Activity Tracker](07-macos-activity-tracker/) | ~Mid 2023 | Working System | Passive behavioral telemetry — active window logging, OCR, NLP analysis |
| 08 | [Hand Gesture Tracker](08-hand-gesture-tracker/) | ~2023–2024 | Archived Prototype | MediaPipe hand tracking with gesture-to-action drawing canvas |
| 09 | [Eye Tracking ML](09-eye-tracking-ml/) | ~2023–2024 | Archived Prototype | dlib eye aspect ratio + synchronized screen/webcam recording |
| 10 | [Action States](10-action-states/) | Jul 22–27, 2023 | Archived Prototype | First SwiftUI/Core Data branch — action states, topics, tags, lists |
| 11 | [Action State Execution](11-action-state-execution/) | Jul 27 – Aug 3, 2023 | Archived Prototype | Execution tracking becomes a first-class concept |
| 12 | [WellTrack](12-welltrack/) | Aug 15–23, 2023 | Archived Prototype | Simplified core: action states, inputs, triggers, executions |
| 13 | [Trackwell](13-trackwell/) | Aug 25–30, 2023 | Archived Prototype | In-memory refactor with parallel old/new architecture |
| 14 | [TrackingWell](14-trackingwell/) | Aug 30, 2023 | Archived Prototype | Most production-ready Core Data branch with clean data layer |
| 15 | [TrackingWellness](15-trackingwellness/) | Aug 30, 2023 | Archived Prototype | Lightweight proof of concept — minimal singleton pattern |
| 16 | [Being Analytics](16-being-analytics/) | Sep 1–15, 2023 | Archived Prototype | Analytics-focused direction with service layer and dashboards |
| 17 | [Mental States Research](17-mental-states-research/) | ~2023 | Research Notes | Psychology framework for understanding focus and well-being |
| 18 | [Holistic Tracker Spec](18-holistic-tracker-spec/) | Oct 12, 2023 | Specification | Comprehensive system specification covering cognition, emotion, and behavior |
| 19 | [Sensory Input Research](19-sensory-input-research/) | May 7, 2024 | Research Notes | Neuroscience model of brain energy, attention, and cognitive processing |
| 20 | [InsightWell Spec](20-insightwell-spec/) | Sep 16, 2024 | Specification | Later product vision — ML-driven wellness and productivity analytics |

**Also in this repo:**

| Item | What It Is |
|------|------------|
| [STORY.md](STORY.md) | The full 1,500-line narrative walkthrough of this entire archive — the long version of the story each README tells in miniature |
| [topics.json](topics.json) | A taxonomy of 45 human motivations and needs (physical well-being, autonomy, creativity, resilience, gratitude, etc.) that forms the conceptual backbone of this work |
| [reference-materials/](reference-materials/) | iPad sketches, UI mockups, and photographs from the design process |

## The Arc, in Brief

**Phase 1 — Desktop Prototyping (May 2023):** The earliest attempts were Python desktop apps built in PyQt. They moved from a bare window to database-backed project management in four days. The ambition outpaced the architecture almost immediately.

**Phase 2 — Visualization & Schema Experiments (~June 2023):** Streamlit and Plotly experiments for gantt charts, dashboards, and organizational structure. A laboratory for testing how to see projects over time.

**Phase 3 — Behavioral Telemetry (~Mid 2023):** The work shifts from asking me what I did to watching what actually happened. A macOS tracker captures active windows, runs OCR on screen content, and uses NLP to categorize what I was looking at. This is where the project stops being a planner and starts becoming an analytics system.

**Phase 4 — Physical Input Experiments (~2023–2024):** Hand tracking with MediaPipe and eye tracking with dlib. Proofs of concept that physical signals, gestures, and gaze direction could become part of the data model.

**Phase 5 — SwiftUI Action State Line (Jul–Sep 2023):** Seven iterations of an iOS app, each exploring a different balance of data persistence, execution tracking, and architectural complexity. The concept of "action states" — modeling not just what you do, but the conditions and triggers around doing it — solidifies here.

**Phase 6 — Research & Theory (~2023–2024):** Psychology notes on mental states and focus. Neuroscience models of brain energy distribution. The theoretical foundation for why productivity cannot be reduced to a task list.

**Phase 7 — Product Specifications (Oct 2023 & Sep 2024):** Two comprehensive design documents that pull together everything learned into blueprints for integrated wellness and productivity platforms. No code, just the clearest articulation of what the system should become.

## Repository Notes

- Local development artifacts such as virtual environments, caches, Xcode user data, databases, logs, and screen recordings are excluded by the root `.gitignore`.
- README links across the collection point to paths that currently exist in the repository.
- The numbered folders are intentionally heterogeneous. Some contain source code, others contain notes, media, or specs.

## Reading Tips

- **Start with any project that interests you.** The numbered order is chronological, but each README is self-contained.
- **Use the navigation links** at the bottom of each project README to move forward or backward through the timeline.
- **Read [STORY.md](STORY.md)** if you want the unabridged version — the full narrative that connects all twenty projects into one continuous reflection.
- **The Swift projects (#10–#16)** are the densest cluster. They happen fast and in parallel. The individual READMEs explain what each one was trying differently.

## Tech Stack Across the Collection

| Category | Technologies |
|----------|-------------|
| **Desktop UI** | PyQt5/6, Streamlit |
| **iOS** | SwiftUI, Core Data |
| **Data & Visualization** | SQLAlchemy, SQLite, Plotly, Pandas, Matplotlib |
| **Machine Learning & CV** | dlib, OpenCV, MediaPipe, spaCy, gensim Word2Vec |
| **System Telemetry** | pynput, PyAutoGUI, pytesseract OCR, AppleScript |
| **Canvas & Interaction** | Pygame, PyAutoGUI |

---

*This collection represents roughly eighteen months of trying to turn observation into understanding. Not all of it worked. All of it changed the next iteration.*
