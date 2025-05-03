import cv2
import mediapipe as mp
import paho.mqtt.publish as publish
import mysql.connector
from datetime import datetime

# --- Initialize Mediapipe ---
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1)

# --- MQTT Settings ---
MQTT_TOPIC = "machine/hand_detected"
MQTT_BROKER = "YOUR_PLC_IP"  # Example: "10.167.40.19"

# --- MySQL Settings ---
try:
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="hand_detection"
    )
    cursor = mydb.cursor()
    print("✅ Connected to MySQL")
except mysql.connector.Error as err:
    print("❌ MySQL Error:", err)
    exit()

# --- Start Webcam ---
cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    if not success:
        break

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(img_rgb)

    if result.multi_hand_landmarks:
        for hand_landmark in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_landmark, mp_hands.HAND_CONNECTIONS)

            for id, lm in enumerate(hand_landmark.landmark):
                h, w, _ = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)

                if id == 8:  # Index fingertip
                    cv2.circle(img, (cx, cy), 10, (0, 0, 255), cv2.FILLED)
                    cv2.rectangle(img, (100, 100), (200, 200), (255, 0, 0), 2)

                    if 100 < cx < 200 and 100 < cy < 200:
                        cv2.putText(img, "HAND IN ZONE!", (50, 50),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                        # --- Send MQTT signal to PLC ---
                        # try:
                        #     publish.single(MQTT_TOPIC, payload="HAND_DETECTED", hostname=MQTT_BROKER)
                        #     print("📡 MQTT Sent: HAND_DETECTED")
                        # except Exception as e:
                        #     print("❌ MQTT Error:", e)

                        # --- Log event to MySQL ---
                        try:
                            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            cursor.execute("INSERT INTO hand_logs (timestamp, message) VALUES (%s, %s)",
                                           (now, "HAND_DETECTED"))
                            mydb.commit()
                            print("🗃️  Logged to DB at", now)
                        except Exception as e:
                            print("❌ DB Log Error:", e)

    cv2.imshow("Hand Detection", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
