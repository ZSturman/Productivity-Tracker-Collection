# macOS Activity Tracker

> Passive behavioral telemetry — watching what actually happens instead of asking me to remember.

| Detail | Value |
|--------|-------|
| **Date** | ~Mid 2023 |
| **Status** | Working System |
| **Stack** | Python, pynput, AppleScript, pytesseract OCR, spaCy NLP, gensim Word2Vec |

---

## The Story

This is one of the most important shifts in the whole archive. Everything before this point was self-reported: I create a task, I mark it done, I organize it into a folder. This project flips that model. Instead of asking what I think I worked on, it records what was actually on screen and whether I was active.

The core tracker watches macOS in real time. It uses AppleScript to inspect the frontmost application, captures active app names, window titles, and document paths, special-cases Chrome to grab the active tab URL, normalizes Electron apps to Visual Studio Code, monitors keyboard and mouse activity to detect idleness, and writes everything to dated CSV files in iCloud storage. That alone is valuable — a ground-truth record of where my attention actually went.

But it goes further. The `txt_from_screen.py` pipeline captures multi-monitor screenshots, runs OCR with Tesseract, and then feeds the extracted text through spaCy NLP to identify nouns, named entities, POS tags, dependency pairs, and verbs. The question shifted from "was I active?" to "what was I looking at, and how can that be summarized automatically?" Then two additional labeling scripts — one using Google News Word2Vec, the other using spaCy similarity — attempt to automatically categorize screen content against semantic labels like topic, platform, framework, priority, and goal type.

If I had to point to a place where the project stopped being a planner and started becoming a personal analytics system, this is it.

## What It Does

- **Active window logging** — monitors frontmost macOS app, window title, document path, and Chrome tab URLs
- **Idle detection** — keyboard/mouse/scroll listeners with 10-second idle threshold
- **Screen OCR** — multi-monitor screenshot capture with Tesseract text extraction
- **NLP analysis** — spaCy pipeline extracts nouns, entities, POS tags, subject-object pairs, and verbs
- **Semantic labeling (Google)** — Word2Vec similarity scoring against 17+ category labels with confidence scores
- **Semantic labeling (spaCy)** — alternative labeling approach using spaCy embeddings
- **CSV output** — dated activity logs and organized/labeled information files

## What's Inside

```
07-macos-activity-tracker/
├── tracker_main.py                  # Core system — active window + idle tracking + CSV logging
├── txt_from_screen.py               # OCR + NLP pipeline (screenshot → text → analysis)
├── txt_from_screen_labels_google.py # Google Word2Vec semantic labeling
├── txt_from_screen_organizer.py     # Text data organizer v1
├── txt_from_screen_organizer2.py    # spaCy semantic labeling
├── logs/                            # Event logs (data stored to iCloud)
├── previous_versions/
│   └── tracker_main_v1.py           # Earlier tracker implementation
└── seperated modules/               # Modularized components
    ├── main.py                      # Module entry point
    ├── active_v_inactive.py         # Activity detection module
    ├── get_device_info.py           # Device information module
    └── get_window_title.py          # Window title extraction module
```

## What I Learned

That the hardest part of personal analytics isn't collection — it's interpretation. Recording what app is open is trivial. Understanding what that means for productivity requires NLP, categorization, and a framework for what "productive" even means in context. This project taught me that passive data collection is powerful, but the value lives in the analysis pipeline, not the raw logs.

Also: building system-level telemetry on macOS means learning AppleScript, which is its own kind of adventure.

---

← [Prev: #06 Streamlit Viz Lab](../06-streamlit-viz-lab/) | [Collection Home](../README.md) | [Next: #08 Hand Gesture Tracker](../08-hand-gesture-tracker/) →
