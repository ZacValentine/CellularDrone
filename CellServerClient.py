import socket

HOST = '100.80.57.27'  # server IP address or hostname
PORT = 5000                # same arbitrary non-privileged port

# create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect the client socket to the server
client_socket.connect((HOST, PORT))

# send data to server
message = 'Hello from client!'
client_socket.sendall(message.encode())

# receive response from server
response = client_socket.recv(1024).decode()
print('Received: {}'.format(response))

# close the socket
client_socket.close()
