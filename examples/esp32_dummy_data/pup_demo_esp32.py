# Copy this file to the LMS-ESP32 with Thonny and name it main.py
# Copy pupremote.py and lpf2.py to the LMS-ESP32 with Thonny
# Connect the LMS-ESP32 to the SPIKE Prime hub though port A
# Run this program on the LMS-ESP32 by rebooting it (ctrl-D in Thonny)


### Setup pupremote code
from pupremote import  PUPRemoteSensor, SPIKE_ULTRASONIC

def msg(*argv):
    if argv!=():
        print(argv)
    return str(value)

value=0
def num(*argv):
    global value
    if argv!=():
        print(argv)
    else:
        print("num called without args")
    value += 1
    return 2*value,-3*value,4*value

sm_data=None
def smalldata(*argv):
    global sm_data
    if argv!=():
        print(argv)
        sm_data = argv
    else:
        print("smalldata() called without args")
    return sm_data

# 32 bytes crashes the connection somehow.
lg_data=tuple(range(32))
def largedata(*argv):
    global lg_data
    if argv!=():
        print(argv)
        lg_data = argv
    else:
        print("largedata() called without args")
    
    return lg_data


p=PUPRemoteSensor(sensor_id=SPIKE_ULTRASONIC, power = True)
p.add_command('msg',"repr","repr")
p.add_command('num',from_hub_fmt="3b", to_hub_fmt="3b")
p.add_command('smalldata',from_hub_fmt="16B", to_hub_fmt="16B")
p.add_command('largedata',from_hub_fmt="32B", to_hub_fmt="32B")
### End of pupremote setup code

### Main loop
while(True):
    connected=p.process()



