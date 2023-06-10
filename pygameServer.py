import cv2
import imutils
import socket
import base64
import zlib
from Motor import Motor


BUFF_SIZE = 65536
#BUFF_SIZE = 35536
SML_BUFF_SIZE = 1000
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
host_ip = '100.110.162.27'
port = 5000
socket_address = (host_ip, port)
server_socket.bind(socket_address)
print('listening at:', socket_address)

vid = cv2.VideoCapture(0)
fps, st, frames_to_count, cnt = (0, 0, 20, 0)

rightMotor = Motor(25, 23, 24)
leftMotor = Motor(27, 17, 22)

while True:
    # get client addr from msg
    msg, client_addr = server_socket.recvfrom(SML_BUFF_SIZE)
    print('got connection from', client_addr)

    WIDTH = 400
    while vid.isOpened():
        # get frame
        _, frame = vid.read()
        # resize frame
        frame = imutils.resize(frame, width=WIDTH)
        # Compress
        _, compressed_frame = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
        compressed_data = zlib.compress(compressed_frame)
        # Encode
        encoded_frame = base64.b64encode(compressed_data)
        # Send Frame
        server_socket.sendto(encoded_frame, client_addr)
        # recv keys
        msg, client_addr = server_socket.recvfrom(SML_BUFF_SIZE)
        # print keys
        msg = msg.decode('utf-8')
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
            
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            server_socket.close()
            break
