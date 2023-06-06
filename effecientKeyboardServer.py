import socket
import keyboard

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 5001))
s.listen(5)

while True:
    client_socket, address = s.accept()

    print("Client connected")

    prev_key_state = {
        'w': False,
        's': False,
        'd': False,
        'a': False
    }

    while True:
        try:
            key_state = {
                'w': keyboard.is_pressed('w'),
                's': keyboard.is_pressed('s'),
                'd': keyboard.is_pressed('d'),
                'a': keyboard.is_pressed('a')
            }

            if key_state != prev_key_state:
                message = ''.join(['1' if key_state[key] else '0' for key in key_state])
                client_socket.sendall(message.encode())

                prev_key_state = key_state
        except Exception as e:
            print("Error:", str(e))
            break

    client_socket.close()

