import cv2
import imutils
import socket
import numpy as np
import base64
import zlib
from PIL import Image, ImageEnhance
import keyboard
from Motor import Motor

BUFF_SIZE = 100

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
host_ip = '100.80.57.27'
port = 5001

motor = Motor(25, 23, 24)
servoMotor = Motor(27, 17, 22)

# send msg so server has client addr
client_socket.sendto(b'', (host_ip, port))

while True:
    # recv packet
    packet, _ = client_socket.recvfrom(BUFF_SIZE)
    # decode
    msg = packet.decode('utf-8')
    print(msg)
    
    if "w" in msg and not "s" in msg:
        motor.backward()
    elif "s" in msg and not "w" in msg:
        motor.forward()
    else:
        motor.stop()
    if "a" in msg and not "d" in msg:
        servoMotor.forward()
    elif "d" in msg and not "a" in msg:
        servoMotor.backward()
    else:
        servoMotor.stop()
