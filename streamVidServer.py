import socket
from vidgear.gears import CamGear


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
    while True:
        # Open video stream using VidGear
        stream = CamGear(source=0).start()

        while True:
            # Read frames from the video stream
            frame = stream.read()

            # Convert the frame to bytes
            frame_bytes = frame.tobytes()

            # Send the frame size to the client
            client_socket.sendall(len(frame_bytes).to_bytes(4, byteorder='big'))

            # Send the frame to the client
            client_socket.sendall(frame_bytes)
