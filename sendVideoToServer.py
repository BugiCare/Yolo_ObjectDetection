import cv2
import socket
import numpy as np

# 소켓 생성
HOST = '192.168.1.5'
PORT = 1234
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# 카메라 모듈 초기화
camera = cv2.VideoCapture(0)

while True:
    # 영상 촬영
    ret, frame = camera.read()

    # 영상 처리
    processed_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # 영상 전송
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    result, imgencode = cv2.imencode('.jpg', processed_frame, encode_param)
    data = np.array(imgencode)
    string_data = data.tostring()
    client_socket.send(str(len(string_data)).ljust(16).encode())
    client_socket.send(string_data)

    # 키 입력 대기
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 소켓 종료
client_socket.close()

# 카메라 모듈 종료
camera.release()
cv2.destroyAllWindows()
