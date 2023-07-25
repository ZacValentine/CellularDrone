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

# Desired frame rate (FPS) to be sent to the client
desired_fps = 30
frame_interval = 1.0 / desired_fps

vid = cv2.VideoCapture(0)
vid.set(cv2.CAP_PROP_FPS, desired_fps)

WIDTH = 3000
# WIDTH = 400 # 4.5mbps CONFIRMED
#WIDTH = 200  # 1.7mbps CONFIRMED
# WIDTH = 100 # 0.7mbps CONFIRMED

print("[SERVER] Server is up. Waiting for client connection...")

# Initialize bandwidth measurement variables
start_time = time.time()
total_data_sent = 0

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
    if elapsed_time >= 1.0:
        data_sent_per_second = (total_data_sent * 8) / (elapsed_time * 1000000)  # Convert to Mbps
        print(f'[SERVER] Data sent per second: {data_sent_per_second:.2f} Mbps')
        start_time = time.time()
        total_data_sent = 0
    else:
        total_data_sent += len(encoded_data)

    # Send the encoded frame to the client using ZeroMQ PUB-SUB pattern
    if elapsed_time >= frame_interval:
        socket.send(encoded_data)
        start_time = time.time()

    # Receive keys
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

# Release the resources
vid.release()
cv2.destroyAllWindows()
