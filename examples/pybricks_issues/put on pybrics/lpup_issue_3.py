from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.tools import wait, StopWatch

# Create a program file pupremote.py with this object
from pupremote import PUPRemoteHub

# Connect LMS-ESP32 to port A
p=PUPRemoteHub(Port.A) 

### Demo commands
# Send anything smaller than 32 bytes and get it back. Mode 0
# Placeholder to keep up the mode count
p.add_command('msg',"repr","repr")

# Send 4 unsigned bytes and read them back. Mode 1
# To crash the hub hard, I intentionally put 3B instead of 
# the 4B defined on the ESP_32
p.add_command('ub',from_hub_fmt="3B",to_hub_fmt="3B")

# BOOM!
print( p.call('ub', 1,2,3) )
