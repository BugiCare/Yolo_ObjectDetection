import cv2
import base64
import numpy as np
from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins='*')

cap = cv2.VideoCapture(0)

def video_feed():
    while True:
        ret, frame = cap.read()
        _, img_encoded = cv2.imencode('.jpg', frame)
        data = base64.b64encode(img_encoded).decode('utf-8')
        socketio.emit('image', data)

if __name__ == '__main__':
    socketio.start_background_task(video_feed)
    socketio.run(app, host='192.168.1.5')
