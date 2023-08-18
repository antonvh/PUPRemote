# Copy this file to OpenMV Cam H7 Plus
# Be sure to also copy pupremote.py and lpf2.py to the camera drive

### Setup pupremote code
from pupremote import PUPRemoteSensor, OPENMV, SPIKE_ULTRASONIC

def msg(txt):
    print(txt)
    return txt+txt

def num(n):
    print(n)
    return 2*n

p=PUPRemoteSensor(sensor_id=SPIKE_ULTRASONIC, platform=OPENMV)
p.add_command('msg',"repr","repr")
p.add_command('num',from_hub_fmt="b", to_hub_fmt="b")
### End of pupremote setup code

### Main loop
while(True):
    connected=p.process()
