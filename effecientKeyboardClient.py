import socket
import keyboard
import RPi.GPIO as gpio

gpio.setmode(gpio.BCM)
gpio.setwarnings(False)

class Motor:
    def __init__(self, Ena, In1, In2):
        self.Ena = Ena
        self.In1 = In1
        self.In2 = In2
        gpio.setup(self.Ena, gpio.OUT)
        gpio.setup(self.In1, gpio.OUT)
        gpio.setup(self.In2, gpio.OUT)
        self.pwm = gpio.PWM(self.Ena, 100)
        self.pwm.start(0)
    
    def forward(self, speed=100):
        gpio.output(self.In1, gpio.HIGH)
        gpio.output(self.In2, gpio.LOW)
        self.pwm.ChangeDutyCycle(speed)
    
    def backward(self, speed=100):
        gpio.output(self.In1, gpio.LOW)
        gpio.output(self.In2, gpio.HIGH)
        self.pwm.ChangeDutyCycle(speed)
    
    def stop(self):
        self.pwm.ChangeDutyCycle(0)

rightMotor = Motor(25, 23, 24)
leftMotor = Motor(27, 17, 22)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('100.80.57.27', 5000))
print("Connection established")

while True:
    if keyboard.is_pressed('w'):
        message = "w"
        leftMotor.forward(100)
        rightMotor.forward(100)
    elif keyboard.is_pressed('s'):
        message = "s"
        leftMotor.backward(100)
        rightMotor.backward(100)
    elif keyboard.is_pressed('d'):
        message = "d"
        leftMotor.forward(100)
        rightMotor.stop()
    elif keyboard.is_pressed('a'):
        message = "a"
        rightMotor.forward(100)
        leftMotor.stop()
    else:
        message = "x"
        leftMotor.stop()
        rightMotor.stop()

    s.send(bytes(message, "utf-8"))

s.close()
