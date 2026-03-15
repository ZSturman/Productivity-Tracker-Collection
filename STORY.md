# Productivity Tracker Collection

## An Archive of Trying to Measure My Own Life Well Enough to Improve It

This folder is not one project in the normal sense. It is a record of a long attempt to understand what actually affects my energy, focus, mood, output, and ability to think clearly, and then build tools around that instead of relying on memory, vague impressions, or whatever happened to feel true in the moment.

Some of this work was very practical. Some of it was exploratory. Some of it was me building versions of the same idea over and over because I still had not found the shape that felt right. A lot of it came from the same basic question: if I could capture enough variables about my day, my behavior, my environment, my work, and my internal state, could I get closer to understanding what helps, what hurts, and what needs to change for me to have a more productive and stable life.

That question stayed constant even as the tools changed. At different points that meant iPhone shortcuts writing JSON, desktop apps for organizing projects, Swift apps for action states and executions, OCR pipelines that captured text from my screen, experiments with hand and eye tracking, and later broader specifications for a system that could tie together wellness, cognition, behavior, and performance instead of treating them as separate topics.

What follows is an archival walkthrough of that work. I am treating it as a chronology where the evidence is clear and as an evolving set of parallel branches where it is not. Some folders are clean steps forward. Others are experiments that overlap in time. That matters, because this archive makes more sense as a record of thinking than as a neat product history.

## How I Am Reading This Archive

The dating in this write-up comes from a mix of explicit and inferred sources.

- Explicit dates come from dated folder names, markdown frontmatter, and file headers such as `Created by Zachary Sturman on ...`.
- Approximate order comes from feature maturity, naming, and how later branches simplify or specialize earlier ones.
- Some branches, especially the Swift apps from mid to late 2023, are better understood as parallel experiments inside the same lineage rather than a single strict version sequence.
- The large private JSON history that motivated a lot of this work is part of the story, but it is not fully represented in this workspace, so I am describing that portion at a high level rather than pretending the repository contains the whole dataset.

## Chronology at a Glance

| Approx. Date | Project / Phase | What It Represents |
| --- | --- | --- |
| 2023-05-25 | `productivity_manager/productivity_app_05252023` | earliest minimal PyQt prototype |
| 2023-05-27 | `productivity_manager/productivity_app_05272023` | folder, project, and task management with SQLAlchemy |
| 2023-05-28 | `productivity_manager/prod_app05282023` | most ambitious early desktop branch with richer schema and multiple layouts |
| 2023-05-31 | `productivity_manager/productivity_app_05312023` | additional experiment, lighter and less complete |
| 2023-07-22 to 2023-07-27 | `ActionStates` | first SwiftUI/Core Data action-state branch with topics, tags, lists, and manual inputs |
| 2023-07-27 to 2023-08-03 | `ActionStateExecution` | adds execution tracking and field/input types |
| 2023-08-15 to 2023-08-23 | `WellTrack` | simplified Core Data app centered on action states, inputs, triggers, and executions |
| 2023-08-25 to 2023-08-30 | `Trackwell` | in-memory refactor with parallel `NewViews` and `NewVMs` redesign |
| 2023-08-30 | `TrackingWell` | most production-ready Core Data Swift branch with cleaner data layer and search config |
| 2023-08-30 | `TrackingWellness` | lightweight proof-of-concept branch |
| 2023-09-01 to 2023-09-15 | `BeingAnalytics` | analytics-oriented Swift branch with service layer and dashboard direction |
| 2023-10-12 | `Holistic Productivity and Wellness Tracker` | full conceptual specification for a broader system |
| 2024-05-07 | `Sensory Input` | neuroscience and cognitive-energy research notes |
| 2024-09-16 | `InsightWell` | later product/spec direction for integrated wellness and productivity analytics |

## Before the Code Took Shape, the Goal Was Already Clear

The goal behind almost all of this work was not simply task management. It was to model the conditions around productivity well enough that I could stop treating output as a personality trait and start treating it as something influenced by inputs, context, friction, health, attention, stress, and behavior.

The foundational taxonomy for that broader view is in `topics.json`. It is not a small list. It covers physical well-being, safety, autonomy, competence, purpose, connection, esteem, growth, creativity, contribution, curiosity, novelty, resilience, harmony, simplicity, gratitude, empowerment, and more. That file matters because it shows I was not trying to track a narrow productivity score. I was trying to map productivity into a wider model of human needs and motivations.

The smaller `mentalStates/MentalState.md` file captures the same idea in a more direct way. It ties feeling good to positive emotions, engagement, relationships, meaning, and accomplishment, then lists what seems to affect focus: interest, knowledge, novelty, pressure, medium, and the time between sessions. Even in its short form, that file shows the project was already moving toward a system where productivity is downstream from internal and external conditions, not independent from them.

## Phase 1: Early Desktop Prototypes in Python, May 2023

The earliest dated sequence in this archive is in `productivity_manager`, and it shows a very recognizable pattern: build something small, realize it is too small, add structure quickly, then try to widen the system before the architecture is settled.

### 2023-05-25: `productivity_app_05252023`

This is the smallest clear starting point. The `main.py` file launches a `ButtonHolder` window. That alone is useful as evidence. It says the first step here was not a big platform. It was getting a UI running and making the loop tangible.

This version looks like a proof that a desktop interface existed at all, not a durable product. It feels like the point where the work moves from idea to application.

### 2023-05-27: `productivity_app_05272023`

Two days later the app is already more concrete. The main window is a `FolderApp` with list widgets and controls for folders, projects, and tasks, backed by SQLAlchemy models through `Session`, `Folder`, `Project`, and `Task`.

The difference between 2023-05-25 and 2023-05-27 is important. The first version proves the UI loop. The second version moves immediately into persistence and object structure. This is the point where the project stops being a widget experiment and starts acting like an organizer.

This version includes:

- folder creation and deletion
- project creation and completion
- task creation and completion
- list refresh behavior
- database-backed relationships instead of hardcoded state

What it does not yet include is the broader life-modeling ambition that shows up later. It is still recognizably a productivity app in the conventional sense.

### 2023-05-28: `prod_app05282023`

This is the strongest branch in the early desktop line, and it is where the ambition becomes obvious.

The UI in `main.py` is no longer a simple form. It loads a `.ui` file and organizes the application around multiple major sections: home, dashboard, productivity, data collection, and settings. Inside productivity it also branches into kanban, gantt, calendar, table, and directory views. Even if some of those layouts were not fully finished, the intent is clear. I was already trying to build a system that did more than list tasks.

The database schema in `application/models/models.py` makes the same point even more clearly. By this point the data model includes:

- `Folder`
- `Project`
- `Task`
- `Deliverable`
- `Milestone`
- `Note`
- `Attachment`
- `SubTask`
- `ToDoList`

There are also fields for creation and modification dates, status, priority, due dates, estimated completion, dependencies, desired outcome, actual outcome, acceptance criteria, and quality criteria. That is not a casual schema. It shows I was trying to capture not just whether something existed, but what kind of work it was, how it related to other work, and how expectations compared to reality.

This branch is the first point in the archive where I can see the system stretching toward project management, planning, evidence collection, and analysis all at once.

### 2023-05-31: `productivity_app_05312023`

This branch looks more experimental and less complete. It is useful in the chronology because it suggests the line did not stabilize immediately after the richer May 28 build. I was still testing directions, and not every newer date means a more finished result.

That becomes a theme in the archive as a whole. Progress is real, but it is not linear.

### What Changed Across the Early Python Versions

The early Python lineage moves through three clear steps.

| Version | What Changed |
| --- | --- |
| `05252023` | minimal UI proof |
| `05272023` | database-backed folder/project/task structure |
| `05282023` | broader productivity platform with richer schema and multiple views |
| `05312023` | additional experimentation rather than a clean replacement |

The lesson from this phase is that I moved quickly toward structure. I did not stay in the toy stage for long. As soon as the interface existed, I wanted relationships, metadata, time, and categorization.

## Phase 2: Side Branches Around Organization, Visualization, and Reference Material

The `productivity_organization` folder reads like a companion laboratory for interface and structure experiments rather than a single application.

It includes:

- `simple_streamlit.py`, a basic folder app in Streamlit
- `main_page_design_stuff.py`, which points toward dashboard and gantt visualization work
- `project_gantt_chart_v1` and `project_gantt_chart_v2`
- `project_schema_v0`
- `gantt_and_proj_creation_v1`
- `app`, `old_py_files`, `refs`, and local data files like `data.json` and `list.txt`

This branch matters because it shows the problem widening again. The work is no longer only about creating and completing tasks. It is about how to represent projects, how to see them over time, how to browse structure, and how to test different interface technologies for the same underlying need.

I read this folder as a transitional layer between the first desktop organizer ideas and the later analytics-heavy thinking. It is less polished than the better defined branches, but it shows a real move toward visualization and schema design.

## Phase 3: Tracking the Computer Itself Instead of Only Asking Me to Remember

One of the most important shifts in this archive is the move from self-reported structure toward passive or semi-passive collection.

That shift is clearest in `productivity_tracker`.

### `productivity_tracker/tracker_main.py`

This script watches actual device behavior in a way that feels much closer to the original goal than a normal task app does.

It:

- gets the device name from the machine hostname
- uses AppleScript to inspect the frontmost macOS application
- captures the active app name, window title, and document path
- special-cases Google Chrome to grab active tab title and URL
- normalizes Electron into Visual Studio Code for cleaner logs
- watches keyboard and mouse activity to determine idleness
- writes events into a dated CSV file in iCloud storage
- periodically calls `run_txt_from_screen()` when the machine is active

The design decision here is important. Instead of asking what I think I worked on, it records what was actually on screen and whether I was active. That is a different level of evidence.

### `productivity_tracker/txt_from_screen.py`

This part goes further. It captures a multi-monitor screenshot, runs OCR with Tesseract, and then runs NLP with spaCy over the extracted text.

It saves:

- raw extracted text
- nouns
- named entities
- POS-tagged noun lists
- dependency pairs for subjects and objects
- extracted verbs

That tells me I was not only interested in where my attention was, but also what the content of that attention might reveal. In other words, the question had shifted from, "Was I active?" to, "What was I looking at, reading, or doing, and how can that be summarized automatically?"

The supporting files in this folder reinforce that interpretation:

- `txt_from_screen_labels_google.py`
- `txt_from_screen_organizer.py`
- `txt_from_screen_organizer2.py`
- `logs`
- `previous_versions`
- `seperated modules`

This is one of the strongest examples in the archive of the work moving closer to real behavioral telemetry.

### Why This Phase Matters

This part of the archive gets much closer to the original vision than a conventional productivity app. It captures work context automatically, stores it over time, and tries to turn raw text on screen into analyzable data.

If I had to point to a place where the project stopped being a planner and started becoming a personal analytics system, this is one of the clearest points.

## Phase 4: Behavioral Input Experiments Beyond Keyboard and Screen

The archive also includes experiments that try to read physical signals instead of only digital ones.

### `Hand Tracker/hand_painter.py`

This branch uses MediaPipe Hands, OpenCV, Pygame, and PyAutoGUI to turn hand gestures into actions.

The behavior is simple, but the direction matters:

- one gesture draws on a Pygame canvas
- another gesture captures screenshots to the desktop
- keyboard shortcuts change drawing color, clear the screen, or quit

This does not read like a finalized app. It reads like a proof that physical gestures can become part of the interaction model and part of the data model. That is consistent with the broader project goal of measuring how I think and move, not only what buttons I click.

### `Eye-Tracking - Machine Learning - Python/ml_eyes/detect_eyes.py`

This branch uses `dlib` facial landmarks and OpenCV to classify whether eyes are pointed toward the screen or away from it.

It does three especially relevant things:

- records webcam video to `webcam_output.avi`
- records the screen to `screen_recording.avi`
- appends timestamped `at` and `away` events into `timestamps.csv`

The script computes eye aspect ratios from landmark points, uses a threshold to decide whether attention is on screen, and creates synchronized artifacts that could later be reviewed or correlated.

This is not a finished attention model. It is rough, and the thresholding is explicitly something to tune. But that does not make it unimportant. It shows the project expanding beyond software events into bodily signals, which fits exactly with the stated purpose of measuring variables that might help explain good and bad days.

## Phase 5: The First SwiftUI/Core Data Action-State Line, July 2023

The Swift branch starts with `ActionStates`, and it has a different flavor than the earliest Python work. It is more structured around entities, lists, and forms from the beginning.

### `ActionStates` (2023-07-22 onward)

The earliest files in this branch are dated 2023-07-22. This branch includes:

- `ActionStateEntity`
- `TopicEntity`
- `TagEntity`
- `ManualInputEntity`
- list support through `ListEntity` and `ListItemEntity`
- views for topics, lists, action states, and manual inputs
- a `TopicPlistGenerator`
- `topics.json` as a project resource

What stands out here is that the action-state idea arrives already connected to categorization. I was not just tracking events. I was already trying to connect states and actions to topics, tags, and manually entered inputs.

This is the first clear Swift version of the idea that later branches refine repeatedly.

### What This Version Was Trying to Solve

Compared with the earlier desktop branches, `ActionStates` feels less like a general project manager and more like a life-state organizer. It is a more personal model. The categories are not just folders and tasks. They are states, topics, and inputs.

That is a real conceptual shift.

## Phase 6: `ActionStateExecution`, July to August 2023

`ActionStateExecution` begins on 2023-07-27 and builds directly on the previous branch, but with a notable addition: execution becomes a first-class concept.

Files in this branch are dated from late July into early August 2023, and the app includes:

- execution views and execution detail views
- field and input-type views such as text, number, list, count, and boolean input fields
- user settings
- list support and topic/tag support carried forward
- view models focused on action states and executions

The important difference is that this branch does not just define a state or an action. It starts modeling what happens when something is actually executed.

That sounds obvious now, but it is a significant change. A state system without execution tracking can describe possibilities. An execution-aware system begins to describe reality.

## Phase 7: The Swift Branch Splits into Multiple Parallel Experiments, August to September 2023

From mid August onward the Swift work becomes denser and less linear. There are several related apps in a short period, and they do not read like simple renames. They read like parallel attempts to find the right balance between data persistence, app complexity, and analysis.

### `WellTrack` (2023-08-15 to 2023-08-23)

`WellTrack` simplifies the model around a tighter core:

- `ActionState`
- `Input`
- `Trigger`
- `ExecutionRecord`

The dated files show action-state views starting on 2023-08-15, `Input` added on 2023-08-17, and triggers and execution-related views added around 2023-08-19 through 2023-08-23.

This branch feels like a reduction after the earlier entity-heavy branches. Instead of topics, tags, fields, and lists all competing for space, the structure centers on what an action state is, what triggers it, what input it needs, and what execution it produces.

That is a better fit for the actual tracking problem.

### `Trackwell` (2023-08-25 to 2023-08-30)

`Trackwell` is one of the clearest signs that I was actively rethinking the architecture, not just adding features.

It includes both the original `ViewModels` and a later `NewVMs` folder, along with `Views` and `NewViews`. The dated file headers show the app beginning on 2023-08-25, then getting a redesign burst on 2023-08-30.

The model layer here is in-memory rather than Core Data focused, with files like:

- `ActionStateModel`
- `InputModel`
- `TriggerModel`
- `ExecutionModel`

What makes this branch important is not only the feature set. It is the evidence of an architectural reset in progress. The presence of `NewViews` and `NewVMs` suggests I was trying to keep momentum while also reworking the app from inside the same branch.

### `TrackingWell` (2023-08-30)

If one Swift branch looks most like the point where the architecture was settling, this is it.

The `DataController.swift` file is small but telling. It sets up a `NSPersistentContainer`, manages preview and test behavior, merges background changes, exposes helper methods like `exists`, `delete`, and `saveChanges`, and includes factory methods for `ActionState`, `Trigger`, `Input`, `Execution`, and `InputExecution`.

This branch also contains `SearchConfig` and `Sort` in `SortAndFilter.swift`, which shows search and filtering being treated as explicit app behavior rather than an afterthought.

Compared with `Trackwell`, this version looks less like a redesign in motion and more like a branch aimed at becoming stable.

### `TrackingWellness` (2023-08-30)

This branch is much lighter. It appears to be a compact proof of concept built around a `SharedVM` singleton and a smaller set of views.

I do not read it as the main path. I read it as a short-lived alternate simplification, likely used to test a smaller architecture without carrying all the complexity of the other branches.

### `BeingAnalytics` (2023-09-01 onward)

`BeingAnalytics` is where the Swift line becomes more explicitly analytical.

The `DataService.swift` file is one of the strongest signals in the whole archive. It introduces a service layer that:

- fetches action states and executions
- saves new action states and executions
- converts temporary execution models into Core Data entities
- maps specialized input execution types such as datetime, string, number, and location
- pulls prompt metadata from input definitions when constructing execution records

The model names are telling too. This branch uses `TempActionState`, `TempExecution`, `TempInput`, `TempInputExecution`, and `TempTrigger`, which suggests a system where more transient or staged data is being translated into durable storage.

The dashboard file dated 2023-09-15 is still mostly placeholder charts, but the intent is obvious: the app is not only about recording action states anymore. It is trying to visualize them.

There are also signs of broader input ambition in the file inventory for this app, including input rows for text, number, datetime, location, calculation, and global and local variable access. Even where the visuals are still placeholders, the underlying model is moving toward a much more flexible execution system.

### How the Swift Versions Differ

This is the simplest way I would describe the Swift lineage.

| Branch | Main Difference |
| --- | --- |
| `ActionStates` | introduces action states tied to topics, tags, lists, and manual inputs |
| `ActionStateExecution` | adds executions and richer field/input modeling |
| `WellTrack` | simplifies around action state, input, trigger, and execution |
| `Trackwell` | in-memory refactor with active UI and VM redesign |
| `TrackingWell` | stronger Core Data foundation and cleaner app infrastructure |
| `TrackingWellness` | lightweight proof-of-concept variant |
| `BeingAnalytics` | pushes toward service layer, analytics, and dashboard thinking |

I do not think it is accurate to call one of these a clean winner and discard the others. They each represent a different answer to the same problem.

Still, if I had to summarize the center of gravity:

- `TrackingWell` looks the most production-ready in architectural terms.
- `BeingAnalytics` looks the most ambitious in analytical direction.
- `Trackwell` shows the strongest evidence of active internal redesign.

## Phase 8: The Conceptual Scope Expands, October 2023

The `Holistic Productivity and Wellness Tracker` folder, dated 2023-10-12, is where the project becomes explicit about its full intended breadth.

This is no longer just an app archive. It is a requirements and design archive for a broader system.

The main README describes a platform for:

- cognitive abilities
- emotional and psychological well-being
- physical aspects
- social interactions
- personal development
- productivity measurement
- task management

The `Project_Requirements.md` file is especially revealing because of how it sequences the work. It starts with getting the user join date, generating a date range, recording dates into a daily tracker, then defining categories, topics, subtopics, subjects, priorities, to-do items, goals, projects, and tasks.

That sequence shows that by late 2023 I was thinking in terms of a unified life record, not a task list. Daily context, topic structure, long-term goals, and tracked work were supposed to live in one model.

This folder also includes:

- `Cognitive_Abilities.md`
- `Emotional_Psychological_Wellbeing.md`
- `Physical_Aspects.md`
- `Social_Interactions.md`
- `Personal_Development.md`
- `Productivity_Measurement.md`
- `Productivity_Rating_Scale.md`
- `Task_App.md`
- `Templates_for_Tracking_Productivity.md`
- `Uncreated_Notes.md`
- `TO_COMPARE_THEN_DELETE`

The presence of `TO_COMPARE_THEN_DELETE` tells its own story. This archive was not only about generating ideas. It was also about trying to reconcile overlapping ones, even if the cleanup was not always finished.

## Phase 9: Brain, Attention, and Energy Become Explicit Research Topics, 2024

The `Sensory Input` folder marks another change. By May 2024 the work is not only about software structure anymore. It is about a working theory of attention and cognitive cost.

### `Brain Energy Distribution and Control.md` (2024-05-07)

This note breaks behavior into cortex, limbic system, and lizard brain, then discusses fatigue, focus, retention, fear, stress, health, sleep, and basic survival responses.

The core idea is simple and important: different kinds of mental work feel different because different systems may be carrying different kinds of load. That is not a complete neuroscience model, but it is enough to explain why the project kept reaching beyond normal productivity software.

### `SensoryInput.canvas`

This is one of the best media artifacts in the repository because it is directly readable. It lays out a cognitive flow diagram with the following nodes:

- Extreme / frightening / dangerous input
- Sensory input
- Memory
- Analysis
- Prediction
- Action
- Expectation
- Body
- Output
- Memory again as downstream storage

The edges show a pipeline where sensory input and prior memory feed analysis, analysis leads to action, action branches toward body and expectation, output flows forward, and output is stored back into memory.

That matters because it shows the software experiments were running alongside an attempt to model the actual process behind attention and behavior. I was not only building trackers. I was trying to sketch the machinery those trackers were supposed to illuminate.

## Phase 10: The Later Product Vision Becomes `InsightWell`, September 2024

`InsightWell` is dated 2024-09-16, and it reads like a later, more outward-facing articulation of the same long-running goal.

The product overview says the objective is to provide actionable insights from personal data across well-being and productivity. The core features expand the scope even further:

- mood tracking
- physical health metrics
- mental well-being indicators
- cognitive performance tests
- financial health tracking
- relationship quality assessment
- environmental data capture
- digital habits monitoring

The roadmap then adds phased development around visualizations, analytics, import/export, social features, and premium or advanced capabilities. The future enhancements file explicitly mentions wearables, health apps, AI personalization, and voice assistants.

This part of the archive is more polished as a spec than as an implementation. Some of the docs still use placeholders like `Your Name`, and some links point to paths that do not exist in this workspace exactly as written. But that does not reduce its value. It shows the later framing of the whole effort: not only track data, but transform it into useful interpretation.

In other words, the center of gravity shifts from collection to insight.

## Other Supporting Folders and Why They Matter

There are several other folders that are lighter individually but important in aggregate because they show how wide the exploration became.

### `Action States`

This appears to be a separate artifact folder from the main `ActionStates` Swift project and includes at least one image, `IMG_9164.jpeg`. I cannot read the binary content directly here, but its presence suggests an early visual or device-level artifact associated with that line of work.

### `BeingAnalytics/InputExecutionTests.swift`

The presence of tests in this branch matters. Even when the app was still exploratory, there was a push to validate the behavior of the input execution pipeline.

### `refs from ipad`, `refs`, `old_py_files`, `previous_versions`, `logs`

These folders point to another important truth about the project: it was never only about the current version. It was also about keeping traces of previous attempts, reference material, and supporting evidence. That archival habit is part of the project identity.

## What the Whole Collection Was Really Doing

Looking across all of these branches, I do not think the project was ever just trying to answer, "What tasks do I have?" It was trying to answer a much harder set of questions.

- What was I doing?
- What was I looking at?
- What did I intend to do?
- What actually got done?
- What state was I in when it happened?
- What inputs, triggers, environment, or conditions might explain the result?
- How can that become visible enough to change?

That is why the archive includes both simple task structures and models of brain energy. It is why there are action-state apps and OCR pipelines in the same workspace. It is why there are hand and eye tracking experiments alongside categories like meaning, autonomy, and belonging.

The project kept expanding because the problem kept refusing to stay small.

## Lessons I Can See in the Archive

There are a few lessons that show up over and over.

### 1. Manual logging alone was never going to be enough

The move from forms and states into OCR, active-window logging, and sensor experiments says this clearly. I wanted data that was more faithful than memory and easier to gather than constant self-report.

### 2. Productivity by itself was too narrow a frame

The topic taxonomy, mental state notes, holistic tracker docs, and InsightWell spec all show the same realization. Sleep, stress, health, relationships, environment, and mood are not side notes. They are part of the explanation.

### 3. The right structure mattered as much as the right features

The repeated Swift rewrites make this obvious. I was not only adding functionality. I was searching for the right architecture for a system that had to connect actions, states, triggers, inputs, and outcomes without collapsing under its own weight.

### 4. Some of the most valuable work was infrastructural, not visible

The best examples are `tracker_main.py`, `txt_from_screen.py`, and the `TrackingWell` data layer. These are not the flashiest parts of the archive, but they are the parts that make later analysis possible.

### 5. The vision consistently outran the implementation

That is not a criticism. It is one of the defining truths of the archive. The later specs always widen the ambition faster than any single branch can fully catch up. That is why the archive contains both promising systems and unfinished comparisons.

## Where I Am Now, in the Context of This Archive

The current context matters.

At this point I use ActivityWatch and WakaTime, and both of those tools overlap with goals that show up all over this repository. They capture work time and computer behavior in ways that reduce manual effort, and in that sense they solve part of the same problem I was trying to solve here.

At the same time, they still do not fully match what I was aiming for. The project in this archive was not only about computer activity. It was about correlating work with sleep, health, attention, environment, internal state, and whatever else seemed to matter. It was also about making sense of the data in a way that reflected my actual life rather than a generic productivity dashboard.

That is why this archive still feels unfinished in a useful way. The core problem is still valid, and a lot of the earlier work now looks more plausible because modern AI can help with the exact part that used to create too much overhead: interpretation.

Thousands of JSON files, audio extracted from videos, window titles, OCR text, timestamps, state models, and execution records are only valuable if something can help synthesize them into patterns without requiring me to become a full-time analyst of my own life. That is where current tools are much stronger than they were when a lot of this code was written.

## Future Direction

If I connect the dots from the earliest desktop prototypes to the latest specs, the future direction looks less like a single app and more like a layered personal analytics system.

At a high level, that system would probably include:

- passive collection where possible
- selective manual input where it adds something unique
- durable storage across time
- event and state models that can be correlated rather than isolated
- AI-assisted summarization and pattern detection
- a clearer bridge between internal state, external behavior, and actual output

I do not think the lesson here is that every folder should be revived exactly as it is. The lesson is that the archive already explored many of the right ingredients. What was missing was a good enough way to unify them without drowning in the volume of raw data.

That is a better problem to have now than it was a few years ago.

## Text Versions of Media and Generated Outputs

This section turns the most relevant non-code artifacts into text descriptions. Where the source is directly readable, I am describing it from the file itself. Where it is a binary artifact, I am describing it from its filename, folder context, and surrounding code, and I am treating that description as contextual rather than definitive.

### 1. `Sensory Input/SensoryInput.canvas`

Text version:

> A visual cognitive-processing diagram. At the top are extreme or dangerous inputs and ordinary sensory input. Sensory input, together with prior memory, feeds analysis. Analysis leads into prediction and action. Action branches toward expectation and the body. Output then follows, and output is stored back into memory. The diagram reads like a feedback system where perception, prior experience, bodily response, and expectation all shape later behavior.

Why it matters:

> This is one of the clearest visual summaries of the broader project logic. It shows that the tracking work was paired with an attempt to model how input becomes action and memory.

### 2. `Eye-Tracking - Machine Learning - Python/ml_eyes/detect_eyes.py`

Text version of the generated video outputs:

> `webcam_output.avi` would be a live webcam recording of my face while the script runs dlib landmark detection and estimates whether my eyes are directed toward the screen.
> `screen_recording.avi` would be a synchronized screen capture recorded alongside the webcam footage so visual attention can be reviewed against what was actually on screen.
> `timestamps.csv` would be a simple event log of `at` and `away` states over time, generated from the eye aspect ratio thresholding.

Why it matters:

> This is a direct attempt to turn attention into data rather than guesswork.

### 3. `Hand Tracker/hand_painter.py`

Text version of the interaction:

> A webcam-driven drawing board where one hand gesture pinches thumb and index finger together to draw and another gesture triggers screenshots. The screen becomes a sandbox for translating movement into visible output and captured artifacts.

Why it matters:

> This is less about drawing than about testing whether motion and gesture can become meaningful inputs.

### 4. `mentalStates/handwrittenNotes/Pasted Graphic 25.jpg` through `Pasted Graphic 28.jpg`

Contextual text version:

> A small set of handwritten note images stored beside the mental-state framework. Based on the surrounding files, these likely capture informal sketches or diagrams around feeling good, focus, engagement, and the conditions that shape mental state. They read as working notes behind the cleaner markdown summaries rather than polished presentation assets.

Limit:

> I cannot inspect the binary image contents directly here, so this description is contextual rather than visual.

### 5. `Action States/IMG_9164.jpeg`

Contextual text version:

> A photo or screenshot artifact associated with the early action-state phase. Because it sits outside the main Swift project and cannot be read directly here, the safest interpretation is that it is a supporting visual from that early iOS exploration rather than a core source of record.

Limit:

> This description is contextual only.

## Final Read on the Collection

What I see in this archive is not a pile of abandoned apps. I see a persistent line of inquiry that kept finding new forms.

Early on, the question looked like project management. Then it started looking like action states. Then it turned into execution tracking. Then it reached toward OCR, NLP, gesture input, eye tracking, brain-energy models, and broader wellness analytics. The exact implementation kept shifting, but the underlying objective stayed recognizable: build a system that can explain, as concretely as possible, why some days work and others do not.

I do not think this archive should be judged by whether one folder became the final app. I think it is better understood as a record of narrowing in on the actual shape of the problem. In that sense, the archive succeeded even where branches remained incomplete, because it kept making the problem more precise.

And where I am now fits the same story. I use better off-the-shelf trackers than I had before, but the deeper goal still points beyond them. The difference now is that AI makes the synthesis side more realistic. The data no longer has to sit there waiting for manual interpretation forever.

That changes the project. It does not erase the earlier work. If anything, it makes the earlier work more relevant, because this repository already contains the models, experiments, categories, and questions that a stronger analytical layer could finally use well.
