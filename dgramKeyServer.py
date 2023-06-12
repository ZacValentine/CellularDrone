import socket
import keyboard




BUFF_SIZE = 65536
#BUFF_SIZE = 35536
SML_BUFF_SIZE = 1000
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
host_ip = '100.80.57.27'
port = 5001
socket_address = (host_ip, port)
server_socket.bind(socket_address)
print('listening at:', socket_address)

while True:
    # get client addr from msg
    msg, client_addr = server_socket.recvfrom(SML_BUFF_SIZE)
    print('got connection from', client_addr)

    while True:
        # track key press
        key_state = {
            'w': keyboard.is_pressed('w'),
            's': keyboard.is_pressed('s'),
            'd': keyboard.is_pressed('d'),
            'a': keyboard.is_pressed('a')
        }
        # keys to str
        keys = f"{''.join([key for key, value in key_state.items() if value])}"
        # send keys
        server_socket.sendto(keys.encode('utf-8'), client_addr)
