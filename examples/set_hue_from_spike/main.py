# Upload this file to LMS-ESP32 v2.0

from neopixel import NeoPixel
from machine import Pin
from np_animation import hsl_to_rgb
from time import sleep_ms
from pupremote import PUPRemoteSensor

np = NeoPixel(Pin(21),6) 

h = 0
def set_h(val):
    global h
    h=val

pr = PUPRemoteSensor(power=True)
pr.add_command('set_h',from_hub_fmt='i')


# shifting rainbow

while 1:
    for i in range(6):
        #hue = (h+60*i) % 359
        np[i] = hsl_to_rgb(h,100,20) 
    np.write() # write buffer to led
    #h+=1
    
    pr.process()