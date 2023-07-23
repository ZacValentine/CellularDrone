import zmq
import cv2
import numpy as np
import zlib
import base64
import time
import datetime

# Server IP address and port
host_ip = '100.80.57.27'
port = 5000

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect(f"tcp://{host_ip}:{port}")
socket.subscribe(b"")

print(f"[CLIENT] Connected to server: {host_ip}:{port}")

# Initialize bandwidth measurement variables
start_time = datetime.datetime.now()
total_data_received = 0

# Custom FPS class
class FPS:
    def __init__(self):
        self._start_time = None
        self._num_frames = 0

    def start(self):
        self._start_time = time.time()
        self._num_frames = 0
        return self

    def update(self):
        self._num_frames += 1

    def fps(self):
        elapsed_time = time.time() - self._start_time
        if elapsed_time > 0:
            return self._num_frames / elapsed_time
        else:
            return 0

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

        # Update FPS counter
        if 'fps_counter' not in locals():
            fps_counter = FPS().start()
        else:
            fps_counter.update()

        # Display the FPS on the frame
        fps_text = f"FPS: {fps_counter.fps():.2f}"
        cv2.putText(frame, fps_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Display the frame
        cv2.imshow('Video Stream', frame)

        # Calculate data received per second
        elapsed_time = datetime.datetime.now() - start_time
        if elapsed_time.total_seconds() >= 1.0:
            data_received_per_second = (total_data_received * 8) / (elapsed_time.total_seconds() * 1000000)  # Convert to Mbps
            print(f'[CLIENT] Data received per second: {data_received_per_second:.2f} Mbps')
            start_time = datetime.datetime.now()
            total_data_received = 0
        else:
            total_data_received += len(encoded_data)

        # Receive keys
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    except zlib.error:
        print('[CLIENT] Error decompressing frame')

# Close the client socket
cv2.destroyAllWindows()
