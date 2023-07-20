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

# Initialize frame rate (in frames per second)
frame_rate = 30  # Fixed frame rate

while True:
    try:
        # Receive the frame from the server (publisher) using ZeroMQ PUB-SUB pattern
        encoded_data = socket.recv()
        decompressed_data = zlib.decompress(base64.b64decode(encoded_data))

        # Convert the frame from bytes to numpy array
        frame = np.frombuffer(decompressed_data, dtype=np.uint8)
        frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

        # Modify frame here

        # factor = 1
        # img = Image.fromarray(frame)
        # brightnessEnhancer = ImageEnhance.Brightness(img)
        # output = brightnessEnhancer.enhance(factor)
        # contrastEnhancer = ImageEnhance.Contrast(output)
        # output = contrastEnhancer.enhance(factor)
        # frame = np.asarray(output)

        # Resize
        frame = cv2.resize(frame, (1920, 1080))

        # Display the frame
        cv2.imshow('Video Stream', frame)

        # Calculate data received per second
        elapsed_time = time.time() - start_time
        if elapsed_time >= 1.0:
            data_received_per_second = (total_data_received * 8) / (elapsed_time * 1000000)  # Convert to Mbps
            print(f'[CLIENT] Data received per second: {data_received_per_second:.2f} Mbps')
            start_time = time.time()
            total_data_received = 0

        total_data_received += len(encoded_data)

        # Wait to maintain the fixed frame rate
        time.sleep(1.0 / frame_rate)

        # Receive keys
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    except zlib.error:
        print('[CLIENT] Error decompressing frame')

# Close the client socket
cv2.destroyAllWindows()