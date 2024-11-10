# Copy this file to OpenMV Cam H7 Plus or LMS-ESP32
# Be sure to also copy pupremote.py and lpf2.py to the device

### Setup pupremote code
from pupremote import PUPRemoteSensor

def msg(txt):
    print(txt)
    return txt+txt

def num(n):
    print(n)
    return 2*n

# Define our emulated sensor, ultrasonic by default.
# power=True is needed for OpenMV RT. H7 can go without power, 
# but it's a good idea to turn it on for displays and other shields.
p=PUPRemoteSensor(power=False)

# Send and receive any object with 'repr' encoding
p.add_command('msg',"repr","repr")

# Send and receive a signed byte with 'b'
# See https://docs.python.org/3/library/struct.html#format-characters
p.add_command('num',from_hub_fmt="b", to_hub_fmt="b")

# Do no execute procedures, but only present new data to hub
p.add_channel('one_w', to_hub_fmt="bbb")

### End of pupremote setup code

### Main loop
cntd=False
while(True):
    # Add more sensor processing code here
    # ....
    p.update_channel('one_w', 1,2,3)
    # Try to connect, send data and return the connected state.
    cntd=p.process()
    # cntd is True if connected

