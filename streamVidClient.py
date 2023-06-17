import socket
import cv2
import numpy as np
import zlib
import base64
import time

# Server IP address and port
host_ip = '100.80.57.27'
port = 5000

# Create a TCP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((host_ip, port))
print(f'[CLIENT] Connected to server: {host_ip}:{port}')

start_time = time.time()
total_data_received = 0

while True:
    # Receive the frame size from the server
    frame_size_bytes = client_socket.recv(4)
    frame_size = int.from_bytes(frame_size_bytes, byteorder='big')

    # Receive the encoded frame from the server
    frame_bytes = b''
    while len(frame_bytes) < frame_size:
        remaining_bytes = frame_size - len(frame_bytes)
        frame_bytes += client_socket.recv(4096 if remaining_bytes > 4096 else remaining_bytes)

    # Decode the frame
    encoded_data = base64.b64decode(frame_bytes)
    decompressed_data = zlib.decompress(encoded_data)

    # Convert the frame from bytes to numpy array
    frame = np.frombuffer(decompressed_data, dtype=np.uint8)
    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
    
    # Modify frame here
    # Resize
    frame = cv2.resize(frame, (1920, 1080))

    # Display the frame
    cv2.imshow('Video Stream', frame)

    # Calculate data received per second
    elapsed_time = time.time() - start_time
    if elapsed_time >= 1.0:
        data_received_per_second = (total_data_received * 8) / (elapsed_time * 1000000)  # Convert to Mbps
        print(f'[CLIENT] Data received per second: {data_received_per_second} Mbps')
        start_time = time.time()
        total_data_received = 0
    else:
        total_data_received += frame_size

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Close the client socket
client_socket.close()
cv2.destroyAllWindows()
