import cv2
import socket
import numpy as np

import requests
import json
import base64
import time

url = "http://3.36.218.186:5000/image"
headers = {
        "Content-Type": "application/json"
}

# 카메라 모듈 초기화
camera = cv2.VideoCapture(0)

while True:
    # 영상 촬영
    ret, frame = camera.read()
    frame = cv2.flip(frame, -1)

    # 영상 전송
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 10]
    img_b64 = base64.b64encode(cv2.imencode('.jpg', frame, encode_param)[1]).decode()
    
    files = {'file': ('image', img_b64)}
    response = requests.post(url, files=files)

    print("response = ", response)

    # 키 입력 대기
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 카메라 모듈 종료
camera.release()
cv2.destroyAllWindows()
