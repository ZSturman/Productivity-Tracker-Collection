# Hand Gesture Tracker

> MediaPipe hand tracking turned into a gesture-controlled drawing canvas.

| Detail | Value |
|--------|-------|
| **Date** | ~2023–2024 |
| **Status** | Archived Prototype |
| **Stack** | Python, MediaPipe 0.10.14, OpenCV 4.9, Pygame, PyAutoGUI |

---

## The Story

This branch asks a question that sounds odd for a productivity project: what if your hands could be part of the data model?

The broader arc of this collection keeps pushing toward measuring more of what I actually do — not just which app is open, but what my body is doing while it's open. This experiment was a proof of concept for that idea. Using MediaPipe's hand landmark detection (21 keypoints per hand) and a webcam, it turns physical gestures into digital actions: pinch your index finger and thumb together to draw on a Pygame canvas, or trigger a screenshot capture to your desktop.

It's not a finished product. It's a test of whether physical gestures can become part of the interaction model — and by extension, part of the data model. That's consistent with the broader goal of measuring how I think and move, not only what buttons I click. The rainbow color cycling and keyboard shortcuts for color changes are delightful touches that suggest this was also just fun to build.

See also: [overview.md](overview.md) for the original project description.

## What It Does

- Real-time hand detection via webcam (up to 1 hand, 0.9 confidence minimum)
- **Pinch-to-draw**: index finger + thumb proximity under 20 pixels triggers drawing
- Rainbow color cycling mode for dynamic stroke colors
- Keyboard controls: Q (quit), C (clear canvas), R/B/Y/G/O (set color), L (rainbow mode)
- 1000×1000 Pygame canvas window
- Screenshot capture via PyAutoGUI on trigger gesture

## What's Inside

```
08-hand-gesture-tracker/
├── hand_painter.py      # Main application — hand detection + Pygame drawing canvas
├── overview.md          # Original project description
└── requirements.txt     # Dependencies (mediapipe, pygame, opencv-contrib-python, pyautogui)
```

## What I Learned

That physical input doesn't have to be complicated to be meaningful. The pinch gesture uses just three landmark points (thumb tip, index tip, middle finger) and a distance threshold, but it creates a surprisingly natural interaction. This experiment planted the seed for thinking about biometric signals as first-class data — an idea that the eye tracking project explores from a different angle.

---

← [Prev: #07 macOS Activity Tracker](../07-macos-activity-tracker/) | [Collection Home](../README.md) | [Next: #09 Eye Tracking ML](../09-eye-tracking-ml/) →
