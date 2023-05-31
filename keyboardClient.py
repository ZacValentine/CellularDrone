import cv2, imutils, socket
import numpy as np
import time
import base64
import RPi.GPIO as gpio
import time

gpio.setmode(gpio.BCM)
gpio.setwarnings(False)

class motor():
    def __init__(self, Ena, In1, In2):
        self.Ena = Ena
        self.In1 = In1
        self.In2 = In2
        gpio.setup(self.Ena, gpio.OUT)
        gpio.setup(self.In1, gpio.OUT)
        gpio.setup(self.In2, gpio.OUT)
        self.pwm = gpio.PWM(self.Ena, 100)
        self.pwm.start(0)
    
    def forward(self, speed = 100):
        gpio.output(self.In1, gpio.HIGH)
        gpio.output(self.In2, gpio.LOW)
        self.pwm.ChangeDutyCycle(speed)
    def backward(self, speed = 100):
        gpio.output(self.In1, gpio.LOW)
        gpio.output(self.In2, gpio.HIGH)
        self.pwm.ChangeDutyCycle(speed)
    def stop(self):
        self.pwm.ChangeDutyCycle(0)
rightMotor = motor(25, 23, 24)
leftMotor = motor(27, 17, 22)



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('100.80.57.27', 5001))
print("connection")
while True:
    msg = s.recv(16)
    data = msg.decode("utf-8")
    data = data[0]
    print(data)
    
    if(data == "w"):
       leftMotor.forward(100)
       rightMotor.forward(100)
    elif(data == "s"):
       leftMotor.backward(100)
       rightMotor.backward(100)
    elif(data == "d"):
       leftMotor.forward(100)
       rightMotor.stop()
    elif(data == "a"):
       rightMotor.forward(100)
       leftMotor.stop()
    elif(data == "x"):
        leftMotor.stop()
        rightMotor.stop()

    
