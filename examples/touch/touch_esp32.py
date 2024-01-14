from machine import TouchPad, Pin
import time
from pupremote import  PUPRemoteSensor, SPIKE_ULTRASONIC

def touch():
    touch_values=[]
    for touch_pin in touch_pins:
        try:
            # returns a 1 if touch below threshold of 300, otherwise 0
            touch_values.append(1 if touch_pin.read()<300 else 0)
        except Exception as e:
            touch_values.append(1)
            print("error",e)
    return touch_values

p=PUPRemoteSensor(sensor_id=SPIKE_ULTRASONIC)
# return 10 button values
p.add_command('touch','10B')

# define all touch pins
touch_pins = [TouchPad(Pin(i, mode=Pin.IN)) for i in [0,2,4,12,13,14,15,27,32,33]]
while True:
    _=p.process()
    time.sleep_ms(50)
