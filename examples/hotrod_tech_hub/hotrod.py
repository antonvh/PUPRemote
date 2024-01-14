# Add pupremote.py in pybricks, with the contents of pupremote_hub.py
# to run this. 
# Build a hotrod with a Technic Hub and steer on Port A and fwd on Port B

from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch


from pupremote import PUPRemoteHub

p=PUPRemoteHub(Port.D)
steer = Motor(Port.A)
fwd = Motor(Port.B)
p.add_command('gmpd',"hhhhHH","HHHHHHHH")

def btns_pressed(btns):
    pressed = []
    if btns & 1:
        pressed.append("X")
    if btns & 2:
        pressed.append("O")
    if btns & 4:
        pressed.append("[]")
    if btns & 8:
        pressed.append("Δ")
    return pressed

def dpad_pressed(btns):
    pressed = []
    if btns & 1:
        pressed.append("D") # Down
    if btns & 2:
        pressed.append("R") # Right
    if btns & 4:
        pressed.append("L") # Left
    if btns & 8:
        pressed.append("U") # Up
    return pressed

def scale_stick(val, min_val, max_val, deadzone=25):
    if -deadzone <= val <= deadzone:
        val = 0
    return (float(val + 512) / 1024) * (max_val - min_val) + min_val

steer.run_until_stalled(-150)
steer.reset_angle(-200)
steer.run_target(300, 0)

while 1:
    lx, ly, rx, ry, btns, dpad = p.call('gmpd')
    print("Left: {},{}.  Right: {},{}. Buttons:{}. Dpad:{}".format(lx,ly,rx,ry,btns_pressed(btns), dpad_pressed(dpad)))
    
    if -512 <= lx <= 512: # Gamepad is connected if it returns regular values
        # Bottom right is positive
        turn = scale_stick(rx, 100,-100)
        spd = scale_stick(ly, 110,-110)
        steer.track_target(turn)
        fwd.dc(spd)
    
