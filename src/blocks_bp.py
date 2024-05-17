__author__ = "Anton Vanhoucke & Ste7an"
__copyright__ = "Copyright 2023, AntonsMindstorms.com"
__license__ = "GPL"
__version__ = "0.1"
__status__ = "Beta"

# DEPRECATED. Just import blocks from bluepad.py








# This code is a wrapper around the methods of the BluePad class, so that these methods can be used from Blocks PyBricks.

from pybricks.parameters import Port
from bluepad import BluePad

# define global vraiables to store Bluepad objects
_bp = None
_nintendo = False
lx, ly, rx, ry, _btns, _dpad = [None] * 6

# the functions below will be imported from the PyBricks Blocks language
def bp_init(port_letter,nintendo=True):
    global _bp
    global _nintendo
    port = eval('Port.' + port_letter)
    _bp = BluePad(port)
    _nintendo = nintendo

def gamepad():
    global lx, ly, rx, ry, _btns, _dpad
    lx, ly, rx, ry, _btns, _dpad = _bp.gamepad()

def lpad_x():
    return lx

def lpad_y():
    return ly

def rpad_x():
    return rx

def rpad_y():
    return ry

def btns():
    b=_bp.btns_pressed(_btns,_nintendo)
    if 'ZL'in b:
        zl_pos=b.index('ZL')
        b[zl_pos]='1'
    if 'ZR' in b:
        zr_pos=b.index('ZR')
        b[zr_pos]='2'
    return ''.join(b)

def dpad():
    return ''.join(_bp.dpad_pressed(_dpad,_nintendo))

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
