from neopixel import NeoPixel
from pupremote import  PUPRemoteSensor, SPIKE_ULTRASONIC
from machine import Pin

np=NeoPixel(Pin(21),64)

def ledxx(l):
    np.fill((l,l,l))
    np.write()
    return l

p=PUPRemoteSensor(sensor_id=SPIKE_ULTRASONIC,power=True)
p.add_command('ledxx',"B","B")
### End of pupremote setup code

### Main loop
while(True):
    connected=p.process()

