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

# Initialize bandwidth measurement variables
start_time = time.time()
total_data_received = 0

# Set the initial target frame rate (adjust as needed)
target_frame_rate = 30

# Initialize buffer to store frames
buffer_size = 5  # Number of frames to store in the buffer
frame_buffer = []

# Initialize timer for frame rate control
last_frame_time = time.time()

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
        frame = cv2.resize(frame, (711, 400))

        # Add the frame to the buffer
        frame_buffer.append(frame)

        # Limit the buffer size to prevent excessive memory usage
        if len(frame_buffer) > buffer_size:
            frame_buffer.pop(0)

        # Calculate data received per second
        elapsed_time = time.time() - start_time
        if elapsed_time >= 1.0:
            data_received_per_second = (total_data_received * 8) / (elapsed_time * 1000000)  # Convert to Mbps
            print(f'[CLIENT] Data received per second: {data_received_per_second:.2f} Mbps')
            start_time = time.time()
            total_data_received = 0

        total_data_received += len(encoded_data)

        # Calculate the actual frame display rate based on elapsed time
        actual_frame_rate = len(frame_buffer) / (time.time() - last_frame_time)

        # Display the most recent frame from the buffer if it's time for the next frame
        if frame_buffer and actual_frame_rate >= target_frame_rate:
            last_frame_time = time.time()
            frame = frame_buffer.pop(0)
            cv2.imshow('Video Stream', frame)

        # Receive keys
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    except zlib.error:
        print('[CLIENT] Error decompressing frame')

# Close the client socket
cv2.destroyAllWindows()
