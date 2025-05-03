# 🧤 AI Hand Detection Safety System

This project is a real-time safety solution using AI-powered computer vision.  
It detects when a human hand enters a **restricted zone** using a webcam, and then:

- 🚨 Sends an **MQTT alert** to an Omron PLC  
- 🗃️ Logs the detection event to a **MySQL database**  
- 🧠 Uses **MediaPipe** for hand tracking and **OpenCV** for zone detection

---

## 🎯 Use Case

In industrial environments like capping machines, indexing systems, or filling lines, operator safety is critical.  
This system helps detect unsafe proximity before damage or injury occurs.

---

## 💻 Tech Stack

- Python
- OpenCV
- MediaPipe (by Google)
- MySQL (via mysql-connector-python)
- MQTT (paho-mqtt)
- Omron PLC (Ethernet/IP ready)

---

## 📸 How It Works

- Tracks 21 hand landmarks using MediaPipe
- Monitors if index finger enters a pre-defined danger zone
- Sends `HAND_DETECTED` over MQTT
- Logs timestamp + message to MySQL for traceability

---

## 📦 Setup

```bash
pip install opencv-python mediapipe paho-mqtt mysql-connector-python
