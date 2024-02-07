from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch
from pupremote import PUPRemoteHub

buttons={'y':(8,[4,0],'C#4/16'),'g':(16,[0,4],'E3/16'),'b':(32,[0,0],'E4/16'),'r':(64,[4,4],'A4/16')}


hub = PrimeHub()
hub.display.off()
p=PUPRemoteHub(Port.A)
p.add_command('touch','H')
p.add_command('val','4H')
p.add_command('tresh','H','H')

p.call('tresh',400)
while True:
    btns=p.call('touch')
    
    pressed=[]
    for c in 'ygbr':
        pressed.append(c if btns&buttons[c][0]>0 else '.')
    print(pressed)
    hub.display.off()
    for col in pressed:
        if col!='.':
            hub.display.pixel(*buttons[col][1],100)
    vals=p.call('val')
    print(','.join(["%4d"%v for v in vals]))
    
