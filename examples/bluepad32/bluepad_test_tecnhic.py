
from pybricks.hubs import TechnicHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

hub = TechnicHub()

from bluepad32 import BluePad

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

while 1:
    (gplx,gply,gprx,gpry,buttons,dpad)=bp.gamepad()
    print(gplx,gply,gprx,gpry,buttons,dpad)
    print(bp.btns_pressed(buttons,nintendo=True),bp.dpad_pressed(dpad,nintendo=True))
    wait(20)
