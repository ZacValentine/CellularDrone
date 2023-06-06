import socket
import psutil
from vidgear.gears import CamGear
import time

# Server IP address and port
SERVER_IP = '100.80.57.27'
SERVER_PORT = 5000

def send_video_stream(client_socket, client_address):
    try:
        # Open video stream using VidGear
        stream = CamGear(source=0).start()

        # Bandwidth measurement variables
        bytes_sent = 0
        start_time = time.time()

        while True:
            # Read frames from the video stream
            frame = stream.read()

            # Convert the frame to bytes
            frame_bytes = frame.tobytes()

            # Send the frame size to the client
            client_socket.sendall(len(frame_bytes).to_bytes(4, byteorder='big'))

            # Send the frame to the client
            client_socket.sendall(frame_bytes)

            # Update the bytes_sent counter
            bytes_sent += len(frame_bytes)

            # Calculate the elapsed time
            elapsed_time = time.time() - start_time

            # Check if 1 second has elapsed
            if elapsed_time >= 1:
                # Calculate the bandwidth in Mbps
                bandwidth = (bytes_sent * 8) / elapsed_time / 1e6

                print(f"[SERVER] Bandwidth: {bandwidth:.2f} Mbps")

                # Reset the counters
                bytes_sent = 0
                start_time = time.time()

    except Exception as e:
        print(f'[SERVER] Error: {str(e)}')

    finally:
        # Stop the video stream and close the client socket
        stream.stop()
        client_socket.close()

# Create a TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the server IP address and port
server_socket.bind((SERVER_IP, SERVER_PORT))

# Listen for incoming connections
server_socket.listen(1)
print('[SERVER] Waiting for client connection...')

while True:
    # Accept a client connection
    client_socket, client_address = server_socket.accept()
    print(f'[SERVER] Client connected: {client_address}')

    # Start sending video stream to the client
    send_video_stream(client_socket, client_address)
