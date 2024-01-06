from pupremote import  PUPRemoteSensor, SPIKE_ULTRASONIC
from uartremote import *
from time import sleep_ms

u=UartRemote(rx_pin=4,tx_pin=5)
p=PUPRemoteSensor(sensor_id=SPIKE_ULTRASONIC)

def gmpd(*argv):
    ack,resp=u.call('gamepad')
    btn,dpad,lx,ly,rx,ry=resp
    return (lx,ly,rx,ry,btn,dpad)

def conn(*argv):
    global con
    ack,con=u.call('connected')
    return con

p.add_command('gmpd',to_hub_fmt="6h")
p.add_command('conn',to_hub_fmt="B")

### Main loop
while(True):
    connected=p.process()
