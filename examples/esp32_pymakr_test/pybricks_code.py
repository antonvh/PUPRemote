from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch
from pybricks.iodevices import PUPDevice
from pupremote import PUPRemoteHub


p=PUPRemoteHub(Port.A)


p.add_channel('cntr',to_hub_fmt="b") # Counts the number of msg and num calls
p.add_command('msg',"repr","repr")
p.add_command('num',from_hub_fmt="b", to_hub_fmt="b")

# Play with the delay (default 100) to see when then answer is actual
DELAY = 30
print( p.call('cntr') )
print( p.call('msg','kello', wait_ms=DELAY), '== kellokello' )
print( p.call('num',5, wait_ms=DELAY), '== 10' )
print( p.call('msg','hello', wait_ms=DELAY), '== hellohello' )
print( p.call('num',4, wait_ms=DELAY), '== 8' )
print( p.call('num',0, wait_ms=DELAY), '== 0' )
print( p.call('cntr') )

