


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

fps = 30

vid = cv2.VideoCapture(0)
vid.set(cv2.CAP_PROP_FPS, fps)

#WIDTH = 400 # 4.5mbps CONFIRMED
WIDTH = 200 # 1.7mbps CONFIRMED
#WIDTH = 100 # 0.7mbps CONFIRMED

print("[SERVER] Server is up. Waiting for client connection...")

# Initialize bandwidth measurement variables
start_time = time.time()
total_data_sent = 0

desired_upload = 2
frame_count = 0
frame_skip_interval = 1
buffer = 1

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

    if frame_count % frame_skip_interval == 0:
        # Send the encoded frame to the client using ZeroMQ PUB-SUB pattern
        socket.send(encoded_data)

        # Calculate data sent per second
        elapsed_time = time.time() - start_time
        if elapsed_time >= 1.0:
            data_sent_per_second = (total_data_sent * 8) / (elapsed_time * 1000000)  # Convert to Mbps
            print(f'[SERVER] Data sent per second: {data_sent_per_second:.2f} Mbps')
            start_time = time.time()
            total_data_sent = 0

           # data_sent_difference = abs(data_sent_per_second - desired_upload)
           # increaseIntervel_data_sent_difference = abs(1 / (frame_skip_interval + 1) * data_sent_per_second - desired_upload)
           # decreaseInterval_data_sent_difference = abs(1 / max(1, (frame_skip_interval - 1)) * data_sent_per_second - desired_upload)

          #  print(data_sent_difference, increaseIntervel_data_sent_difference, decreaseInterval_data_sent_difference)

            if abs(desired_upload - data_sent_per_second) < buffer:
                frame_skip_interval += 0
            elif data_sent_per_second > desired_upload:
                frame_skip_interval += 1
            elif data_sent_per_second < desired_upload and frame_skip_interval > 1:
                frame_skip_interval -= 1


            print("[SERVER] Frame skip interval:", frame_skip_interval)
            print("[SERVER] FPS:", fps / frame_skip_interval)
            print("")

        else:
            total_data_sent += len(encoded_data)

    frame_count += 1





    if frame_count >= frame_skip_interval:
        frame_count = 0

    # Receive keys
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

# Release the resources
vid.release()
cv2.destroyAllWindows()
