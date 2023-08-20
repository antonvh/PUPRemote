from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pupremote import PUPRemoteHub

p=PUPRemoteHub(Port.A)
p.add_command('msg',"repr","repr")
p.add_command('num',from_hub_fmt="3b",to_hub_fmt="3b")

# Print something on the openmv console
for i in range(10):
    print(p.call('msg'))
    print(p.call('num'))
#print(p.call('msg','hello'))

print(p.call('num',1,2,45))
print(p.call('num',5,6,42))