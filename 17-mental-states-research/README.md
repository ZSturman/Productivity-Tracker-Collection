# Mental States Research

> A psychology framework for understanding focus, well-being, and the conditions that make productive days possible.

| Detail | Value |
|--------|-------|
| **Date** | ~2023 |
| **Status** | Research Notes |
| **Stack** | Markdown, handwritten notes |

---

## The Story

Somewhere between building apps and writing schemas, I needed to think about what I was actually trying to measure. This folder is that thinking.

The core document (`MentalState.md`) bridges psychology and engineering. It starts from the question of what "feeling good" actually means and breaks it down into five components: positive emotions, engagement (flow), relationships, meaning, and accomplishment. Then it lists what seems to affect focus — interest in the subject, knowledge and confidence about it, novelty, pressure, the medium (active vs. passive), and the time between sessions.

That list might look simple, but it's the conceptual kernel of the entire project. Every tracker, every input type, every categorization system in the later branches is trying to capture some version of these variables. If the code is the mechanism, this document is the theory of what the mechanism is for.

The `handwrittenNotes/` folder contains photographs of handwritten notes — the kind of thinking that happens on paper before it becomes data models and view controllers. They're included because they're part of the story, not because they're polished.

See also: [overview.md](overview.md) for the original project summary, and [MentalState.md](MentalState.md) for the full framework.

## What It Does

This isn't code — it's the theoretical backbone that the code projects are built on.

- Framework for "Feeling Good" based on positive psychology components
- Analysis of focus control factors and what influences them
- Bridge between psychological research and system design
- Tags: Psychology, Science, Happiness, QualityOfLife, Algorithm, Math, Computers

## What's Inside

```
17-mental-states-research/
├── MentalState.md           # Core framework: well-being components + focus factors
├── overview.md              # Brief project summary
└── handwrittenNotes/        # Scanned handwritten notes (photographs)
    ├── Pasted Graphic 25.jpg
    ├── Pasted Graphic 26.jpg
    ├── Pasted Graphic 27.jpg
    └── Pasted Graphic 28.jpg
```

## What I Learned

That you can't build a measurement system without a theory of what you're measuring. Productivity isn't just output — it's downstream from emotional state, interest, confidence, novelty, and recovery time. Writing this framework down made the later architectural decisions (like adding triggers and inputs to action states) feel less arbitrary and more grounded. Theory first, schema second.

---

← [Prev: #16 Being Analytics](../16-being-analytics/) | [Collection Home](../README.md) | [Next: #18 Holistic Tracker Spec](../18-holistic-tracker-spec/) →
