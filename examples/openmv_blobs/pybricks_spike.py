# Copy the contents of this file into a new Pybricks project on the hub side.

from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

from pupremote import PUPRemoteHub

p=PUPRemoteHub(Port.A)
p.add_command('get_blob','hhh')
p.add_command('msg',"repr","repr")
p.add_command('num',from_hub_fmt="b",to_hub_fmt="b")

print('blob:',p.call('get_blob'))

# Print something on the openmv console
print(p.call('msg','hello'))
print(p.call('num',45))
print(p.call('num',42))

for i in range(10):
    # Get x (0= right, 300= left), y (0=bottom, 220=top), num_pixels
    x, y, num_pixels = p.call('get_blob')
    print('blob:', x, y, num_pixels)
