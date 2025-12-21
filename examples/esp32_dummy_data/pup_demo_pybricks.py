from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pupremote import PUPRemoteHub
from pybricks.tools import wait, StopWatch

p=PUPRemoteHub(Port.A)
p.add_command('msg',"repr","repr")
p.add_command('num',from_hub_fmt="3b",to_hub_fmt="3b")
p.add_command('sdata',from_hub_fmt="16B", to_hub_fmt="16B")

data = [-1]*16
print(p.call('num',1,2,-45))
print(p.call('num',5,-6,42))
print(p.call('sdata', *data))
for i in range(100):
    data = [x+i for x in range(16)]
    print(
        i,p.call('sdata', *data)
        )
