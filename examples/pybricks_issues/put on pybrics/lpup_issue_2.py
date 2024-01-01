from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.tools import wait, StopWatch

# Create a program file pupremote.py with this object
from pupremote import PUPRemoteHub

# Connect LMS-ESP32 to port A
p=PUPRemoteHub(Port.A) 

### Demo commands
# Send anything smaller than 32 bytes and get it back. Mode 0
p.add_command('msg',"repr","repr")

# Send 4 unsigned bytes and read them back. Mode 1
p.add_command('ub',from_hub_fmt="4B",to_hub_fmt="4B")

# Send 4 signed bytes and read them back. Mode 2
p.add_command('sb',from_hub_fmt="4b",to_hub_fmt="4b")

# All values of a byte
p.add_command('sweep',to_hub_fmt="B")

# Send 16 bytes and get them back. Mode 4
p.add_command('sm_data',from_hub_fmt="16B", to_hub_fmt="16B")

# Send 32 bytes and get them back. Mode 5
p.add_command('lg_data',from_hub_fmt="32B", to_hub_fmt="32B")


## Now call the lms-esp32 over lpup to test our commands
### ISSUE 2: It seems that pybricks only *writes* the first 7 bits of a byte

# Unsigned bytes can represent 128, but not -10
# Expecting to get (1, 2, 246, 128)
print("\nPybricks hubs only send 7 bytes on mode write")
data = (1, 2, -10, 128)
answer = p.call('ub', *data)
print('Sent:', data, '\nGot:', answer)

# Signed bytes can represent -10, but not 128
# Expecting to get (1, 2, -10, -127)
data = (1, 2, -10, 128)
answer = p.call('sb', *data)
print('\nSent:', data, '\nGot:', answer)

# This arrives as b'}~\x7f\x7f' (or ['7d', '7e', '7f', '7f']) :((
p.pup_device.write(1, tuple(b'\x7d\x7e\x7f\x80'))

# *Reading* all 8 bits is no problem, however
tgt_values = list(range(256))
print("\nReading all possible byte values... [0,1, ... ,255]")
for i in range(500):
    n = p.call('sweep')
    wait(10)
    if n in tgt_values:
        tgt_values.pop(tgt_values.index(n))
print('\nBy now this list should be empty:', tgt_values)