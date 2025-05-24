import cv2
import mediapipe as mp
import numpy as np
from tensorflow.keras.models import load_model
from gesture_commands import run_command

model = load_model("cnn_model.h5")
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(img_rgb)

    if result.multi_hand_landmarks:
        for handLms in result.multi_hand_landmarks:
            x_min, y_min = 1, 1
            x_max, y_max = 0, 0
            for lm in handLms.landmark:
                x_min = min(x_min, lm.x)
                y_min = min(y_min, lm.y)
                x_max = max(x_max, lm.x)
                y_max = max(y_max, lm.y)

            h, w, _ = frame.shape
            x1, y1 = int(x_min * w) - 20, int(y_min * h) - 20
            x2, y2 = int(x_max * w) + 20, int(y_max * h) + 20
            crop = frame[y1:y2, x1:x2]
            if crop.size == 0: continue
            crop = cv2.resize(crop, (64, 64))
            gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
            gray = gray.reshape(1, 64, 64, 1) / 255.0
            pred = model.predict(gray)
            gesture = np.argmax(pred)

            # Show prediction
            cv2.putText(frame, f"Gesture: {gesture}", (10, 70),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            run_command(gesture)  # 🎯 Gesture-to-command mapping

    cv2.imshow("Gesture Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
