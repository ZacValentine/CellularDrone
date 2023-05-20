import socket

HOST = '100.80.57.27'  # all available interfaces
PORT = 5000  # arbitrary non-privileged port

# create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)



try:
    # bind the socket to a public host, and a well-known port
    server_socket.bind((HOST, PORT))
except OSError as e:
    print(f"Error binding to {HOST}:{PORT}: {e}")
    server_socket.close()
    exit()

# become a server socket
server_socket.listen(1)

print(f'Server listening on {HOST}:{PORT}')

while True:
    # accept connections from outside
    try:
        (client_socket, client_address) = server_socket.accept()
        print(f'Incoming connection from {client_address[0]}:{client_address[1]}')
    except KeyboardInterrupt:
        # allow the server to be stopped by pressing CTRL-C
        print("Server stopped")
        server_socket.close()
        exit()
    except:
        print("Error accepting incoming connection")
        continue

    # receive data from client
    try:
        data = client_socket.recv(1024).decode()
        print(f'Received: {data}')
    except:
        print("Error receiving data from client")
        continue

    # send response to client
    response = 'Hello from server!'
    client_socket.sendall(response.encode())

    # close the client connection
    client_socket.close()
    # close the client connection
    client_socket.close()
# close the connection
client_socket.close()
