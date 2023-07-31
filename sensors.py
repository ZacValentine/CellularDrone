import psutil
import time
import os

class temp_sensor:
    def __init__(self):
        self.temp = 0
        
    def getTemp(self):
        try:
            with open('/sys/class/thermal/thermal_zone0/temp', 'r') as temp_file:
                temp_str = temp_file.read().strip()
                temp = float(temp_str) / 1000.0
                return temp
        except:
            return "N/A"
        
temp_sensor = temp_sensor()
while True:
    print(temp_sensor.getTemp())
    time.sleep(1)    


