# Copy this file to the LMS-ESP32 with Thonny and name it main.py
# Copy pupremote.py and lpf2.py to the LMS-ESP32 with Thonny
# Connect the LMS-ESP32 to the SPIKE Prime hub though port A
# Run this program on the LMS-ESP32 by rebooting it (ctrl-D in Thonny)


### Setup pupremote code
from pupremote import  PUPRemoteSensor, SPIKE_ULTRASONIC

message = ""
def msg(*argv):
    if argv!=():
        global message
        print(argv)
        message = argv
    return message


values = (0,0,0)
def three_bytes(*argv):
    if argv!=():
        global values
        print(argv)
        values = argv
    return values

s = 0
def sweep():
    global s
    s+=1
    if s > 255:
        s = 0
    return s

def ub(*argv):
    return three_bytes(*argv)

def sb(*argv):
    return three_bytes(*argv)


sdata=tuple(range(16))
def sm_data(*argv):
    global sdata
    if argv!=():
        print(argv)
        sdata = argv
    #else:
    #    print("smalldata() called without args")
    return sdata


# 32 bytes crashes the connection somehow.
ldata=tuple(range(32))
def lg_data(*argv):
    global ldata
    if argv!=():
        print(argv)
        ldata = argv
    #else:
    #    print("largedata() called without args")
    
    return ldata


p=PUPRemoteSensor(sensor_id=SPIKE_ULTRASONIC)
### Demo commands
# Send anything smaller than 32 bytes and get it back
p.add_command('msg',"repr","repr")

# Send 4 unsigned bytes and read them back
p.add_command('ub',from_hub_fmt="4B",to_hub_fmt="4B")

# Send 4 signed bytes and read them back
p.add_command('sb',from_hub_fmt="4b",to_hub_fmt="4b")

# All values of a byte
p.add_command('sweep',to_hub_fmt="B")

# Send 16 bytes and get them back
p.add_command('sm_data',from_hub_fmt="16B", to_hub_fmt="16B")

# Send 32 bytes and get them back
p.add_command('lg_data',from_hub_fmt="32B", to_hub_fmt="32B")
### End of pupremote setup code

### Main loop
while(True):
    connected=p.process()



