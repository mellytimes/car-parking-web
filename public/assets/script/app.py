# Required libraries: flask, flask-cors, paho-mqtt, opencv-python
# pip install flask flask-cors paho-mqtt opencv-python

import paho.mqtt.client as mqtt
import cv2
import time
import sys
from flask import Flask, Response
from flask_cors import CORS  # <-- Added

app = Flask(__name__)
CORS(app) 
stream_url = 'rtsp://user:password@123.45.67.89/stream'
# --- Configuration ---
BROKER_ADDRESS = "mqtt-ajoy.ddns.net"
BROKER_PORT = 1883
MQTT_USER = "AIoT"
MQTT_PASSWORD = "codingthailand"

PUB_CAR_SIZE_TOPIC = "/aiot/ajoyjaa/carsize"
SUB_BORDER_COLOR_TOPIC = "/aiot/ajoyjaa/bordercolor"

CAMERA_INDEX = 0

g_border_color = (0, 255, 0) 

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Successfully connected to MQTT Broker!")
        client.subscribe(SUB_BORDER_COLOR_TOPIC)
    else:
        print(f"Failed to connect, error code: {rc}\n")
        sys.exit()

def on_message(client, userdata, message):
    global g_border_color
    try:
        payload = message.payload.decode("utf-8")
        topic = message.topic
        print(f"Received: '{payload}' on topic: '{topic}'")

        if topic == SUB_BORDER_COLOR_TOPIC:
            color_map = {
                "RED": (0, 0, 255),
                "GREEN": (0, 255, 0),
                "BLUE": (255, 0, 0)
            }
            g_border_color = color_map.get(payload.upper(), (255, 255, 255))
    except Exception as e:
        print(f"Error processing message: {e}")

def setup_mqtt_client():
    try:
        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
        client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
        client.on_connect = on_connect
        client.on_message = on_message
        client.connect(BROKER_ADDRESS, BROKER_PORT, 60)
        return client
    except Exception as e:
        print(f"Error connecting to MQTT broker: {e}")
        return None

# --- Video Streaming Generator ---
def generate_frames():
    car_cascade_path = cv2.data.haarcascades + 'haarcascade_car.xml'
    car_cascade = cv2.CascadeClassifier(car_cascade_path)
    if car_cascade.empty():
        print(f"Error loading cascade: {car_cascade_path}")
        return

    cap = cv2.VideoCapture(CAMERA_INDEX)  # Use stream URL for RTSP
    if not cap.isOpened():
        print(f"Error: Could not open camera index {CAMERA_INDEX}")
        return

    client = setup_mqtt_client()
    if not client:
        cap.release()
        return
    
    client.loop_start()
    last_publish_time = time.time()

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cars = car_cascade.detectMultiScale(gray, 1.1, 5, minSize=(50, 50))

            for (x, y, w, h) in cars:
                cv2.rectangle(frame, (x, y), (x + w, y + h), g_border_color, 2)
                cv2.putText(frame, "Car", (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, g_border_color, 2)

                if time.time() - last_publish_time > 1.0:
                    payload = str(w)
                    client.publish(PUB_CAR_SIZE_TOPIC, payload)
                    last_publish_time = time.time()

            _, buffer = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

    finally:
        client.loop_stop()
        client.disconnect()
        cap.release()

# --- Routes ---
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    print("--- Starting MQTT Car Detection Web Server ---")
    app.run(host='0.0.0.0', port=5001, debug=True)
