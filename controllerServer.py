import pygame
import socket
import base64

pygame.joystick.init()
pygame.init()
screen = pygame.display.set_mode([240, 160])
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
for i in range(pygame.joystick.get_count()):
    joysticks.append(pygame.joystick.Joystick(i))
    joysticks[-1].init()
    #axis 0 is left and right
    #axis 1 is up and down
    #joysticks[0] is xbox controller

#while True:
    #for event in pygame.event.get():
     #  if event.type == pygame.JOYAXISMOTION:
      #      if(pygame.joystick.Joystick(0).get_axis(1) > 0.1 or pygame.joystick.Joystick(0).get_axis(1) < -0.1):
       #         print("leftMotor: ", pygame.joystick.Joystick(0).get_axis(1) * 100)
       #     else:
         #       print("leftMotor: no input")
          #  if(pygame.joystick.Joystick(0).get_axis(3) > 0.1 or pygame.joystick.Joystick(0).get_axis(3) < -0.1):
           #     print("rightMotor: ", pygame.joystick.Joystick(0).get_axis(3) * 100)
           # else:
                #print("rightMotor: no input")



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 5000))
s.listen(5)

#print(pygame.joystick.Joystick(1).get_name())
while True:
    clientsocket, address = s.accept()
    print(f"connection from {address} has been established")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                if (pygame.joystick.Joystick(0).get_axis(1) > 0.1):
                    message = str(pygame.joystick.Joystick(0).get_axis(1) * 100)
                    message = message[0:4]
                    print(message)
                    message1 = message
                   # clientsocket.send(bytes(message, "utf-8"))
                elif(pygame.joystick.Joystick(0).get_axis(1) < 0.1):
                    message = str(pygame.joystick.Joystick(0).get_axis(1) * 100)
                    message = message[0:4]
                    print(message)
                    message1 = message
                    #clientsocket.send(bytes(message, "utf-8"))
                else:
                    message = str(0)
                    print(message)
                    message1 = message
                    #clientsocket.send(bytes(message, "utf-8"))
                if (pygame.joystick.Joystick(0).get_axis(3) > 0.1):
                    message = str(pygame.joystick.Joystick(0).get_axis(3) * 100)
                    message = message[0:4]
                    print(message)
                    message2 = message
                    #clientsocket.send(bytes(message, "utf-8"))
                elif(pygame.joystick.Joystick(0).get_axis(3) < -0.1):
                    message = str(pygame.joystick.Joystick(0).get_axis(3) * 100)
                    message = message[0:4]
                    print(message)
                    message2 = message
                    #clientsocket.send(bytes(message, "utf-8"))
                else:
                    message = str(0)
                    print(message)
                    message2 = message
                    #clientsocket.send(bytes(message, "utf-8"))


                message3 = message1 + message2
                clientsocket.send(bytes(message3, "utf-8"))
