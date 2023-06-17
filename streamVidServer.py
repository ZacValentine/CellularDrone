import socket
import cv2
import imutils
import zlib
import base64

# Server IP address and port
host_ip = '100.80.57.27'
port = 5000

# Create a TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the server IP address and port
server_socket.bind((host_ip, port))

# Listen for incoming connections
server_socket.listen(1)
print('[SERVER] Waiting for client connection...')

while True:
    # Accept a client connection
    client_socket, client_address = server_socket.accept()
    print(f'[SERVER] Client connected: {client_address}')

    # Start sending video stream to the client
    vid = cv2.VideoCapture(0)
    WIDTH = 400

    while True:
        # Get frame
        _, frame = vid.read()
        # Resize frame
        frame = imutils.resize(frame, width=WIDTH)

        # Compress the frame
        _, compressed_frame = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
        compressed_data = zlib.compress(compressed_frame)
        encoded_data = base64.b64encode(compressed_data)

        # Send the frame size to the client
        frame_size = len(encoded_data)
        client_socket.sendall(frame_size.to_bytes(4, byteorder='big'))

        # Send the encoded frame to the client
        client_socket.sendall(encoded_data)

        # Receive keys
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            server_socket.close()
            break

    # Release the resources
    vid.release()
    cv2.destroyAllWindows()
