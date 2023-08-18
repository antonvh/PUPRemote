# Copy the contents of this file to main.py on the ESP32 side.
# Copy pupremote.py and lpf2.py to the ESP32 side.
# Use Thonny or Pymakr

from pupremote import PUPRemoteSensor
from utime import ticks_ms

WeDo_Ultrasonic, SPIKE_Color, SPIKE_Ultrasonic = 35, 61, 62

count = 0
def rgb():
    global count
    count+=1
    count%=30
    return count,count*2,count*3

def set_rgb(*argv):
    print("set_rgb",argv)

def gyroscoop():
    resp = [i+1 for i in range(8)]
    return resp

def set_gyroscoop(*argv):
    print('set_gyro',argv)
    
p=PUPRemoteSensor(sensor_id=SPIKE_Ultrasonic)

p.add_command('rgb','BBB','BBB')
p.add_command('gyroscoop','8B','8B')

while True:
    connected=p.process()
