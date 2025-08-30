import cv2
import mediapipe as mp
import pyautogui
import time
from collections import deque

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils

finger_tips = [8, 12, 16, 20]

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

last_action_time = 0
cooldowns = {"Jump": 0.3, "Slide": 0.3, "Left": 0.6, "Right": 0.6}

gesture_history = deque(maxlen=5)
last_gesture = None  # Track last confirmed gesture

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    current_gesture = None

    if result.multi_hand_landmarks:
        for handLms in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)
            lm_list = []
            for id, lm in enumerate(handLms.landmark):
                lm_list.append((int(lm.x * w), int(lm.y * h)))

            fingers = []
            for tip in finger_tips:
                if lm_list[tip][1] < lm_list[tip - 2][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            # Match gesture
            if fingers == [1, 0, 0, 0]:
                current_gesture = "Jump"
            elif fingers == [1, 1, 0, 0]:
                current_gesture = "Slide"
            elif fingers == [1, 1, 1, 0]:
                current_gesture = "Left"
            elif fingers == [1, 1, 1, 1]:
                current_gesture = "Right"

            # Add to history
            gesture_history.append(current_gesture)

            # If majority of last frames agree
            if current_gesture and gesture_history.count(current_gesture) >= 3:
                # Only trigger if it's not same as last_gesture
                if current_gesture != last_gesture:
                    if time.time() - last_action_time > cooldowns[current_gesture]:
                        if current_gesture == "Jump":
                            pyautogui.press("up")
                        elif current_gesture == "Slide":
                            pyautogui.press("down")
                        elif current_gesture == "Left":
                            pyautogui.press("left")
                        elif current_gesture == "Right":
                            pyautogui.press("right")

                        last_action_time = time.time()
                        last_gesture = current_gesture
            else:
                # Reset last gesture if no stable gesture
                last_gesture = None

            # Debug overlay
            cv2.putText(frame, f"Fingers: {fingers}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(frame, f"Gesture: {current_gesture}", (10, 70),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Subway Surfer Hand Control", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC
        break

cap.release()
cv2.destroyAllWindows()
