from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

hub = PrimeHub()

from pupremote import PUPRemoteHub
prh=PUPRemoteHub(Port.A)
prh.add_command('led',from_hub_fmt="B", to_hub_fmt="B")
while 1:
    prh.call('led',100)
    wait(3000)
    prh.call('led',0)
    wait(1000)