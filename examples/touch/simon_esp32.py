from machine import TouchPad, Pin
import time
from pupremote import  PUPRemoteSensor, SPIKE_ULTRASONIC

TRESHOLD=380 # when non connectd to 5v
#TRESHOLD=300 # when connected to 5V
def touch():
    global TRESHOLD
    touch_value=0
    for i,touch_pin in enumerate(touch_pins):
        try:
            touch_value+=(2**i if touch_pin.read()<TRESHOLD else 0)
        except Exception as e:
            pass
            print("error",e)
    return touch_value

def val():
    v=[]
    for p in [3,4,5,6]:
        try:
            v.append(touch_pins[p].read())
        except:
            v.append(0)
    return v

def tresh(*argv):
    global TRESHOLD
    if argv!=():
        print(argv)
        print("set threshold to",argv[0])
        TRESHOLD=argv[0]
    return TRESHOLD

p=PUPRemoteSensor(sensor_id=SPIKE_ULTRASONIC)
p.add_command('touch','H')
p.add_command('val','4H')
p.add_command('tresh','H','H')
touch_pins = [TouchPad(Pin(i, mode=Pin.IN)) for i in [0,2,4,12,13,14,15,27,32,33]]
while True:
    _=p.process()
    time.sleep_ms(50)
