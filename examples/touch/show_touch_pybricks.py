# Program to get all 10 touch pins readings from the LMS-ESP32 and show their values on the 5x5 matrix display
# use show_touch_esp32.py on the LMS-ESP32

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
    touch=p.call('touch')
    for it,t in enumerate(touch):
        # map each touch sensor to a pixel on the display
        x=it//5 
        y=it%5
        hub.display.pixel(x,y,100-t//3)
    print(touch)
    wait(100)
