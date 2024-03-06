# Program to read all 10 touch pins and communicate their values to the hub
# use show_touch_pybbricks.py on the hub

from machine import TouchPad, Pin
import time
from pupremote import  PUPRemoteSensor, SPIKE_ULTRASONIC

def touch():
    v=[]
    for p in touch_pins: # loop over all touch pins
        try:
            v.append(p.read()//4) # reduce value from max 1024 to max 255
        except:
            v.append(0)
    return v

p=PUPRemoteSensor(sensor_id=SPIKE_ULTRASONIC)
p.add_command('touch','10B') # returns 10 bytes with each byte representing the touch value//4

# initialize all possible touch pins
touch_pins = [TouchPad(Pin(i, mode=Pin.IN)) for i in [0,2,4,12,13,14,15,27,32,33]]
while True:
    _=p.process()
    time.sleep_ms(30)
