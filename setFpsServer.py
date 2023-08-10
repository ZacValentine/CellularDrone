
# ZMQ/LOWER LATENCY - NO FPS CONTROL - LATENCY INCREASES WHEN UPLOAD IS LOWER THAN MBPS(GETS BACKED UP) - SEEMS TO BE FRAME SKIPPING(10000 WIDTH, ON PC, LOW FPS BUT NO LATENCY INCREASE)

import zmq
import cv2
import imutils
import zlib
import base64
import time
import datetime
from sys import argv

from sensors import temp_sensor

# Server IP address and port
host_ip = '100.110.162.27'
port = 5000

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind(f"tcp://{host_ip}:{port}")

if len(argv) > 1:
	fps = int(argv[1])
	WIDTH = int(argv[2])
else:
	fps = 15
	WIDTH = 200 # 1.7 mbps CONFIRMED
vid = cv2.VideoCapture(0)
vid.set(cv2.CAP_PROP_FPS, fps)

#WIDTH = 800
#WIDTH = 400 # 4.5mbps CONFIRMED
#WIDTH = 200 # 1.7mbps CONFIRMED
#WIDTH = 100 # 0.7mbps CONFIRMED

HEIGHT = int(WIDTH * 0.5625)

print("[SERVER] Server is up. Waiting for client connection...")

# Initialize bandwidth measurement variables
start_time = time.time()
total_data_sent = 0

temp_sensor = temp_sensor()

while True:
    # Get frame
    _, frame = vid.read()
    # Resize frame
    frame = imutils.resize(frame, width=WIDTH, height=HEIGHT)
    
    
    
    # resizing for UI placement
    #MAY CAUSE SLOW DOWN
    #frame = cv2.resize(frame, (1920, 1080))
    
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    cv2.putText(frame, current_time, (5, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    #put sensor data
    cv2.putText(frame, "TEMP: " + str(temp_sensor.getTemp()), (WIDTH - 80, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    #MAY CAUSE SLOW DOWN
    #frame = cv2.resize(frame, (400, 400))
    

    # Compress the frame
    _, compressed_frame = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
    compressed_data = zlib.compress(compressed_frame)
    encoded_data = base64.b64encode(compressed_data)

    # Send the encoded frame to the client using ZeroMQ PUB-SUB pattern
    socket.send(encoded_data)

    # Calculate data sent per second
    elapsed_time = time.time() - start_time
    if elapsed_time >= 1.0:
        data_sent_per_second = (total_data_sent * 8) / (elapsed_time * 1000000)  # Convert to Mbps
        print(f'[SERVER] Data sent per second: {data_sent_per_second:.2f} Mbps')
        start_time = time.time()
        total_data_sent = 0
    else:
        total_data_sent += len(encoded_data)


    # Receive keys
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

# Release the resources
vid.release()
cv2.destroyAllWindows()
