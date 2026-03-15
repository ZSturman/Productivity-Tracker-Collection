# Action States

> First SwiftUI/Core Data branch — where actions, states, topics, and tags became the vocabulary.

| Detail | Value |
|--------|-------|
| **Date** | July 22–27, 2023 |
| **Status** | Archived Prototype |
| **Stack** | Swift, SwiftUI, Core Data, Xcode |

---

## The Story

The Swift branch starts here, and it has a different flavor than the Python work. From day one it's more structured around entities, lists, and forms. Where the Python prototypes were reaching for project management, this branch reaches for something more personal: a life-state organizer.

The core concept — the "action state" — arrives already connected to categorization. I wasn't just tracking events. I was trying to connect actions and states to topics (from a taxonomy of 45 human motivations exported as a plist), tags for flexible labeling, and manually entered inputs for custom data. There's list support through `ListEntity` and `ListItemEntity`, a `TopicPlistGenerator` that converts the JSON taxonomy into a native resource, and views for browsing, creating, and editing each entity type.

Compared with the desktop branches, ActionStates feels less like a general project manager and more like a tool for modeling what's going on in my life. The categories are not folders and tasks. They are states, topics, and inputs. That's a real conceptual shift — the same shift that defines every Swift iteration after this one.

## What It Does

- Core Data entities: `ActionStateEntity`, `TopicEntity`, `TagEntity`, `ManualInputEntity`, `ListEntity`, `ListItemEntity`
- Topic browsing from a 45-item taxonomy of human needs and motivations
- Tag management for flexible categorization
- Manual input forms for custom data entry
- List management with items
- MVVM architecture with ViewModels directory
- Plist generation from JSON topic data

## What's Inside

```
10-action-states/
├── ActionStateEntity+CoreDataClass.swift   # Core Data model extension (at project root)
├── ActionStates/                           # Main app source
│   ├── ActionStatesApp.swift               # App entry point (7/22/23)
│   ├── ContentView.swift                   # List-based home view (7/22/23)
│   ├── TopicPlistGenerator.swift           # Topic taxonomy → plist converter
│   ├── topics.plist                        # Serialized topic data
│   ├── Models/                             # Core Data entity definitions
│   ├── Views/                              # SwiftUI views
│   │   ├── Topics/                         # Topic browsing
│   │   ├── Lists/                          # List management
│   │   ├── ActionStates/                   # Action state CRUD
│   │   └── ManualInputs/                   # Manual input forms
│   ├── ViewModels/                         # MVVM view models
│   └── ActionStatesData.xcdatamodeld/      # Core Data schema
└── ActionStates.xcodeproj/                 # Xcode project configuration
```

## What I Learned

That the vocabulary you choose for your data model shapes the questions you can ask. "Folder → Project → Task" is a project management vocabulary. "Action State → Topic → Tag → Input" is a life-modeling vocabulary. This branch was the first time I found words that fit the actual problem: understanding the conditions and context around what I do, not just tracking what I do.

---

← [Prev: #09 Eye Tracking ML](../09-eye-tracking-ml/) | [Collection Home](../README.md) | [Next: #11 Action State Execution](../11-action-state-execution/) →
