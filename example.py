"""
Eye Gaze Controlled Media Player
Author: Abhishek Tyagi
Version: 2.3
GitHub: https://github.com/AbhishekTyagi404
CS50 Certificate: https://cs50.harvard.edu/certificates/cdea1963-1535-4aef-be8e-d285f8a4f2e4
"""

import cv2
import time
import pyautogui
from gaze_tracking import GazeTracking

gaze = GazeTracking()
webcam = cv2.VideoCapture(0)

blink_count = 0
last_blink_time = 0
blink_window = 2  # seconds to detect multiple blinks

while True:
    _, frame = webcam.read()
    gaze.refresh(frame)
    frame = gaze.annotated_frame()

    text = ""

    if gaze.is_blinking():
        now = time.time()
        if now - last_blink_time < blink_window:
            blink_count += 1
        else:
            blink_count = 1  # restart count
        last_blink_time = now

        # --- Trigger actions ---
        if blink_count == 2:
            pyautogui.press('right')  # Next song
            print("[MEDIA] Next song triggered (2 blinks)")
            blink_count = 0
        elif blink_count == 3:
            pyautogui.press('space')  # Pause/Play toggle
            print("[MEDIA] Pause/Play toggled (3 blinks)")
            blink_count = 0

        text = f"Blinking ({blink_count})"
    elif gaze.is_right():
        text = "Looking right"
    elif gaze.is_left():
        text = "Looking left"
    elif gaze.is_center():
        text = "Looking center"

    # Display info
    cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)

    left_pupil = gaze.pupil_left_coords()
    right_pupil = gaze.pupil_right_coords()
    cv2.putText(frame, f"Left pupil:  {left_pupil}", (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
    cv2.putText(frame, f"Right pupil: {right_pupil}", (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)

    cv2.imshow("Gaze Media Player", frame)

    if cv2.waitKey(1) == 27:
        break

webcam.release()
cv2.destroyAllWindows()
