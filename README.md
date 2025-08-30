# Hand-Gesture-Recognition-with-MediaPipe-for-Real-Time-Game-Control-
🎮 Hand Gesture Recognition for Game Control using MediaPipe

This project uses MediaPipe and OpenCV to recognize hand gestures via webcam and map them to keyboard controls for popular PC games. With this, you can play games like Subway Surfers and Hill Climb Racing using only your hand movements — no keyboard required!

# 🚀 Features

Real-time hand tracking using MediaPipe Hands.

Gesture recognition with rule-based logic (no training needed).

Maps gestures to keyboard inputs using pyautogui.

Smooth gameplay with gesture history + cooldown to avoid false triggers.

Works with any PC game that uses arrow keys.

# 🕹️ Supported Games
1. Subway Surfers (Hand Controls)

One finger (Index Up) → Jump (↑ key)

Two fingers (Index + Middle Up) → Slide (↓ key)

Three fingers (Index + Middle + Ring Up) → Move Left (← key)

Four fingers (All Up) → Move Right (→ key)

The system uses a gesture history buffer to confirm actions and a cooldown to prevent spamming inputs.

2. Hill Climb Racing (Hand Controls)

Open Hand (All fingers up) → Accelerate (→ key)

Fist (No fingers up) → Brake/Reverse (← key)

Neutral (any other gesture) → Release keys

# 🛠️ Tech Stack

Python 3.x

OpenCV
 → Webcam capture & image processing

MediaPipe
 → Hand landmark detection

PyAutoGUI
 → Keyboard control emulation

# ▶️ How to Run

1. Clone this repository:
   git clone https://github.com/your-username/hand-gesture-game-control.git cd hand-gesture-game-control


2. Install dependencies:

   pip install opencv-python mediapipe pyautogui
   
3.Run the script for your game:

  Subway Surfers

   python subway_surfer_control.py


 Hill Climb Racing

   python hill_climb_control.py


4. Start the game and control it with your hand gestures! 🖐️

# 📌 Notes

Make sure your webcam is enabled and has good lighting.

Gestures may need slight adjustments depending on your camera angle.

Works on any game that uses arrow keys — you can adapt the key mapping easily in the code.
