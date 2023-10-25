from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pupremote import PUPRemoteHub
from pybricks.tools import wait, StopWatch

p=PUPRemoteHub(Port.A)
p.add_command('msg',"repr","repr")
p.add_command('num',from_hub_fmt="3b",to_hub_fmt="3b")
p.add_command('smalldata',from_hub_fmt="16b", to_hub_fmt="16b")
p.add_command('largedata',from_hub_fmt="32b", to_hub_fmt="32b")
# Print something on the openmv console
#for i in range(10):
#    print(p.call('msg'))
#    print(p.call('num'))
#print(p.call('msg','hello'))

print(p.call('num',1,2,45))
print(p.call('num',5,6,42))
print(p.call('smalldata'))
for i in range(100):
    print(i,p.call('smalldata',10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25))
    wait(20)
    
for i in range(100):
    print(i,p.call('largedata',10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,\
                               10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25))
    wait(20)