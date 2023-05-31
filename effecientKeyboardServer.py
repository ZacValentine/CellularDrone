import socket
import keyboard

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 5000))
s.listen(5)

lastKeyPress = ""

while True:
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established")

    # Set the client socket to non-blocking mode
    clientsocket.setblocking(0)

    while True:
        try:
            data = clientsocket.recv(16)
            if data:
                message = data.decode("utf-8")
                message = message[0]
                print(message)

                if message == "w":
                    # Perform action for 'w' key
                    pass
                elif message == "s":
                    # Perform action for 's' key
                    pass
                elif message == "d":
                    # Perform action for 'd' key
                    pass
                elif message == "a":
                    # Perform action for 'a' key
                    pass
                elif message == "x":
                    # Perform action for 'x' key
                    pass

                lastKeyPress = message

        except BlockingIOError:
            pass

s.close()
