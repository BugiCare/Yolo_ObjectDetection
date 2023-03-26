### 파일 설명

------
1. makeImg.py
* 라즈베리파이에서 딥러닝용 이미지 촬영 코드 
2. receiveRaspiCam.py
* 서버 코드
2. sendVideoToServer.py
* 라즈베리파이(호스트) 코드
<br>


### 실행방법

------

1. 서버컴퓨터에서 python receiveRaspiCam.py 로 서버를 실행시킨다. (반드시 서버 먼저 실행)
2. 라즈베리파이에서 python sendVideoToServer.py 로 코드를 실행시킨다.
3. 라즈베리파이에서 전송한 영상이 서버컴퓨터에서 Yolo Object Detection을 통해 딥러닝된 결과로 나타난다.
