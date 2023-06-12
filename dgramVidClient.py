import cv2
import imutils
import socket
import numpy as np
import base64
import zlib
from PIL import Image, ImageEnhance


BUFF_SIZE = 65536
SML_BUFF_SIZE = 1000
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
host_ip = '100.110.162.27'
port = 5000

# send msg so server has client addr
client_socket.sendto(b'', (host_ip, port))

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
    frame = cv2.resize(frame, (1920, 1080))

    cv2.imshow("RECEIVING VIDEO", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        client_socket.close()
        break
