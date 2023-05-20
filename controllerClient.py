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
s.connect(('192.168.1.17', 1234))
while True:
    msg = s.recv(16)
    data = msg.decode("utf-8")
    print(data)
    
    try:
        leftInput = float(data[:4])
        rightInput = float(data[4:8])
        leftInput = int(leftInput)
        rightInput = int(rightInput)
    except:
        leftInput = 0
        rightInput = 0
        
    

    
    
    print("leftInput: ", leftInput)
    print("rightInput: ", rightInput)
    
    if(leftInput > 0 and leftInput <= 100):
        leftMotor.backward(abs(leftInput))
    elif(leftInput < 0 and leftInput >= -100):
        leftMotor.forward(abs(leftInput))
    else:
        leftMotor.stop()
            
    if(rightInput > 0 and rightInput <= 100):
        rightMotor.backward(abs(rightInput))
    elif(rightInput < 0 and rightInput >= -100):
        rightMotor.forward(abs(rightInput))
    else:
        rightMotor.stop()
    
    
        

