from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pupremote import PUPRemoteHub

p=PUPRemoteHub(Port.A)
# Send and receive any object with 'repr' encoding
p.add_command('msg',"repr","repr")

# Send and receive a signed byte with 'b'
# See https://docs.python.org/3/library/struct.html#format-characters
p.add_command('num',from_hub_fmt="b", to_hub_fmt="b")

# Do no execute procedures, but only present new data to hub
p.add_channel('one_w', to_hub_fmt="bbb")


# Print something on the openmv console
print(p.call('msg','hello'))
print(p.call('num',45))
print(p.call('num',42))
print(p.call('one_w'))