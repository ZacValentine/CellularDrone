import socket
import cv2
import numpy as np

# Server IP address and port
host_ip = '100.80.57.27'
port = 5000

# Create a TCP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((host_ip, port))
print(f'[CLIENT] Connected to server: {host_ip}:{port}')

while True:
    # Receive the frame size from the server
    frame_size_bytes = client_socket.recv(4)
    frame_size = int.from_bytes(frame_size_bytes, byteorder='big')

    # Receive the frame from the server
    frame_bytes = b''
    while len(frame_bytes) < frame_size:
        remaining_bytes = frame_size - len(frame_bytes)
        frame_bytes += client_socket.recv(4096 if remaining_bytes > 4096 else remaining_bytes)

    # Convert the frame from bytes to numpy array
    frame = np.frombuffer(frame_bytes, dtype=np.uint8).reshape((480, 640, 3))
    frame = cv2.resize(frame, (1920, 1080))

    # Display the frame
    cv2.imshow('Video Stream', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
