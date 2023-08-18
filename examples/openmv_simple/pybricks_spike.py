from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pupremote import PUPRemoteHub

p=PUPRemoteHub(Port.A)
p.add_command('msg',"repr","repr")
p.add_command('num',from_hub_fmt="b",to_hub_fmt="b")

# Print something on the openmv console
print(p.call('msg','hello'))
print(p.call('num',45))
print(p.call('num',42))