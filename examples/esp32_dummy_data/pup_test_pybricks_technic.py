from pybricks.hubs import TechnicHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch
from pupremote import PUPRemoteHub

hub = TechnicHub()

p=PUPRemoteHub(Port.A)
p.add_command('msg',from_hub_fmt="B", to_hub_fmt="B")
p.add_command('num',from_hub_fmt="3b", to_hub_fmt="3b")
i=0
cnt=0
while True:
    cnt+=1
    if cnt>50:
        cnt=0
        print(p.call('num',1,2,3))
    q=p.call('msg')
    print(q)
    i+=1
    if i==20:
        p.call('msg',q)
        i=0
    wait(20)