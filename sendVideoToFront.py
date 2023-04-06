import cv2
import base64
import eventlet
from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

# 카메라 캡처
camera = cv2.VideoCapture(0)

@socketio.on('connect')
def connect():
    print('connected')

@socketio.on('disconnect')
def disconnect():
    print('disconnected')

@socketio.on('stream')
def stream():
    while True:
        # 프레임 캡처 및 인코딩
        _, frame = camera.read()
        _, buffer = cv2.imencode('.png', frame)
        jpg_as_text = base64.b64encode(buffer).decode('utf-8')

        # 클라이언트로 이미지 전송
        socketio.emit('image', jpg_as_text)

if __name__ == '__main__':
    # 웹 서버 실행
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 5000)), app)
