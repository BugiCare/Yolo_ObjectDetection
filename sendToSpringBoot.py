import socket

# 소켓2 생성

receiveHOST = '0.0.0.0'  
receivePORT = 1111       # 소켓1 서버와 통신할 포트 번호

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((receiveHOST, receivePORT))
server_socket.listen()

conn, addr = server_socket.accept()
with conn:
    print('socket1과 연결됨:', addr)
    while True:  # 데이터가 계속 오면 True
        data = conn.recv(1024)  # 데이터 수신 대기
        if not data:
            break
        print('socket1으로부터 받은 메시지:', data.decode())
        
        sendHOST = 'localhost'  # 스프링부트 서버의 IP 주소
        sendPORT = 2222    # 스프링부트 서버와 통신할 포트 번호
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((sendHOST, sendPORT))

        # 텍스트 전달
        text = data.decode() + " to spring"
        client_socket.sendall(text.encode())

        # 소켓 종료
        client_socket.close()

server_socket.close()