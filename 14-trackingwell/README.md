# TrackingWell

> The most production-ready Core Data branch — clean data layer, factory methods, and search infrastructure.

| Detail | Value |
|--------|-------|
| **Date** | August 30, 2023 |
| **Status** | Archived Prototype |
| **Stack** | Swift, SwiftUI, Core Data, Xcode |

---

## The Story

If one Swift branch in this collection looks most like the point where the architecture was settling, it's this one.

The `DataController.swift` file tells the story. It sets up an `NSPersistentContainer`, manages preview and test behavior, merges background changes automatically, and exposes clean helper methods: `exists()`, `delete()`, `saveChanges()`. It also includes factory methods for creating `ActionState`, `Trigger`, `Input`, `Execution`, and `InputExecution` entities — something no earlier branch had formalized.

The `SortAndFilter.swift` file adds `SearchConfig` and `Sort` capabilities, treating search and filter as explicit behavior built into the architecture rather than bolted on after the fact. The view model layer is organized and consistent, with six view models covering detail views, list views, create/edit flows, execution, and trigger management.

The input types mature here too: AskForText, SetText, AskForNumber, SetNumber, Calculate, GetLocation, and Date — a complete palette for structured data capture.

This version benefits from everything that came before it. The entity model from WellTrack, the architectural lessons from Trackwell's refactor, and the input-type comprehensiveness from Action State Execution all converge here into the cleanest implementation in the Swift line.

## What It Does

- **DataController** with factory methods for all entities
- Background change merging for Core Data
- Preview and test behavior management
- `SearchConfig` and `Sort` for filtering and ordering
- Input types: AskForText, SetText, AskForNumber, SetNumber, Calculate, GetLocation, Date
- Action vs State categorization with filtering
- Execution detail and list views
- Location tracking capability
- 6 organized view models, 15 views

## What's Inside

```
14-trackingwell/
├── TrackingWell/
│   ├── TrackingWellApp.swift                # App entry point
│   ├── ContentView.swift                    # Home view
│   ├── DataController.swift                 # Core Data stack with factory methods
│   ├── SortAndFilter.swift                  # SearchConfig and Sort infrastructure
│   ├── Models/
│   │   ├── ActionStateModel.swift           # Core entity model
│   │   ├── InputTypes.swift                 # Input type definitions
│   │   ├── ExecutionModel.swift             # Execution model
│   │   └── TriggerModel.swift               # Trigger model
│   ├── ViewModels/                          # 6 organized view models
│   │   ├── DetailedViewModel.swift
│   │   ├── ListViewModel.swift
│   │   ├── CreateEditViewModel.swift
│   │   ├── ExecutionViewModel.swift
│   │   └── TriggerViewModel.swift
│   ├── Views/                               # 15 SwiftUI views
│   └── TrackingWellCoreData.xcdatamodeld/   # Core Data schema
└── TrackingWell.xcodeproj/
```

## What I Learned

That a clean data layer makes everything else easier. Factory methods, consistent helpers, and explicit search/sort infrastructure might not be visible features, but they're what makes a codebase livable. This branch proved that the right architecture isn't about more features — it's about less friction between the features you have.

---

← [Prev: #13 Trackwell](../13-trackwell/) | [Collection Home](../README.md) | [Next: #15 TrackingWellness](../15-trackingwellness/) →
