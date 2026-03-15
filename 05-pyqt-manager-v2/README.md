# PyQt Manager v2

> A modularized revision of the desktop productivity manager concept.

| Detail | Value |
|--------|-------|
| **Date** | ~June 2023 |
| **Status** | Archived Prototype |
| **Stack** | Python, PyQt6 |

---

## The Story

After four dated prototypes in a week, this version stepped back to think about architecture. Instead of one growing monolith, the code here separates concerns into modules: a `managers.py` for abstract utility functions, an `app/` directory with `item_manager.py`, `buttons.py`, and `layout.py` handling distinct parts of the interface.

It reads less like a feature push and more like an attempt to make the earlier ideas sustainable. The question shifted from "what should this app do?" to "how should this app be structured so I can keep building it?" That's a sign of growing engineering maturity, even if the result didn't become the final product.

The screenshot utilities (`ss1.py`, `ss2.py`) also hint at an early interest in capturing visual state — a thread that would become much more prominent in the macOS activity tracker and the eye-tracking experiments.

## What It Does

- Modular desktop application framework with separated layout, buttons, and item management
- Abstract manager pattern for utility functions
- Screenshot/state capture utilities
- Cleaner separation of concerns than earlier prototypes

## What's Inside

```
05-pyqt-manager-v2/
├── managers.py          # Abstract utility and manager functions
├── ss1.py               # Screenshot/state utility v1
├── ss2.py               # Screenshot/state utility v2
├── app/
│   ├── item_manager.py  # Item management logic
│   ├── buttons.py       # Button/UI component module
│   └── layout.py        # Layout management module
├── __pycache__/         # Python bytecode cache
├── Pipfile
└── Pipfile.lock
```

## What I Learned

That separating code into modules is not just a best practice — it's a survival strategy. The earlier prototypes had everything in one or two files, which made iteration fast but understanding slow. This version was the first to treat structure as a feature.

---

← [Prev: #04 PyQt Experiment](../04-pyqt-experiment/) | [Collection Home](../README.md) | [Next: #06 Streamlit Viz Lab](../06-streamlit-viz-lab/) →
