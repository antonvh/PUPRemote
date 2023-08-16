from pybricks.hubs import TechnicHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

hub = TechnicHub()

from pupremote import *

p=PUPRemoteHub(Port.A)
p.add_command('rgb','BBB','BBB')
p.add_command('gyroscoop','8B','8B')
print('gyro:',p.call('gyroscoop'))
p.call('set_gyroscoop',*[i for i in range(8)])
p.call('set_rgb',5,6,7)
for i in range(5):
    print(p.call('rgb'))
    wait(20)
