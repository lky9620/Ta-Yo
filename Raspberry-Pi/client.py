# -*- coding: utf8 -*-
import cv2
import RPi.GPIO as GPIO
import socket
import numpy as np
import sys
import time
import choeumpa
import motor


## TCP 사용
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
## server ip, port
s.connect(('220.149.236.152', 8485))
# s.connect(('192.168.0.2', 8485))

## webcam 이미지 capture
cam = cv2.VideoCapture(0)

## 이미지 속성 변경 3 = width, 4 = height
cam.set(3, 640);
cam.set(4, 320);

## 0~100에서 90의 이미지 품질로 설정 (default = 95)
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 83]

try:
    motor.Forward(23)
    pre_data=''
    while True:
        # 비디오의 한 프레임씩 읽는다.
        # 제대로 읽으면 ret = True, 실패면 ret = False, frame에는 읽은 프레임
        ret, frame = cam.read()
        # cv2. imencode(ext, img [, params])
        # encode_param의 형식으로 frame을 jpg로 이미지를 인코딩한다.
        result, frame = cv2.imencode('.jpg', frame, encode_param)
        # frame을 String 형태로 변환
        data = np.array(frame)
        stringData = data.tostring()
        
        
        s.sendall((str(len(stringData))).encode().ljust(16) + stringData)

        recvData = s.recv(512).decode('utf-8')
#         print(recvData)
        if recvData == 'S':
            motor.Forward(13)
            print('Driving Slow')
            pre_data = 'S'
        elif recvData == 'R':
            motor.Forward(25)
            print('Normal Driving')
            pre_data = ''
        elif recvData == 'T':
            motor.Stop()
            print('Redlight Stop')
        elif recvData == 'G':
            motor.Stop()
            print('Stop sign Stop')
            pre_data='G'
        elif pre_data=='G' and recvData =='N':
            motor.Forward(25)
            print('Normal Driving')
            pre_data = ''
        
        if pre_data == 'S':
            dist = choeumpa.distance()
            if dist <=7:
                print('Force Stop!!')    
                motor.Stop()
#         else:
#             motor.Stop()
#             time.sleep(1)
#             motor.Forward(25)
#             continue
#         predata=''
       
except KeybordInterrupt:
    GPIO.cleanup()
    cam.release()
