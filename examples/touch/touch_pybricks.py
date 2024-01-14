from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch
from pupremote import PUPRemoteHub

hub = PrimeHub()
hub.display.off()
p=PUPRemoteHub(Port.A)
p.add_command('touch','10B')

while True:
    buttons=p.call('touch')
    print(buttons)
    for i,b in enumerate(buttons):
        # light pixel on row, column when button is touched
        r=i%5
        c=i//5
        hub.display.pixel(r,c,b*100)
    wait(20)
