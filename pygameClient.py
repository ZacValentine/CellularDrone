import cv2
import imutils
import socket
import numpy as np
import base64
import zlib
from PIL import Image, ImageEnhance
import pygame

pygame.joystick.init()
pygame.init()
screen = pygame.display.set_mode([240, 160])
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
for i in range(pygame.joystick.get_count()):
    joysticks.append(pygame.joystick.Joystick(i))
    joysticks[-1].init()


BUFF_SIZE = 65536
#BUFF_SIZE = 35536
#SML_BUFF_SIZE = 100
SML_BUFF_SIZE = 1000
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
host_ip = '100.110.162.27'
port = 5000

# send msg so server has client addr
client_socket.sendto(b'', (host_ip, port))

key_state = {
        'w': False,
        's': False,
        'd': False,
        'a': False,
    }

while True:
    # recv packet
    packet, _ = client_socket.recvfrom(BUFF_SIZE)
    # decode
    data = packet.decode()
    decoded_data = base64.b64decode(data)
    # decompress
    decompressed_data = zlib.decompress(decoded_data)
    # prep frame for modification
    npdata = np.frombuffer(decompressed_data, dtype=np.uint8)
    frame = cv2.imdecode(npdata, cv2.IMREAD_COLOR)
    # modify frame here
    #resize
    #frame = cv2.resize(frame, (1920, 1080))

    for event in pygame.event.get():
        if event.type == pygame.JOYBUTTONDOWN:
            if joysticks[0].get_button(0):
                key_state = {
                        'w': False,
                        's': True,
                        'd': False,
                        'a': False,
                    }
            elif joysticks[0].get_button(1):
                key_state = {
                        'w': False,
                        's': False,
                        'd': True,
                        'a': False,
                    }
            elif joysticks[0].get_button(2):
                key_state = {
                        'w': False,
                        's': False,
                        'd': False,
                        'a': True,
                    }
            elif joysticks[0].get_button(3):
                key_state = {
                        'w': True,
                        's': False,
                        'd': False,
                        'a': False,
                    }
            else:
                key_state = {
                        'w': False,
                        's': False,
                        'd': False,
                        'a': False,
                    }
        elif event.type == pygame.JOYBUTTONUP:
            key_state = {
                        'w': False,
                        's': False,
                        'd': False,
                        'a': False,
                    }

    # keys to str
    keys = f"{''.join([key for key, value in key_state.items() if value])}"
    # send keys
    client_socket.sendto(keys.encode('utf-8'), (host_ip, port))

    cv2.imshow("RECEIVING VIDEO", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        client_socket.close()
        break
