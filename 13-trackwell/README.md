# Trackwell

> An architectural reset in progress — old and new implementations coexisting in the same branch.

| Detail | Value |
|--------|-------|
| **Date** | August 25–30, 2023 |
| **Status** | Archived Prototype |
| **Stack** | Swift, SwiftUI, Core Data (in-memory models), Xcode |

---

## The Story

If you opened this project and saw two parallel sets of everything — `ViewModels/` alongside `NewVMs/`, `Views/` alongside `NewViews/` — your first thought might be that something went wrong. It didn't. This is what an architectural reset looks like when you're trying to keep momentum while reworking the foundations.

The dated file headers show the app beginning on August 25, then getting a redesign burst on August 30. The model layer shifts to in-memory structs (`ActionStateModel`, `InputModel`, `TriggerModel`, `ExecutionModel`) rather than pure Core Data dependence, while the "New" folders contain refactored view models and views that address structural issues in the originals. The Core Data schema is still present (`TrackwellCoreData.xcdatamodeld`), but the architecture is testing whether an in-memory layer could simplify the data flow.

The trigger types here are also interesting: `QuickActionButtonOne`, `QuickActionButtonTwo`, and `SwipeLeftOne` — suggesting experiments with different interaction styles for triggering execution.

This branch is important not for its feature set but for its honesty. It shows a developer (me) in the middle of a rethink, not at the end of one. The presence of both old and new architectures in the same project is a snapshot of the work in motion.

## What It Does

- Dual architecture: original ViewModels + new ViewModels (NewVMs)
- Dual views: original Views + new Views (NewViews)
- In-memory model layer: ActionStateModel, InputModel, TriggerModel, ExecutionModel
- Trigger interaction types: QuickActionButton, SwipeLeft
- Input types with defaults and blank handling
- Action and State execution with input chains
- Core Data backing with in-memory experiment layer

## What's Inside

```
13-trackwell/
├── Trackwell/
│   ├── TrackwellApp.swift                   # App entry point
│   ├── ContentView.swift                    # Home view
│   ├── Models/                              # Class-based Core Data models
│   │   ├── ActionState.swift
│   │   ├── Execution.swift
│   │   ├── Trigger.swift
│   │   └── Input.swift
│   ├── ViewModels/                          # Original 5 view models
│   ├── NewVMs/                              # Refactored 6 view models
│   │   ├── ActionStateVM.swift
│   │   ├── ExecutionVM.swift
│   │   ├── InputVM.swift
│   │   ├── TriggerVM.swift
│   │   ├── ActionStateListVM.swift
│   │   └── InputExecutionVM.swift
│   ├── Views/                               # Original views
│   ├── NewViews/                            # Refactored views
│   │   ├── NewHomeScreenView.swift
│   │   ├── ActionStateListViewNew.swift
│   │   ├── CreateEditActionStateViewNew.swift
│   │   └── ActionStateDetailedViewNew.swift
│   └── TrackwellCoreData.xcdatamodeld/      # Core Data schema
└── Trackwell.xcodeproj/
```

## What I Learned

That you can rethink the architecture without throwing away the project. The dual-implementation pattern — keeping old code working while building its replacement beside it — is messy but practical. It's how real refactors happen when you don't have the luxury of stopping everything to rewrite from scratch. The in-memory experiment also revealed that Core Data's save-and-fetch cycle adds friction that sometimes obscures the actual data logic.

---

← [Prev: #12 WellTrack](../12-welltrack/) | [Collection Home](../README.md) | [Next: #14 TrackingWell](../14-trackingwell/) →
