import cv2
import mediapipe as mp
import pyautogui
import time

# Mediapipe initialization
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)

cap = cv2.VideoCapture(0)
cap.set(3, 640)  # width
cap.set(4, 480)  # height

last_action_time = 0
cooldown = 0.2  # seconds (reduce double press issue)

def count_fingers(hand_landmarks):
    finger_tips = [8, 12, 16, 20]
    finger_pips = [6, 10, 14, 18]
    count = 0
    for tip, pip in zip(finger_tips, finger_pips):
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[pip].y:
            count += 1
    return count

while True:
    success, frame = cap.read()
    if not success:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)

            fingers = count_fingers(handLms)

            # Open hand (all fingers up) -> Accelerate
            if fingers == 4:
                if time.time() - last_action_time > cooldown:
                    pyautogui.keyDown("right")
                    pyautogui.keyUp("left")
                    last_action_time = time.time()
                    cv2.putText(frame, "Accelerate", (50, 100),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

            # Fist (0 fingers up) -> Brake
            elif fingers == 0:
                if time.time() - last_action_time > cooldown:
                    pyautogui.keyDown("left")
                    pyautogui.keyUp("right")
                    last_action_time = time.time()
                    cv2.putText(frame, "Brake", (50, 100),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

            else:
                # Release both if neutral
                pyautogui.keyUp("right")
                pyautogui.keyUp("left")

    cv2.imshow("Hill Climb Hand Control", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
