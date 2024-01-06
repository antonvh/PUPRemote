from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch
from pupremote import PUPRemoteHub

hub = PrimeHub()

pup = PUPRemoteHub(Port.A)
pup.add_command('gmpd',to_hub_fmt="6h")
pup.add_command('conn',to_hub_fmt="B")

while True:
    data=pup.call('gmpd')
    print(data)
    wait(0.1)
