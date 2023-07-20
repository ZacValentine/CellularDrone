import zmq
import cv2
import numpy as np
import zlib
import base64
import time

# Server IP address and port
host_ip = '100.80.57.27'
port = 5000

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect(f"tcp://{host_ip}:{port}")
socket.subscribe(b"")

print(f"[CLIENT] Connected to server: {host_ip}:{port}")

while True:
    try:
        # Receive the frame from the server (publisher) using ZeroMQ PUB-SUB pattern
        encoded_data = socket.recv()
        decompressed_data = zlib.decompress(base64.b64decode(encoded_data))

        # Convert the frame from bytes to numpy array
        frame = np.frombuffer(decompressed_data, dtype=np.uint8)
        frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

        # Modify frame here

        # Resize
        frame = cv2.resize(frame, (1920, 1080))

        # Display the frame
        cv2.imshow('Video Stream', frame)

        # Receive keys
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    except zlib.error:
        print('[CLIENT] Error decompressing frame')

# Close the client socket
cv2.destroyAllWindows()
