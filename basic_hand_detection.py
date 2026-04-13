import cv2
import mediapipe as mp

# Initialize Mediapipehi
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=2)

# Start Camera
cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    if not success:
        break

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(img_rgb)

    # Draw hand landmarks if detected
    if result.multi_hand_landmarks:
        for hand_landmark in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_landmark, mp_hands.HAND_CONNECTIONS)

            # Get index finger tip coordinates (landmark ID 8)
            for id, lm in enumerate(hand_landmark.landmark):
                h, w, _ = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)

                if id == 8:  # Index fingertip
                    cv2.circle(img, (cx, cy), 10, (0, 0, 255), cv2.FILLED)
                    # Optional: Draw a restricted zone for visual check
                    cv2.rectangle(img, (100, 100), (200, 200), (255, 0, 0), 2)
                    if 100 < cx < 200 and 100 < cy < 200:
                        cv2.putText(img, "HAND IN ZONE!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow("Hand Detection", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
