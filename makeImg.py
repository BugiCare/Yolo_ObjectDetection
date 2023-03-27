import uuid   # to create a unique identifier
import os   
import time
import cv2


IMAGES_PATH = os.path.join('data', 'newimages')   # 이미지 저장 경로 (/data/images)
labels = ['openRefrigerator', 'closeRefrigerator', 'fallenPerson', 'standingPerson', 'sleepingPerson']   # 분류할 클래스 5개 (일단 문은 빼고)
number_imgs = 320   # 각 클래스마다 수집하고 싶은 이미지 수(잘못 찍힐 것까지 고려)

cap = cv2.VideoCapture(0)

# Loop through Labels
# 클래스 각각 30장씩 찍기 위해 루프 도는 코드
for label in labels:
    print('Collecting images for {}'.format(label))
    time.sleep(5)

    # Loop through image range
    for img_num in range(number_imgs):
        print('Collecting images for {}, image number {}'.format(label, img_num))

        ret, frame = cap.read()   # read video feed from Webcam

        # data/images/class이름/@@@.jpg 같은 형식으로 이미지가 저장됨
        imgname = os.path.join(IMAGES_PATH, label + '.' + str(uuid.uuid1()) + '.jpg')
        
        # Writes out image to file
        cv2.imwrite(imgname, frame)     # frame == capturing from Webcam
        # Render to the Screen
        cv2.imshow('Image Collection', frame)
        # 2 second delay between captures
        time.sleep(2)
    
        # q 누르면 종료됨
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
