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

p=PUPRemoteSensor(sensor_id=SPIKE_ULTRASONIC)
p.add_command('msg',"repr","repr")
p.add_command('num',from_hub_fmt="3b", to_hub_fmt="3b")
### End of pupremote setup code

### Main loop
while(True):
    connected=p.process()
    value+=1

