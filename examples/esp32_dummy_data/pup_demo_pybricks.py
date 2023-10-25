from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pupremote import PUPRemoteHub
from pybricks.tools import wait, StopWatch

p=PUPRemoteHub(Port.A)
p.add_command('msg',"repr","repr")
p.add_command('num',from_hub_fmt="3b",to_hub_fmt="3b")
p.add_command('smalldata',from_hub_fmt="16B", to_hub_fmt="16B")
p.add_command('largedata',from_hub_fmt="32B", to_hub_fmt="32B")

print(p.call('num',1,2,-45))
print(p.call('num',5,-6,42))
print(p.call('smalldata'))
for i in range(100):
    data = [x+i for x in range(16)]
    print(
        i,p.call('smalldata', *data)
        )

for i in range(100):
    data = [x+i for x in range(32)]
    print(
        i, p.call('largedata', *data)
        )