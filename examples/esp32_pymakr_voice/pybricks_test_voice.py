from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch
from pybricks.iodevices import PUPDevice
from pupremote import PUPRemoteHub


p=PUPRemoteHub(Port.A)


p.add_command('listen', to_hub_fmt="b")

while 1:
    ans = p.call('listen')
    if ans > 0:
        if ans == 22:
            print('Fwd')
        elif ans == 2:
            print('OK')
        else:
            print( ans )
        # Wait until something new is said, avoid doubles.
        wait(500)
