# Force reload libraries for development purposes
import sys
if 'pupremote' in sys.modules:
    del sys.modules['pupremote']
if 'lpf2' in sys.modules:
    del sys.modules['lpf2']

from pupremote import PUPRemoteSensor, ESP32, SPIKE_ULTRASONIC


def msg(txt):
    print(txt)
    return txt+txt

def num(n):
    print(n)
    return 2*n

p=PUPRemoteSensor(sensor_id=SPIKE_ULTRASONIC, platform=ESP32)
p.add_command('msg',"repr","repr")
p.add_command('num',from_hub_fmt="b", to_hub_fmt="b")

while(True):
    connected=p.process()