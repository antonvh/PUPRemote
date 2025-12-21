# Copy this file to the LMS-ESP32 with Thonny or ViperIDE and name it main.py
# Connect the LMS-ESP32 to the SPIKE Prime hub though port A
# Run this program on the LMS-ESP32 by rebooting it (ctrl-D)

### Setup pupremote code
from pupremote import  PUPRemoteSensor, SPIKE_ULTRASONIC

def msg(*argv):
    if argv!=():
        print(*argv)
    return argv

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
def sdata(*argv):
    global sm_data
    if argv!=():
        print(argv)
        sm_data = argv
    else:
        print("smalldata() called without args")
    return sm_data


p=PUPRemoteSensor(power = True, max_packet_size=16)
p.add_command('msg',"repr","repr")
p.add_command('num',from_hub_fmt="3b", to_hub_fmt="3b")
p.add_command('sdata',from_hub_fmt="16B", to_hub_fmt="16B")


### Main loop
while(True):
    connected=p.process()



