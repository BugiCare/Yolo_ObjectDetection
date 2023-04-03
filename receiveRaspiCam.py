import cv2
import socket
import torch
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


# 클라이언트 연결 대기
client_socket, addr = server_socket.accept()

# 영상 수신 및 처리
while True:
    # 데이터 길이 수신
    data = client_socket.recv(16)
    if not data:
        break
    data_length = int(data)

    # 데이터 수신
    data = b''
    while len(data) < data_length:
        packet = client_socket.recv(data_length - len(data))
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
    
    flag = 0
    refriStatus = ""
    doorStatus = ""
    personStatus = ""

    text = ""
    
    print("===============================")    
    if("closeRefrigerator" in str(results)):
        flag = 1
        refriStatus = "closeRefrigerator"
    elif("openRefrigerator" in str(results)):
        flag = 1
        refriStatus = "openRefrigerator"

    if("fallenPerson" in str(results)):
        flag = 1
        personStatus = "fallenPerson"
    elif("sleepingPerson" in str(results)):
        flag = 1
        personStatus = "sleepingPerson"
    elif("standingPerson" in str(results)):
        flag = 1
        personStatus = "standingPerson"  
        
    if (flag == 0):
        print("none")

    print(refriStatus)
    print(personStatus)
    print("===============================")

    text = refriStatus + " " + doorStatus + " " + personStatus
    sendHOST = 'localhost'  # 스프링부트 서버의 IP 주소
    sendPORT = 2222    # 스프링부트 서버와 통신할 포트 번호
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        
    client_socket.connect((sendHOST, sendPORT))

    # 텍스트 전달
    client_socket.sendall(text.encode())

    # 소켓 종료
    client_socket.close()


    # 키 입력 대기
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 소켓 종료
server_socket.close()

# OpenCV 윈도우 종료
cv2.destroyAllWindows()
