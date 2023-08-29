# Build a simple robot with wheels on ports C and D
# Connect a voice recognition sensor dfrobot SEN0539 to LMS-ESP32 and then to your hub
# Put the sensor in i2c mode.
# https://wiki.dfrobot.com/SKU_SEN0539-EN_Gravity_Voice_Recognition_Module_I2C_UART

from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch
from pybricks.iodevices import PUPDevice
from pupremote import PUPRemoteHub


p=PUPRemoteHub(Port.A)
lm = Motor(Port.C)
rm = Motor(Port.D, Direction.COUNTERCLOCKWISE)
kick = Motor(Port.B)
db=DriveBase(lm, rm, 56, 120)

p.add_command('listen', to_hub_fmt="b")

while 1:
    ans = p.call('listen')
    if ans > 0:
        if ans == 22:
            print('Fwd')
            db.straight(50)
        elif ans == 23:
            print('Back')
            db.straight(-50)
        elif ans == 25:
            print('Left 90')
            db.turn(-90)
        elif ans == 26:
            print('Left 45')
            db.turn(-45)
        elif ans == 27:
            print('Left 30')
            db.turn(-30)
        elif ans == 28:
            print('Right 90')
            db.turn(90)
        elif ans == 29:
            print('Right 45')
            db.turn(45)
        elif ans == 30:
            print('Right 30')
            db.turn(30)
        elif ans == 2:
            print('OK')
        else:
            print( ans )
        # Wait until something new is said, avoid doubles.
        wait(500)
