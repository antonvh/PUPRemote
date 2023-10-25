# Copy this file to OpenMV Cam H7 Plus
# Be sure to also copy pupremote.py and lpf2.py to the camera drive

### Setup pupremote code
from pupremote import  PUPRemoteSensor, SPIKE_ULTRASONIC
value=1
def msg(*argv):
    if argv!=():
        print(argv)
    return str(value)

def num(*argv):
    if argv!=():
        print(argv)
    return 2*value,3*value,4*value

def smalldata(*argv):
    if argv!=():
        print(argv)
    
    return 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16

def largedata(*argv):
    if argv!=():
        print(argv)
    
    return 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,\
           1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16


p=PUPRemoteSensor(sensor_id=SPIKE_ULTRASONIC)
p.add_command('msg',"repr","repr")
p.add_command('num',from_hub_fmt="3b", to_hub_fmt="3b")
p.add_command('smalldata',from_hub_fmt="16b", to_hub_fmt="16b")
p.add_command('largedata',from_hub_fmt="32b", to_hub_fmt="32b")
### End of pupremote setup code

### Main loop
while(True):
    connected=p.process()
    value+=1



