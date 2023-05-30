import cv2
import imutils
import socket
import numpy as np
import base64

BUFF_SIZE = 65536
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
host_name = socket.gethostname()
host_ip = '100.88.162.36'
port = 5000
message = b'hello'

client_socket.sendto(message, (host_ip, port))

while True:
    packet, _ = client_socket.recvfrom(BUFF_SIZE)
    data = base64.b64decode(packet)
    npdata = np.frombuffer(data, dtype=np.uint8)
    frame = cv2.imdecode(npdata, cv2.IMREAD_COLOR)

    # Modify frame here (e.g., image enhancement)
    # factor = 1
    # img = Image.fromarray(frame)
    # brightnessEnhancer = ImageEnhance.Brightness(img)
    # output = brightnessEnhancer.enhance(factor)
    # contrastEnhancer = ImageEnhance.Contrast(output)
    # output = contrastEnhancer.enhance(factor)
    # frame = np.asarray(output)

    cv2.imshow("RECEIVING VIDEO", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        client_socket.close()
        break
