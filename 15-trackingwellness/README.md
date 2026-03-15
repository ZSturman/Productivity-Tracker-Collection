# TrackingWellness

> The lightest possible version — a minimal singleton pattern to test small.

| Detail | Value |
|--------|-------|
| **Date** | August 30, 2023 |
| **Status** | Archived Prototype |
| **Stack** | Swift, SwiftUI, Xcode |

---

## The Story

On the same day TrackingWell was reaching its most production-ready state, this parallel branch went in the opposite direction: strip everything down to almost nothing and see what still works.

TrackingWellness has just one model (`ActionStateModel`), two view models (`SharedVM` as a singleton and `CreateEditVM`), and five views. No Core Data. No triggers. No execution records. No input types. Just the bare minimum of creating and viewing action states.

This reads like a controlled experiment. When you've been building increasingly complex iterations, sometimes you need to go back to the simplest possible version to test whether the core idea still makes sense without all the infrastructure. The `SharedVM` singleton pattern is interesting too — it's a different state management approach than anything in the other branches, testing whether a shared mutable state object could replace the view model multiplication happening elsewhere.

The timing matters: this was built on the same day as TrackingWell (#14), which means I was running two architectural experiments simultaneously — one maximally clean, one minimally complex.

## What It Does

- Basic ActionState management (create, view, edit)
- SharedVM singleton for centralized state management
- Row-based list display
- Detail views for individual action states
- No persistence layer — in-memory only

## What's Inside

```
15-trackingwellness/
├── TrackingWellness/
│   ├── TrackingWellnessApp.swift    # App entry point
│   ├── ContentView.swift            # Home view
│   ├── Models/
│   │   └── ActionStateModel.swift   # Single model definition
│   ├── ViewModels/
│   │   ├── SharedVM.swift           # Singleton shared state
│   │   └── CreateEditVM.swift       # Create/edit logic
│   └── Views/
│       ├── ListView.swift           # Action state list
│       ├── CreateEditView.swift     # Create/edit form
│       ├── ActionStateDetailView.swift  # Detail view
│       └── ActionStateRowView.swift     # Row component
└── TrackingWellness.xcodeproj/
```

## What I Learned

That there's value in building the minimum version even when you already have a maximum version. This branch confirmed which pieces of the larger architecture are truly essential (the action state concept itself) and which are optimizations (Core Data, input types, triggers). It also tested whether a singleton shared state could work — and the answer seemed to be "yes, but only at this scale."

---

← [Prev: #14 TrackingWell](../14-trackingwell/) | [Collection Home](../README.md) | [Next: #16 Being Analytics](../16-being-analytics/) →
