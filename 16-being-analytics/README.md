# Being Analytics

> The analytics-focused direction — service layer, dashboards, and the richest input type system.

| Detail | Value |
|--------|-------|
| **Date** | September 1–15, 2023 |
| **Status** | Archived Prototype |
| **Stack** | Swift, SwiftUI, Core Data, Xcode |

---

## The Story

This is the last and most analytics-focused branch in the Swift line, and it marks a shift in ambition. The previous iterations were about tracking — defining action states, recording executions, managing inputs and triggers. BeingAnalytics adds a layer on top: analysis and visualization.

The `DataService.swift` introduces a proper service layer between the views and Core Data, handling fetches, saves, and the conversion of temporary struct-based models (`TempActionState`, `TempExecution`, `TempInput`, `TempInputExecution`, `TempTrigger`) into persistent Core Data entities. This two-layer pattern — temporary models for UI manipulation, Core Data entities for persistence — is the most sophisticated data architecture in the entire Swift collection.

The input types reach their widest range here: text, number, datetime, location, and calculation inputs, plus global and local variable access. The view layer has 20+ files including specialized input row variants for every type (SetNumber, SetLocalVariable, GetGlobalVariable, Calculate, DateTime, AskForText, AskForNumber, GetLocation, SetText). And then there's the dashboard — a placeholder for charts and analytics visualizations, dated September 15, that points toward the future direction this whole project was heading.

The file `InputExecutionTests.swift` (at the project root) also marks the most testing-conscious version, validating the execution pipeline with structured tests.

## What It Does

- **DataService** layer abstracting Core Data operations
- **Temporary model layer**: TempActionState, TempExecution, TempInput, TempInputExecution, TempTrigger
- **Struct → Core Data conversion** for staged data before persistence
- **10 input row types**: SetNumber, SetLocalVariable, GetGlobalVariable, Calculate, DateTime, AskForText, AskForNumber, GetLocation, SetText, SetLocation
- **Global and local variable system** for inter-input calculations
- **Action vs State categorization**
- **Dashboard view** with placeholder charts (9/15/23)
- **Trigger types** with locations and datetime support
- **Execution filtering and search**
- **Unit tests** for input execution pipeline

## What's Inside

```
16-being-analytics/
├── InputExecutionTests.swift                # Test file for execution pipeline (at project root)
├── BeingAnalytics/
│   ├── BeingAnalyticsApp.swift              # App entry point (9/1/23)
│   ├── ContentView.swift                    # NavigationStack home view
│   ├── DataService.swift                    # Service layer for Core Data
│   ├── Models/
│   │   ├── TempActionState.swift            # Temporary action state struct
│   │   ├── TempExecution.swift              # Temporary execution struct
│   │   ├── TempInput.swift                  # Temporary input with calculations
│   │   ├── TempInputExecution.swift         # Temporary input execution
│   │   └── TempTrigger.swift                # Temporary trigger types
│   ├── Views/                               # 20+ view files
│   │   ├── DashboardView.swift              # Analytics dashboard (9/15/23)
│   │   ├── InputRows/                       # Specialized input row views
│   │   ├── Detail/                          # Detail views
│   │   ├── List/                            # List views
│   │   └── Edit/                            # Edit views
│   ├── ViewModels/                          # View models
│   └── BeingAnalyticsCoreData.xcdatamodeld/ # Core Data schema
└── BeingAnalytics.xcodeproj/
```

## What I Learned

That the jump from tracking to analytics requires an architectural jump too. A service layer, temporary models, and a clean separation between UI state and persisted state aren't luxuries — they're prerequisites for building anything analytical on top of the data. The dashboard was just a placeholder, but the infrastructure beneath it was the most solid foundation in the entire Swift line. If any of these branches were to continue, this is the one with the best bones.

---

← [Prev: #15 TrackingWellness](../15-trackingwellness/) | [Collection Home](../README.md) | [Next: #17 Mental States Research](../17-mental-states-research/) →
