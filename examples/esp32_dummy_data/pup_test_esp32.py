from pupremote import  PUPRemoteSensor, SPIKE_ULTRASONIC

value=0
def msg(*argv):
    if argv!=():
        print(argv)
    return value

value=0
def num(*argv):
    global value
    print("num")
    if argv!=():
        print(argv)
    else:
        print("num called without args")
    value += 1
    return 2*value,-3*value,4*value




p=PUPRemoteSensor(sensor_id=SPIKE_ULTRASONIC, power = True)
p.add_command('msg',"B","B")
p.add_command('num',from_hub_fmt="3b", to_hub_fmt="3b")

### End of pupremote setup code

### Main loop
while(True):
    connected=p.process()



