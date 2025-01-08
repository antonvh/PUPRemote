
from hub import port
import time
import color
import color_matrix
import device
import motor
import math
import runloop

# This script assumes you have flashed your LMS-ESP32 board with Bluepad-SPIKE via firmware.antonsmindstorms.com
# Next you need to configure it via bluepad.antonsmindstorms.com and select 'Color Sensor'
# Set it to light matrix and ensure you have 12 LEDs on GPIO21. Connect your leds to that port.

class Gamepad:
    def __init__(self, port):
        self.port = port
        self.lx=0
        self.ly=0
        self.rx=0
        self.ry=0
        self.buttons=0
        self.dpad=0

    @staticmethod
    def scale100(pos):
        # Scale the values to integers of -100,100 and add deadzone
        if -10 < pos < 10: # deadzone
            return 0
        else:
            return int((pos*100)/127)

    def refresh(self):
        # get data from LMS-ESP32
        #(self.lx,self.ly,self.rx,self.ry,self.buttons,self.dpad,_,_)=device.data(self.port)
        raw = device.data(self.port)
        f1,f2,f3=raw[0:3]
        # optional scale and deadzone
        self.lx = self.scale100(int(f1%256)-127)
        self.ly = self.scale100(128-((f1//256)&255))
        self.rx = self.scale100(int(f2%256)-127)
        self.ry = self.scale100(128-((f2//256)&255))
        self.buttons = f3%256
        self.dpad = int(f3//256)

gp=Gamepad(port.A)



async def main():
    while (1):
        gp.refresh()
        print(gp.rx,gp.ry,gp.lx,gp.ly,gp.buttons,gp.dpad)
        await runloop.sleep_ms(200)

runloop.run(main())
