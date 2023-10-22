"""
Example working with a dual pad gamepad. The left gamepad controls a red led 
and the tight gamepad controls a green led, both on a 24-neopixel circular
such as https://nl.aliexpress.com/item/33010280628.html
"""


from pybricks.pupdevices import Motor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch
import umath

from bluepad import BluePad

# instantiate bluepad
bp=BluePad(Port.A)

bp.neopixel_init(24,12) # set 24 pixel NeoPixel on pin GPIO12
bp.neopixel_fill(30,0,0)
wait(300)
bp.neopixel_zero()
wait(300)

# st=StopWatch()
# i=0
# for x in range(100):
#     i+=1
#     i%=20
#     q=bp.neopixel_set_multi(i%5,3,[i,(i+6)%20,(i+12)%20]*3)
    
# print(st.time())
# st=StopWatch()
# for x in range(100):
#     q=bp.servo(0,x%180)
#     print(q)
# print(st.time())

def set_angle(angle,r,g,b):
    for i in range(6):
        lednr=(angle-6+i)%24
        f=i/5.
        bp.neopixel_set(lednr,int(r*f),int(g*f),int(b*f))
    for i in range(6):
        lednr=(angle+i)%24
        f=1-i/5.
        bp.neopixel_set(lednr,int(r*f),int(g*f),int(b*f))
        

while 1:
    (gplx,gply,gprx,gpry,buttons,dpad)=bp.gamepad()
    #print(gplx,gply,gprx,gpry,buttons,dpad)
    #print(bp.btns_pressed(buttons,nintendo=True),bp.dpad_pressed(dpad,nintendo=True))
    vector1_len=umath.sqrt(gplx**2+gply**2)
    vector2_len=umath.sqrt(gprx**2+gpry**2)
    
    angle1=umath.atan2(gplx,gply)
    angle1=int(-angle1/6.28*24)%24
    angle2=umath.atan2(gprx,gpry)
    angle2=int(-angle2/6.28*24)%24
    
    bp.neopixel_zero()
    if vector1_len>100:
        bp.neopixel_set(angle1,30,0,0)
    if vector2_len>100:
        bp.neopixel_set(angle2,0,30,0)
    wait(10)
