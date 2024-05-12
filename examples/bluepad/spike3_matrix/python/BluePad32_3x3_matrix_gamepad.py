# Paste this script in new Python project in the LEGO SPIKE Prime object.
# Required hardware:
# - Single SPIKE Prime kit to build a Hot Rod. Instructions: https://www.antonsmindstorms.com/product/hot-rod-with-spike-prime-pdf-building-instructions/
# - LMS-ESP32. https://www.antonsmindstorms.com/product/wifi-python-esp32-board-for-mindstorms/
# - 12 RGB Leds to make the lights. https://www.antonsmindstorms.com/product/rgb-ws2812-neopixel-leds-10x6-for-mindstorms/

# See it in action here:
# https://www.instagram.com/p/C40iGBvpZNu/

from hub import port
import time
import color
import color_matrix
import device
import motor
import math
import runloop

# This script assumes you have flashed your LMS-ESP32 board with Bluepad-SPIKE via firmware.antonsmindstorms.com
# Next you need to configure it via bluepad.antonsmindstorms.com
# Set it to light matrix and ensure you have 12 LEDs on GPIO21. Connect your leds to that port.
# For this demo we connect a neopixel matrix to the LMS-ESP32. Confiure the leds to form a 3x3 matrix 
# corresponding to the original 3x3 color matrix




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
        (self.lx,self.ly,self.rx,self.ry,self.buttons,self.dpad,_,_)=device.data(self.port)
        # optional scale and deadzone
        self.lx = self.scale100(self.lx)
        self.ly = self.scale100(self.ly)
        self.rx = self.scale100(self.rx)
        self.ry = self.scale100(self.ry)

gp=Gamepad(port.A)

pixels = [(color.BLUE, 2),(color.GREEN, 2),(color.YELLOW, 2),
          (color.PURPLE, 2),(color.ORANGE, 2),(color.RED, 2),
          (color.BLUE, 2),(color.AZURE, 2),(color.MAGENTA, 2)] 
new_pixels=[i for i in pixels]
color_matrix.show(port.A, pixels)

async def main():
    while (1):
        gp.refresh()
        print(gp.rx,gp.ry,gp.lx,gp.ly,gp.buttons,gp.dpad)
        await runloop.sleep_ms(200)

async def leds():
    global pixels
    while (1):
        new_pixels[0]=pixels[6]
        new_pixels[1]=pixels[3]
        new_pixels[2]=pixels[6]
        new_pixels[3]=pixels[7]
        new_pixels[4]=pixels[4]
        new_pixels[5]=pixels[1]
        new_pixels[6]=pixels[8]
        new_pixels[7]=pixels[5]
        new_pixels[8]=pixels[2]
        pixels=[i for i in new_pixels]
        color_matrix.show(port.A, pixels)
        await runloop.sleep_ms(500)

runloop.run(main(),leds())
