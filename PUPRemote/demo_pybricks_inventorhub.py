from pybricks.hubs import InventorHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch
from pybricks.iodevices import PUPDevice


hub = InventorHub()

from pupremote import *

p=PUPRemoteHub(Port.A)
p.add_command('rgb','BBB','BBB')
p.add_command('gyro','8B','8B')
print('gyro:',p.read('gyro'))
p.write('gyro',*[i for i in range(8)])
p.write('rgb',5,6,7)
for i in range(5):
    print(p.read('rgb'))
    wait(20)