# Eye Tracking ML

> Synchronized screen and webcam recording with eye aspect ratio attention classification.

| Detail | Value |
|--------|-------|
| **Date** | ~2023–2024 |
| **Status** | Archived Prototype |
| **Stack** | Python, dlib, OpenCV, NumPy, PIL, PyAutoGUI |

---

## The Story

If the hand tracker asked "can gestures become data?", this project asks the more pointed question: "can I tell whether I'm actually paying attention?"

Using dlib's 68-point facial landmark predictor and OpenCV, this script watches my eyes through the webcam and classifies each frame as "looking at the screen" or "looking away" based on the eye aspect ratio — a simple geometric measurement computed from the six landmark points that define each eye. When the ratio drops below a threshold (0.25), it means the eyes are likely looking away or blinking.

What makes this especially relevant is the synchronized recording. While the webcam watches my face, a screen recorder captures exactly what was on the display. The result: time-stamped artifacts (`timestamps.csv`, `webcam_output.avi`, `screen_recording.avi`) that could later be reviewed or correlated to understand not just what was on screen, but whether I was actually looking at it.

This is rough. The thresholding is explicitly something to tune. The attention model is simplified. But it represents the project expanding beyond software events into bodily signals — exactly the direction the broader vision requires to explain good days and bad days.

## What It Does

- **Eye aspect ratio detection** from dlib facial landmarks (6 points per eye)
- **Attention classification**: "at" (looking at screen) vs "away" (looking elsewhere) with configurable threshold
- **Dual video recording**: synchronized webcam capture + screen capture
- **Timestamped event logging** to CSV with frame-level gaze state
- ~20 FPS real-time processing

## What's Inside

```
09-eye-tracking-ml/
└── ml_eyes/
    ├── detect_eyes.py         # Real-time eye detection with webcam + screen recording
    ├── test_save.py           # Video file analysis with eye aspect ratio tracking
    ├── requirements.txt       # Dependencies (dlib, opencv-python, pyautogui, etc.)
    ├── webcam_output.avi      # Recorded webcam footage (generated artifact)
    ├── screen_recording.avi   # Synchronized screen capture (generated artifact)
    ├── timestamps.csv         # Timestamped attention events (generated artifact)
    └── eyes/                  # Training/reference data
```

## What I Learned

That even a rough biometric signal is surprisingly informative. Knowing "I was looking at the screen" vs "I wasn't" is a binary that, combined with the activity tracker's record of what was on screen, starts to paint a real picture of attention patterns. The harder lesson: calibrating physiological thresholds across lighting conditions, distances, and faces is a deep problem — one where simple aspect ratios are a starting point, not a solution.

---

← [Prev: #08 Hand Gesture Tracker](../08-hand-gesture-tracker/) | [Collection Home](../README.md) | [Next: #10 Action States](../10-action-states/) →
