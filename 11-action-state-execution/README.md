# Action State Execution

> Execution tracking becomes a first-class concept — modeling what actually happens, not just what could.

| Detail | Value |
|--------|-------|
| **Date** | July 27 – August 3, 2023 |
| **Status** | Archived Prototype |
| **Stack** | Swift, SwiftUI, Core Data, Xcode |

---

## The Story

This branch grows directly from Action States but adds something critical: the concept of execution. The previous version could define a state or an action and categorize it. This one starts modeling what happens when something is actually done.

That sounds obvious, but it's a significant change. A state system without execution tracking can describe possibilities. An execution-aware system begins to describe reality. The entity model introduces `ExecutionRecord` for the first time, alongside a rich set of field types — text, number, list, count, boolean, datetime, and location — that let executions capture structured data instead of just a "done" checkmark.

The architecture also matures here. There's a `FieldCreator` protocol that drives dynamic field rendering based on type, user settings management, and a more organized view hierarchy split by functional area: Executions, InputFields, Lists, TagsAndTopics, UserSettings.

The dates in the file headers show this branch starting the same day Action States' last file was created (July 27), making it essentially a continuation of the same creative push.

## What It Does

- **7 input field types**: Text, Number, List, Bool, Count, DateTime, Location + Upload
- Execution recording with structured input data
- `FieldCreator` protocol for type-driven dynamic field rendering
- User settings views and management
- Topic, tag, and list management (carried forward from Action States)
- View models for action states and executions

## What's Inside

```
11-action-state-execution/
├── ActionStateExecution/                    # Main app source
│   ├── ActionStateExecutionApp.swift        # App entry point
│   ├── ContentView.swift                    # Lists ActionStates with FetchRequest
│   ├── DataModel/
│   │   └── DataController.swift             # Core Data stack
│   ├── Protocols/
│   │   └── FieldCreator.swift               # Dynamic field rendering protocol
│   ├── Views/
│   │   ├── Executions/                      # Execution detail and row views
│   │   ├── InputFields/                     # 7+ field type views
│   │   ├── Lists/                           # List management
│   │   ├── TagsAndTopics/                   # Tag and topic views
│   │   └── UserSettings/                    # Settings views
│   ├── ViewModels/                          # Action state and execution VMs
│   └── ActionStatesCoreData.xcdatamodeld/   # Core Data schema
└── ActionStateExecution.xcodeproj/          # Xcode project
```

## What I Learned

That the gap between "defining what you want to do" and "recording what you actually did" is where all the useful data lives. A system that only tracks intentions is a todo list. A system that captures executions with structured inputs starts to generate the evidence needed for real analysis. The field-type system also taught me that flexibility in input types has to be designed upfront — bolting it on later is much harder.

---

← [Prev: #10 Action States](../10-action-states/) | [Collection Home](../README.md) | [Next: #12 WellTrack](../12-welltrack/) →
