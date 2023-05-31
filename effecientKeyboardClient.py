import socket
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

key_state = {
    'w': False,
    's': False,
    'd': False,
    'a': False
}

while True:
    data = s.recv(16)
    if not data:
        break

    message = data.decode("utf-8")
    message = message[0]
    print(message)

    if message == "w":
        key_state['w'] = True
    elif message == "s":
        key_state['s'] = True
    elif message == "d":
        key_state['d'] = True
    elif message == "a":
        key_state['a'] = True
    elif message == "x":
        key_state = {
            'w': False,
            's': False,
            'd': False,
            'a': False
        }

    if not key_state['w'] and not key_state['s']:
        leftMotor.stop()
        rightMotor.stop()
    elif key_state['w']:
        leftMotor.forward(100)
        rightMotor.forward(100)
    elif key_state['s']:
        leftMotor.backward(100)
        rightMotor.backward(100)

s.close()
