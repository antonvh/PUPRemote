from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

from bluepad import BluePad



_bp = None
_nintendo = False
lx, ly, rx, ry, btns, dpad = [None] * 6

def bp_init(port_letter,nintendo=True):
    global _bp
    global _nintendo
    port = eval('Port.' + port_letter)
    _bp = BluePad(port)
    _nintendo = nintendo

def gamepad():
    global lx, ly, rx, ry, btns, dpad
    lx, ly, rx, ry, btns, dpad = _bp.gamepad()

def lpad_x():
    return lx

def lpad_y():
    return ly

def rpad_x():
    return rx

def rpad_y():
    return ry

def btns():
    return _bp.btns_pressed(btns,_nintendo)

def dpad():
    return _bp.dpad_pressed(dpad,_nintendo)

def neopixel_init(nr_leds,pin):
    _bp.neopixel_init(nr_leds,pin)

def neopixel_fill(r,g,b,write=True):
    _bp.neopixel_fill((r,g,b),write=write)

def neopixel_zero(write=True):
    _bp.neopixel_zero(write=write)

def neopixel_set(led_nr,r,g,b,write=True):
    _bp.neopixel_set(led_nr,(r,g,b),write=True)

def servo(servo_nr,pos):
    _bp.servo(servo_nr,pos)