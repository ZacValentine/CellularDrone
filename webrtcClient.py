import socket
import cv2
import numpy as np

# Server IP address and port
SERVER_IP = '100.80.57.27'
SERVER_PORT = 5000

# Create a TCP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to the server
    client_socket.connect((SERVER_IP, SERVER_PORT))
    print(f'[CLIENT] Connected to server: {SERVER_IP}:{SERVER_PORT}')

    while True:
        # Receive the frame size from the server
        frame_size_bytes = client_socket.recv(4)
        frame_size = int.from_bytes(frame_size_bytes, byteorder='big')

        # Receive the frame from the server
        frame_bytes = b''
        while len(frame_bytes) < frame_size:
            remaining_bytes = frame_size - len(frame_bytes)
            frame_bytes += client_socket.recv(4096 if remaining_bytes > 4096 else remaining_bytes)

        # Convert the frame from bytes to numpy array
        frame = np.frombuffer(frame_bytes, dtype=np.uint8).reshape((480, 640, 3))

        # Display the frame
        cv2.imshow('Video Stream', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except Exception as e:
    print(f'[CLIENT] Error: {str(e)}')

finally:
    # Close the client socket
    client_socket.close()
    cv2.destroyAllWindows()
