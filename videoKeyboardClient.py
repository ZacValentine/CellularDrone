import cv2
import imutils
import socket
import numpy as np
import base64
import zlib
from PIL import Image, ImageEnhance

BUFF_SIZE = 65536
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
host_ip = '100.80.57.27'
port = 5000
message = b'hello'

client_socket.sendto(message, (host_ip, port))

while True:
    packet, _ = client_socket.recvfrom(BUFF_SIZE)

    # Split the packet into header and data
    header, data = packet.decode().split('|', 1)

    # Process the header for keyboard information
    # For example, if the header format is "KEYS:w,s,d,a"
    keys = header.split(':')[1].split(',')

    # Process the keyboard information as desired
    # For example, you can print the keys list
    print("Keyboard Info:", keys)

    decoded_data = base64.b64decode(data)
    decompressed_data = zlib.decompress(decoded_data)

    npdata = np.frombuffer(decompressed_data, dtype=np.uint8)
    frame = cv2.imdecode(npdata, cv2.IMREAD_COLOR)

    # Modify frame here (e.g., image enhancement)
    factor = 1
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(frame)
    brightness_enhancer = ImageEnhance.Brightness(img_pil)
    output = brightness_enhancer.enhance(factor)
    contrast_enhancer = ImageEnhance.Contrast(output)
    output = contrast_enhancer.enhance(factor)
    frame = np.asarray(output)

    cv2.imshow("RECEIVING VIDEO", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        client_socket.close()
        break
