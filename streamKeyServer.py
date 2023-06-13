import socket
import keyboard

BUFF_SIZE = 100
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
host_ip = '100.80.57.27'
port = 5001
socket_address = (host_ip, port)
server_socket.bind(socket_address)
server_socket.listen(1)
print('listening at:', socket_address)

while True:
    # Accept a client connection
    client_socket, client_address = server_socket.accept()
    print('got connection from', client_address)

    while True:
        # Track key press
        key_state = {
            'w': keyboard.is_pressed('w'),
            's': keyboard.is_pressed('s'),
            'd': keyboard.is_pressed('d'),
            'a': keyboard.is_pressed('a')
        }
        # Keys to str
        keys = f"{''.join([key for key, value in key_state.items() if value])}"
        # Send keys
        client_socket.sendall(keys.encode('utf-8'))
