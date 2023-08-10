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
