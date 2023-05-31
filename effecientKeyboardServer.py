import socket
import keyboard
import select

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 5000))
s.listen(5)
s.setblocking(0)

lastKeyPress = ""

while True:
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established")

    while True:
        ready_to_read, _, _ = select.select([clientsocket], [], [], 0)

        if ready_to_read:
            client_data = clientsocket.recv(1024)
            if not client_data:
                break
            print("Received data from the client:", client_data.decode("utf-8"))

        if keyboard.is_pressed('w'):
            message = "w"
        elif keyboard.is_pressed('s'):
            message = "s"
        elif keyboard.is_pressed('d'):
            message = "d"
        elif keyboard.is_pressed('a'):
            message = "a"
        else:
            message = "x"

        if message != lastKeyPress:
            clientsocket.send(bytes(message, "utf-8"))
            lastKeyPress = message

clientsocket.close()
