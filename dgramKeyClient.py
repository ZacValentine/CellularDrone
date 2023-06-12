import cv2
import imutils
import socket
import numpy as np
import base64
import zlib
from PIL import Image, ImageEnhance
import keyboard
from Motor import Motor

BUFF_SIZE = 65536
#BUFF_SIZE = 35536
#SML_BUFF_SIZE = 100
SML_BUFF_SIZE = 1000
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
host_ip = '100.80.57.27'
port = 5001

rightMotor = Motor(25, 23, 24)
leftMotor = Motor(27, 17, 22)

# send msg so server has client addr
client_socket.sendto(b'', (host_ip, port))

while True:
    # recv packet
    packet, _ = client_socket.recvfrom(BUFF_SIZE)
    # decode
    msg = packet.decode('utf-8')
    print(msg)
    
    if len(msg) <= 0:
        leftMotor.stop()
        rightMotor.stop()
    elif msg[0] == 'w':
        leftMotor.forward()
        rightMotor.forward()
    elif msg[0] == 's':
        leftMotor.backward()
        rightMotor.backward()
    elif msg[0] == 'a':
        leftMotor.stop()
        rightMotor.forward()
    elif msg[0] == 'd':
        leftMotor.forward()
        rightMotor.stop()


