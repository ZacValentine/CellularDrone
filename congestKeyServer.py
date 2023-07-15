import socket
import keyboard

BUFF_SIZE = 100
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
host_ip = '100.80.57.27'
port = 5001
socket_address = (host_ip, port)
server_socket.bind(socket_address)
print('listening at:', socket_address)

while True:
    try:
        # get client addr from msg
        msg, client_addr = server_socket.recvfrom(BUFF_SIZE)
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
            keys = ''.join([key for key, value in key_state.items() if value])
            # send keys
            server_socket.sendto(keys.encode('utf-8'), client_addr)
    except socket.error as e:
        print(f"Socket error: {e}")
        # Handle the error condition appropriately, e.g., break the loop, raise an exception, or perform cleanup actions.
        break
    except Exception as e:
        print(f"Error: {e}")
        # Handle other exceptions as needed.
        # For example, you could continue the loop, perform cleanup actions, or log the error.

# Clean up and close the socket
server_socket.close()
