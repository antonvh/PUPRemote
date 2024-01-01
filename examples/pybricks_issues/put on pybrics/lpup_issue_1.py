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
### ISSUE 1: msg is hit and miss: it is 32 bytes always (max official frame size)
# sometimes the checksum fails because Pybricks mangles the last
# few bytes on a 32 bytes mode write(). There seems to be a buffer
# overflow becauase the last 2-3 bytes are often identical to the
# first byte of the received mode data.
print('\n--- starting lpup comms test ---')
data = 'hello from the hub' # a string
answer = p.call('msg', data)
print('\nSent:', data, '\nGot:', answer)

data = {1:[2,3], 'b':[7]} # an arbitray python object
answer = p.call('msg', data)
print('\nSent:', data, 'of len', len(repr(data)), '\nGot:', answer, type(answer))

print("\nSending string and dict reprs alternatingly")
hits=0
misses=0
tries = 10
for i in range(tries):
    data = 'hello from the hub'
    answer = p.call('msg', data)
    if data == answer: 
        hits += 1
    else:
        misses += 1

    data = {1:[2,3], 'b':[7]}
    answer = p.call('msg', data)
    if data == answer: 
        hits += 1
    else:
        misses += 1

print(hits, 'hits, ', misses, 'misses in', tries*2, 'tries of "msg"')

# Another demo of the buffer issue
# Sending 16 bytes goes flawless
hits=0
misses=0
tries = 20
print("\nSending 16 bytes across for",tries,"tries")
for i in range(tries):
    data = tuple(range(i,i+16))
    answer = p.call('sm_data', *data)
    if data == answer: 
        hits += 1
    else:
        print(data,answer)
        misses += 1
print(hits, 'hits, ', misses, 'misses in', tries, 'tries of "sm_data"')

# Sending 32 bytes is problematic
# Not only does the checksum fail as buffers collide, but
# doing this fast and often can also eliminate the heartbeat and lead to a 
# disconnect with more than 10 tries.
hits=0
misses=0
tries = 10
print("\nSending 32 bytes across for",tries,"tries")
for i in range(tries):
    data = tuple(range(i,i+32))
    answer = p.call('lg_data', *data)
    if data == answer: 
        hits += 1
    else:
        misses += 1
print(hits, 'hits, ', misses, 'misses in', tries, 'tries of "lg_data"')


