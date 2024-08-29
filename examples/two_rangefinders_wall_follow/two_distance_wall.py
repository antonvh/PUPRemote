from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch
from pupremote import PUPRemoteHub

hub = PrimeHub()

WALL_FOLLOW = 0
WALL_AHEAD  = 1
WALL_SEARCH = 2 # Not implemented yet. Should trigger after turning in circles.
NO_DATA     = 3 # Not implemented yet. Should trigger on invalid data.

MIN_WALL_AHEAD_DIST = 220 # mm
WALL_FOLLOW_TGT_DIST = 150 # mm
BASE_SPEED = 350 # mm/s
# Ensure that the minimum turning radius is wall distance
MAX_TURN_RATE = BASE_SPEED / (2*3.1415*WALL_FOLLOW_TGT_DIST) * 360 # º/s 
print(MAX_TURN_RATE)

KP = -1.5

lm = Motor(Port.F, positive_direction=Direction.COUNTERCLOCKWISE)
rm = Motor(Port.E)
db = DriveBase(lm,rm, 56, 16*8) 

pr = PUPRemoteHub(Port.A)
pr.add_channel('dists', 'hh')

front_dist = right_dist = 0
mode = NO_DATA

while True:
    front_dist, right_dist = pr.call('dists')
    if front_dist > MIN_WALL_AHEAD_DIST:
        mode = WALL_FOLLOW
    else:
        mode = WALL_AHEAD
    
    if mode == WALL_FOLLOW:
        speed = BASE_SPEED
        turn_rate = (WALL_FOLLOW_TGT_DIST - right_dist) * KP # deg/s
        turn_rate = min(max(turn_rate, -MAX_TURN_RATE), MAX_TURN_RATE)
    elif mode == WALL_AHEAD:
        speed = 0
        turn_rate = -200
    db.drive(speed, turn_rate)