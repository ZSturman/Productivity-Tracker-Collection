import cv2
import dlib
import numpy as np
from PIL import Image
from datetime import datetime
import csv
import pyautogui

# Constants
#screen_size = (2940, 1912)
screen_size = pyautogui.size()
fps = 20.0

# Dlib face detector and predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# Timestamps
timestamps = []

def find_webcam():
    index = 0
    while True:
        cap = cv2.VideoCapture(index)
        if not cap.read()[0]:
            break
        else:
            # Here you can add additional checks if needed to ensure the right webcam is selected
            # For now, we assume the first available camera is the computer's webcam
            return cap
        cap.release()
        index += 1
    return None

cap = find_webcam()
if not cap or not cap.isOpened():
    print("Error: No webcam found or webcam not opened")
    exit()


# Set up video writers
fourcc = cv2.VideoWriter_fourcc(*'XVID')
webcam_writer = cv2.VideoWriter("webcam_output.avi", fourcc, fps, (int(cap.get(3)), int(cap.get(4)))) 

codec = cv2.VideoWriter_fourcc(*'XVID')
screen_writer = cv2.VideoWriter("screen_recording.avi", codec, fps, screen_size)

if not webcam_writer.isOpened():
    print("Error: Webcam Writer not opened")
    exit()

if not screen_writer.isOpened():
    print("Error: Screen Writer not opened")
    exit()






def analyze_eye_position(eye_points, landmarks, image):
    # Calculate the aspect ratio of the eye
    x1, y1 = landmarks.part(eye_points[0]).x, landmarks.part(eye_points[0]).y
    x2, y2 = landmarks.part(eye_points[3]).x, landmarks.part(eye_points[3]).y
    eye_width = np.linalg.norm(np.array([x2, y2]) - np.array([x1, y1]))

    x1, y1 = landmarks.part(eye_points[1]).x, landmarks.part(eye_points[1]).y
    x2, y2 = landmarks.part(eye_points[5]).x, landmarks.part(eye_points[5]).y
    eye_height = np.linalg.norm(np.array([x2, y2]) - np.array([x1, y1]))

    aspect_ratio = eye_height / eye_width
    return aspect_ratio

def analyze_eyes(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)
    for face in faces:
        landmarks = predictor(gray, face)

        left_eye_points = [36, 37, 38, 39, 40, 41]
        right_eye_points = [42, 43, 44, 45, 46, 47]

        left_eye_aspect_ratio = analyze_eye_position(left_eye_points, landmarks, frame)
        right_eye_aspect_ratio = analyze_eye_position(right_eye_points, landmarks, frame)

        avg_eye_aspect_ratio = (left_eye_aspect_ratio + right_eye_aspect_ratio) / 2

        if avg_eye_aspect_ratio < 0.25:  # Adjust this threshold based on your observations
            print("Eyes are looking away from the screen")
            timestamps.append((datetime.now(), "away"))
        else:
            print("Eyes are looking at the screen")
            timestamps.append((datetime.now(), "at"))


def main():
    cap = cv2.VideoCapture(0)
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Take screenshot
        img = pyautogui.screenshot()
        screen_shot = np.array(img)
        screen_shot = cv2.cvtColor(screen_shot, cv2.COLOR_BGR2RGB)

        # Resize screenshot to match the screen size
        screen_shot = cv2.resize(screen_shot, screen_size)

        screen_writer.write(screen_shot)

        frame_count += 1
        print("Frame count:", frame_count)

        cv2.imshow("frame", frame)

        webcam_writer.write(frame)

        key = cv2.waitKey(1)
        if key == ord("q"):
            break

    webcam_writer.release()
    screen_writer.release()
    cap.release()

    with open("timestamps.csv", "w", newline="") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Timestamp", "Event"])
        csv_writer.writerows(timestamps)

    analyze_eyes(frame) 
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()