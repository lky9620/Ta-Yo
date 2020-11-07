from __future__ import division
import time
import torch
import torch.nn as nn
from torch.autograd import Variable
import numpy as np
import cv2
from util import *
import os
import os.path as osp
from darknet import Darknet
import pickle as pkl
import pandas as pd
import random
import socket
import time

batch_size = 16
confidence = 0.85
nms_thesh = 0.85
CUDA = torch.cuda.is_available()
num_classes = 8
classes = load_classes("./obj.names")

print("Loading network.....")
model = Darknet('./yolov3_cls8.cfg')
model.load_weights('./yolov3.backup')
print("Network successfully loaded")

model.net_info["height"] = 416
inp_dim = int(model.net_info["height"])
assert inp_dim % 32 == 0
assert inp_dim > 32

if CUDA:
    model.cuda()
    print('쿠다 준비 완뇨-')

model.eval()

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf:
            return None
        buf += newbuf
        count -= len(newbuf)
    return buf

def write(x, results):
    c1 = tuple(x[1:3].int())
    c2 = tuple(x[3:5].int())
    img = results
    cls = int(x[-1])
    color = random.choice(colors)
    label = "{0}".format(classes[cls])
    cv2.rectangle(img, c1, c2, color, 1)
    t_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_PLAIN, 1, 1)[0]
    c2 = c1[0] + t_size[0] + 3, c1[1] + t_size[1] + 4
    cv2.rectangle(img, c1, c2, color, -1)
    cv2.putText(img, label, (c1[0], c1[1] + t_size[1] + 4), cv2.FONT_HERSHEY_PLAIN, 1, [225, 255, 255], 1);
    return img, label


def ccount(object):
    return class_name.count(object)

def csend(direction):
    if direction == 1:
        conn.send(sendData_Stop.encode('utf-8'))
    elif direction == 2:
        conn.send(sendData_Sign.encode('utf-8'))
    elif direction == 3:
        conn.send(sendData_Slow.encode('utf-8'))
    elif direction == 4:
        conn.send(sendData_Return.encode('utf-8'))
    elif direction == 0:
        conn.send(sendData_None.encode('utf-8'))
sendData_Stop = 'T'
sendData_Slow = 'S'
sendData_None = 'N'
sendData_Return = 'R'
sendData_Sign = 'G'




HOST = ''
PORT = 8485

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')

s.bind((HOST, PORT))
print('Socket bind complete')
s.listen(10)
print('Socket now listening')
# cap = cv2.VideoCapture(0)
conn, addr = s.accept()
Pre_SendData = ''

predata=''
while True:
    start = time.time()
    length = recvall(conn, 16)
    stringData = recvall(conn, int(length))
    data = np.fromstring(stringData, dtype='uint8')
    frame = cv2.imdecode(data, cv2.IMREAD_COLOR)

    # if ret:
    img = prep_image(frame, inp_dim)
    im_dim = frame.shape[1], frame.shape[0]
    im_dim = torch.FloatTensor(im_dim).repeat(1, 2)

    if CUDA:
        im_dim = im_dim.cuda()
        img = img.cuda()

    with torch.no_grad():
        output = model(Variable(img, volatile=True), CUDA)
    output = write_results(output, confidence, num_classes, nms_conf=nms_thesh)

    if type(output) == int:   ## 인식 되는게 없을 경우 해당 if문 걸림 오고 while문 탈출
        conn.send(sendData_None.encode('utf-8'))
        cv2.imshow("frame with no class", frame)
        key = cv2.waitKey(1)
        if key & 0xFF == ord('q'):
            break
        continue
    im_dim = im_dim.repeat(output.size(0), 1)
    scaling_factor = torch.min(416 / im_dim, 1)[0].view(-1, 1)

    output[:, [1, 3]] -= (inp_dim - scaling_factor * im_dim[:, 0].view(-1, 1)) / 2
    output[:, [2, 4]] -= (inp_dim - scaling_factor * im_dim[:, 1].view(-1, 1)) / 2

    output[:, 1:5] /= scaling_factor

    for i in range(output.shape[0]):
        output[i, [1, 3]] = torch.clamp(output[i, [1, 3]], 0.0, im_dim[i, 0])
        output[i, [2, 4]] = torch.clamp(output[i, [2, 4]], 0.0, im_dim[i, 1])

    classes = load_classes('./obj.names')
    colors = pkl.load(open("pallete", "rb"))

    list(map(lambda x: write(x, frame)[0], output))
    class_name = list(map(lambda x: write(x, frame)[1], output))
    print(class_name)
    # class_name = "".join(class_name)
    # print(class_name)
    cslist = []
    if ccount('redlight') >= 1:
        cslist.append(1)
    if ccount('greenlight') >= 1:
        cslist.append(4)
    if ccount('stop') >= 1:
        cslist.append(2)
        predata = 'stop'
    if ccount('kidzoneout') >= 1:
        cslist.append(4)
    if ccount('kidzone') >= 1:
        cslist.append(3)
    if ccount('person') >= 3:
        cslist.append(3)
    else:
        cslist.append(4)

    if cslist is not None:
        # if sorted(cslist)[0] == 2 and predata == 'stop':
        csend(sorted(cslist)[0])
        # else:
        #     predata = ''
        #     csend(sorted(cslist)[0])
        #     print(csend(sorted(cslist)[0]))
    else:
        csend(0)

    cv2.imshow("frame with class", frame)
    key = cv2.waitKey(1)

    if key & 0xFF == ord('q'):
        break
