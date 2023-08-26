# Force reload libraries for development purposes
import sys
if 'pupremote' in sys.modules:
    del sys.modules['pupremote']
if 'lpf2' in sys.modules:
    del sys.modules['lpf2']

from pupremote import PUPRemoteSensor, ESP32, SPIKE_ULTRASONIC
from time import sleep_ms
counter = 0

def msg(txt):
    global counter
    counter += 1
    print(txt)
    return txt+txt

def num(n):
    global counter
    counter += 1
    print(n)
    return 2*n

# def cntr():
#     global counter
#     return counter

p=PUPRemoteSensor(sensor_id=SPIKE_ULTRASONIC, platform=ESP32)
p.add_channel('cntr',to_hub_fmt="b")
p.add_command('msg',"repr","repr")
p.add_command('num',from_hub_fmt="b", to_hub_fmt="b")

while(True):
    connected=p.process()
    p.update_channel('cntr', counter)
    sleep_ms(20)
