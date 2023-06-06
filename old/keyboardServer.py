import socket
import keyboard

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 5001))
s.listen(5)

lastKeyPress = ""

while True:
    clientsocket, address = s.accept()
    print(f"connection from {address} has been established")

    while True:
        if keyboard.is_pressed('w'):
            message = "w"

            if(message != lastKeyPress):
                clientsocket.send(bytes(message, "utf-8"))
                lastKeyPress = message
        elif keyboard.is_pressed('s'):
            message = "s"

            if (message != lastKeyPress):
                clientsocket.send(bytes(message, "utf-8"))
                lastKeyPress = message
        elif keyboard.is_pressed('d'):
            message = "d"

            if (message != lastKeyPress):
                clientsocket.send(bytes(message, "utf-8"))
                lastKeyPress = message
        elif keyboard.is_pressed('a'):
            message = "a"

            if (message  != lastKeyPress):
                clientsocket.send(bytes(message, "utf-8"))
                lastKeyPress = message
        else:
             message = "x"

             if (message != lastKeyPress):
                 clientsocket.send(bytes(message, "utf-8"))
                 lastKeyPress = message

