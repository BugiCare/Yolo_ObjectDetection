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
conn, addr = server_socket.accept()

# 이미지 수신 및 저장
while True:
    # 데이터 크기 수신
    data = conn.recv(16)
    data_size = int(data.decode().strip())

    # 이미지 데이터 수신
    data = b''
    while len(data) < data_size:
        packet = conn.recv(data_size - len(data))
        if not packet:
            break
        data += packet

    # 수신된 데이터를 이미지로 변환
    img_data = np.frombuffer(data, dtype=np.uint8)
    img = cv2.imdecode(img_data, cv2.IMREAD_UNCHANGED)

    # 이미지 저장
    cv2.imwrite('received_image.jpg', img)

    # Make detections in Real-time
    results = model(img) # pass frame to Yolov5 Model and get result

    # 처리된 영상 출력
    cv2.imshow('YOLO', np.squeeze(results.render()))
    
    
    print("===============================")
    print(results)
    print("===============================")

     # 키 입력 대기
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 소켓 종료
conn.close()
server_socket.close()

# OpenCV 윈도우 종료
cv2.destroyAllWindows()
