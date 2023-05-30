import cv2
import imutils
import socket
import numpy as np
import base64
import zlib

BUFF_SIZE = 65536
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
host_name = socket.gethostname()
host_ip = '100.80.57.27'
port = 5000
socket_address = (host_ip, port)
server_socket.bind(socket_address)
print('listening at:', socket_address)

vid = cv2.VideoCapture(0)
fps, st, frames_to_count, cnt = (0, 0, 20, 0)

while True:
    msg, client_addr = server_socket.recvfrom(BUFF_SIZE)
    print('got connection from', client_addr)

    WIDTH = 400
    while vid.isOpened():
        _, frame = vid.read()
        frame = imutils.resize(frame, width=WIDTH)

        # Compress the frame
        _, compressed_frame = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
        compressed_data = zlib.compress(compressed_frame)

        # Encode the compressed frame to base64
        encoded_frame = base64.b64encode(compressed_data)

        # Send the encoded frame to the client
        server_socket.sendto(encoded_frame, client_addr)

        # Display the frame
        cv2.imshow('TRANSMITTING VIDEO', frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            server_socket.close()
            break
