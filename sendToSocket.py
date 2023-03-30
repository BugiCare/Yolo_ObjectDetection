import socket

# 소켓1 생성 : (라즈베리 역할로 만들어둔 임시 소켓서버)

HOST = 'localhost'  # 소켓 서버2의 IP 주소
PORT = 1111    # 소켓 서버2와 통신할 포트 번호
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# 텍스트 전달
text = "to socket2"
client_socket.sendall(text.encode())

# 소켓1 종료
client_socket.close()