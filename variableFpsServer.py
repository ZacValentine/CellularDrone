
# ZMQ - LOW LATENCY - SUPPOSED CHANGE FPS WHEN UPLOAD SPEED IS HIGHER THAN SPECIFIED UPLOAD SPEED - LATENCY NOT SUPPOSED TO INCREASE WHEN UPLOAD IS LOWER THAN MBPS

import zmq
import cv2
import imutils
import zlib
import base64
import time

# Server IP address and port
host_ip = '100.80.57.27'
port = 5000

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind(f"tcp://{host_ip}:{port}")

vid = cv2.VideoCapture(0)
WIDTH = 400

print("[SERVER] Server is up. Waiting for client connection...")

# Initialize bandwidth measurement variables
start_time = time.time()
total_data_sent = 0
elapsed_frames = 0

# Set the initial target frame rate (adjust as needed)
target_frame_rate = 30

# Initialize buffer to store frames
buffer_size = 5  # Number of frames to store in the buffer
frame_buffer = []

# Initialize timer for frame rate control
last_frame_time = time.time()

while True:
    # Get frame
    _, frame = vid.read()
    # Resize frame
    frame = imutils.resize(frame, width=WIDTH)

    # Compress the frame
    _, compressed_frame = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
    compressed_data = zlib.compress(compressed_frame)
    encoded_data = base64.b64encode(compressed_data)

    # Calculate data sent per second
    elapsed_time = time.time() - start_time
    elapsed_frames += 1
    if elapsed_time >= 1.0:
        data_sent_per_second = (total_data_sent * 8) / (elapsed_time * 1000000)  # Convert to Mbps
        print(f'[SERVER] Data sent per second: {data_sent_per_second:.2f} Mbps')
        print(f'[SERVER] Target frame rate: {target_frame_rate} fps')
        start_time = time.time()
        total_data_sent = 0
        elapsed_frames = 0

        # Calculate the desired frame rate to achieve the target bandwidth
        target_data_rate = 4  # Set the desired data rate in Mbps (adjust as needed)
        print("[SERVER] Target data rate:", target_data_rate)

        # Calculate the actual frame rate based on elapsed time
        actual_frame_rate = elapsed_frames / elapsed_time

        # Use a proportional control algorithm to adjust the target frame rate
        adjustment_factor = 0.1  # Set the proportional control factor (adjust as needed)
        error = data_sent_per_second - target_data_rate
        target_frame_rate = max(1, target_frame_rate + int(error * adjustment_factor))

        # Limit the target frame rate to a maximum of 30
        target_frame_rate = min(target_frame_rate, 30)

    # Add the frame to the buffer
    frame_buffer.append(encoded_data)

    # Limit the buffer size to prevent excessive memory usage
    if len(frame_buffer) > buffer_size:
        frame_buffer.pop(0)

    # Calculate the actual frame display rate based on elapsed time
    actual_frame_rate = elapsed_frames / elapsed_time

    # Send the most recent frame from the buffer if it's time for the next frame
    if frame_buffer and actual_frame_rate >= target_frame_rate:
        last_frame_time = time.time()
        latest_frame = frame_buffer.pop()
        socket.send(latest_frame)
        total_data_sent += len(latest_frame)

    # Receive keys
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

# Release the resources
vid.release()
cv2.destroyAllWindows()
