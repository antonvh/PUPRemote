# Copy the contents of this file to a new Pybricks project on the hub side.
# Copy the contents of pupremote.py to a new Pybricks project with EXACTLY the name pupremote.py

# Connect the LMS-ESP32 to port A of the hub.

from pybricks.hubs import InventorHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

hub = InventorHub()

from pupremote import PUPRemoteHub

p=PUPRemoteHub(Port.A)
p.add_command('rgb','BBB','BBB')
p.add_command('gyroscoop','8B','8B')
print('gyro:',p.call('gyroscoop'))
p.call('set_gyroscoop',*[i for i in range(8)])
p.call('set_rgb',5,6,7)
for i in range(5):
    print(p.call('rgb'))
    wait(20)