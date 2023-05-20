import socket
import keyboard

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 5000))
s.listen(5)

while True:
    clientsocket, address = s.accept()
    print(f"connection from {address} has been established")

    while True:
        if keyboard.is_pressed('w'):
            #message1 = str(100)
            #message2 = str(100)
            message = "f"
        elif keyboard.is_pressed('s'):
            # message1 = str(-100)
            # message2 = str(-100)
            message = "b"
        elif keyboard.is_pressed('d'):
            # message1 = str(100)
            # message2 = str(0)
            message = "r"
        elif keyboard.is_pressed('a'):
            # message1 = str(0)
            # message2 = str(100)
            message = "l"
        else:
            # message1 = str(0)
            # message2 = str(0)
            message = "s"

        # print(message1, message2)
        # message = message1 + message2

        print(message)
        clientsocket.send(bytes(message, "utf-8"))
