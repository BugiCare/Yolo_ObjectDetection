import cv2
import socket
import torch
import time
import numpy as np

# 소켓 생성

receiveHOST = '0.0.0.0'
receivePORT = 1111
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((receiveHOST, receivePORT))
server_socket.listen()

# load Model
model = torch.hub.load('ultralytics/yolov5', 'custom', path='yolov5/runs/train/exp/weights/last.pt', force_reload = True)

sendHOST = '192.168.1.5'  # 스프링부트 서버의 IP 주소
sendPORT = 2222    # 스프링부트 서버와 통신할 포트 번호
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        
client_socket.connect((sendHOST, sendPORT))

# 클라이언트 연결 대기
conn, addr = server_socket.accept()

# time.sleep(5) 썼더니 영상프레임도 5초마다 와서 timeCount 변수 생성
timeCount = 30

# 영상 수신 및 처리
while True:
    # 데이터 길이 수신
    data = conn.recv(16)
    if not data:
        break
    data_length = int(data)

    # 데이터 수신
    data = b''
    while len(data) < data_length:
        packet = conn.recv(data_length - len(data))
        if not packet:
            break
        data += packet

    # 수신한 데이터 디코딩 및 처리
    np_data = np.frombuffer(data, dtype=np.uint8)
    frame = cv2.imdecode(np_data, cv2.IMREAD_UNCHANGED)

    # Make detections in Real-time
    results = model(frame) # pass frame to Yolov5 Model and get result

    # 처리된 영상 출력
    cv2.imshow('YOLO', np.squeeze(results.render()))
    
    resultText = ""
    
    print("===============================")    
    if("closeRefrigerator" in str(results)):
        resultText += "closeRefrigerator  "
    elif("openRefrigerator" in str(results)):
        resultText += "openRefrigerator  "

    if("fallenPerson" in str(results)):
        resultText += "fallenPerson  "
    elif("sleepingPerson" in str(results)):
        resultText += "sleepingPerson  "
    elif("standingPerson" in str(results)):
        resultText += "standingPerson  "
        
    if (resultText == ""):
        resultText = "none"

    print(resultText)
    print("===============================")

    # 텍스트 전달
    resultText += "\n"

    if timeCount == 30:  # 체감상 한 3초
        client_socket.sendall(resultText.encode())

    # 1초 감소
    timeCount -= 1

    if timeCount == 0:
        # 0초가 되면 다시 5초 카운트
        timeCount = 30

    # 키 입력 대기
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 소켓 종료c
conn.close()
client_socket.close()
server_socket.close()

# OpenCV 윈도우 종료
cv2.destroyAllWindows()
