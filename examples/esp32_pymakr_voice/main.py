# # Force reload libraries for development purposes
import sys
if 'pupremote' in sys.modules:
    del sys.modules['pupremote']
if 'lpf2' in sys.modules:
    del sys.modules['lpf2']

from pupremote import PUPRemoteSensor, ESP32, SPIKE_ULTRASONIC
from sens0539 import SENS0539, CMD_IDS
from time import sleep_ms
s=SENS0539()

def listen():
    id = s.get_cmd_id()
    if id in CMD_IDS:
        print(CMD_IDS[id])
    else:
        print('Unknown command ID: %d' % id)

    return id


pr = PUPRemoteSensor(platform=ESP32, sensor_id=SPIKE_ULTRASONIC)
pr.add_command('listen', to_hub_fmt='b')

while(True):
    connected=pr.process()
    sleep_ms(20)