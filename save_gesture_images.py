# save_gesture_images.py
import cv2
import mediapipe as mp
import os

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
cap = cv2.VideoCapture(0)

gesture_id = input("Enter gesture label (e.g. 0 for fist): ")
save_dir = f"dataset/{gesture_id}"
os.makedirs(save_dir, exist_ok=True)

count = 0
while count < 200:
    ret, frame = cap.read()
    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(img_rgb)

    if result.multi_hand_landmarks:
        x_min = y_min = 1
        x_max = y_max = 0
        for handLms in result.multi_hand_landmarks:
            for lm in handLms.landmark:
                x_min = min(x_min, lm.x)
                y_min = min(y_min, lm.y)
                x_max = max(x_max, lm.x)
                y_max = max(y_max, lm.y)

            h, w, _ = frame.shape
            x1, y1 = int(x_min * w) - 20, int(y_min * h) - 20
            x2, y2 = int(x_max * w) + 20, int(y_max * h) + 20
            hand_crop = frame[y1:y2, x1:x2]

            if hand_crop.size > 0:
                hand_crop = cv2.resize(hand_crop, (64, 64))
                gray = cv2.cvtColor(hand_crop, cv2.COLOR_BGR2GRAY)
                cv2.imwrite(f"{save_dir}/{count}.jpg", gray)
                count += 1
                print(f"Saved {count}/200")

    cv2.imshow("Collecting", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
