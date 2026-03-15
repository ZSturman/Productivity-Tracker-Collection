# WellTrack

> Simplified core — action states, inputs, triggers, and executions. Nothing else.

| Detail | Value |
|--------|-------|
| **Date** | August 15–23, 2023 |
| **Status** | Archived Prototype |
| **Stack** | Swift, SwiftUI, Core Data, Xcode |

---

## The Story

After the entity-heavy Action States branches, WellTrack makes a deliberate reduction. Instead of topics, tags, fields, and lists all competing for space, the structure centers on four concepts: `ActionState`, `Input`, `Trigger`, and `ExecutionRecord`. That's it.

The dated file headers show the build growing over about a week: action-state views on August 15, Input support on the 17th, triggers and execution views by the 19th through the 23rd. Each addition feels intentional rather than exploratory. The model has a clear inheritance chain — input classes like `AskForTextInput`, `AskForNumberInput`, `SetTextInput`, `SetNumberInput`, and `CalculateInput` all extend a template base class with prompt, default, and blank configuration.

This branch also includes a test plan (`WellTrack.xctestplan`) and a test suite — the first indication that testing was becoming part of the workflow, not just an afterthought.

The reduction to four core entities turns out to be a better fit for the actual tracking problem. What is a state? What triggers it? What input does it need? What execution does it produce? Those four questions are enough to model a surprising amount of behavior.

## What It Does

- Core model: ActionState → Input → Trigger → ExecutionRecord
- Sophisticated input chain with `previousInput`/`nextInput` relationships
- Input types: AskForText, AskForNumber, SetText, SetNumber, Calculate
- Trigger buttons with customizable text
- Execution records with timestamps and location data
- Output types: ExecutionString and ExecutionNumber
- Singleton `DataController` for Core Data management
- Test plan and test suite

## What's Inside

```
12-welltrack/
├── WellTrack/
│   ├── WellTrackApp.swift                    # App entry point
│   ├── ContentView.swift                     # Home view (8/15/23)
│   ├── Models/
│   │   ├── ActionState.swift                 # Core entity
│   │   ├── Input.swift                       # Input base class with chain support
│   │   ├── Trigger.swift                     # Trigger button model
│   │   └── ExecutionRecord.swift             # Execution output model
│   ├── Views/
│   │   ├── CreateEditActionState.swift       # Action state CRUD (8/15/23)
│   │   ├── OutputListView.swift              # Output display (8/19/23)
│   │   ├── ExecutionDetailedView.swift       # Execution details
│   │   ├── ExecutioningInputView.swift       # Input during execution
│   │   └── ...                               # ~11 view files total
│   ├── Data/
│   │   └── ActionStateDataController.swift   # Core Data stack (singleton)
│   └── ActionStateCoreData.xcdatamodeld/     # Core Data schema
├── WellTrackTests/
│   └── ModelTests.swift                      # Model validation tests
├── WellTrack.xctestplan                      # Xcode test plan
└── WellTrack.xcodeproj/
```

## What I Learned

That reduction is a feature, not a compromise. The four-entity model captures more useful structure than the earlier branches with their larger entity counts, because it asks the right four questions. Also: adding tests early makes refactoring possible later. The test plan in this branch is small, but it represents a change in mindset from "make it work" to "make it verifiable."

---

← [Prev: #11 Action State Execution](../11-action-state-execution/) | [Collection Home](../README.md) | [Next: #13 Trackwell](../13-trackwell/) →
