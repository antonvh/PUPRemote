# This robot uses the OpenMV Cam to track a red ball and drive towards it.
# When it is close enough, it kicks the ball.

from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

hub = PrimeHub()

from pupremote import PUPRemoteHub

p=PUPRemoteHub(Port.A)
p.add_command('get_blob','hhh')

lm = Motor(Port.C)
rm = Motor(Port.D, Direction.COUNTERCLOCKWISE)
kick = Motor(Port.B)
db=DriveBase(lm, rm, 56, 120)

CLOSE_BLOB_PIXELS = 11000

while 1:
    # Get x (0= right, 300= left), y (0=bottom, 220=top), num_pixels
    x, y, num_pixels = p.call('get_blob')
    # print('blob:', x, y, num_pixels)
    if 0 < num_pixels < CLOSE_BLOB_PIXELS:
        db.drive(max((CLOSE_BLOB_PIXELS-num_pixels)*.05, 0), (150-x)*-.8)
    elif num_pixels >= CLOSE_BLOB_PIXELS:
        kick.dc(-100)
        wait(70)
        kick.run_target(500,45)
    else:
        db.drive(0,50)

