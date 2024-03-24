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
# Then create this LED mapping
# | 0| 1| 4|
# | 5| 8| 6|
# | 7|10|11|

WHEELBASE = 120 # mm
CAR_WIDTH = 114 # mm
STEER_GEAR_RATIO = 20 / 12

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

gp=Gamepad(port.E)

color_matrix.set_pixel(port.E, 2,1, (color.WHITE, 10)) # front left headlight led
color_matrix.set_pixel(port.E, 0,2, (color.WHITE, 10)) # front right headlight led


motor.run_to_absolute_position(port.F, 15, 100)
time.sleep_ms(500)
motor.reset_relative_position(port.F, 0)

async def main():
    while (1):
        gp.refresh()
        target_wheel_angle = gp.rx*-0.4
        target_motor_pos = target_wheel_angle * STEER_GEAR_RATIO
        # make motor F move to the target with feedback loop
        motor.set_duty_cycle(
            port.F, 
            int( (target_motor_pos - motor.relative_position(port.F)) * 100 )
            )
        
        # Now calculate the turn radius and the electronic differential
        current_front_wheel_angle = motor.relative_position(port.F) / STEER_GEAR_RATIO
        base_speed = gp.ly*-10 # forward stick is -100, hence the minus.

        if current_front_wheel_angle == 0:
            motor.run( port.A, base_speed)
            motor.run( port.B, base_speed* -1)
        else: 
            turn_radius = 120/math.tan(math.radians( current_front_wheel_angle ))

            motor.run(
                port.A, 
                int( (turn_radius + CAR_WIDTH/2)/turn_radius*base_speed )
                )
            motor.run(
                port.B,
                int( (turn_radius - CAR_WIDTH/2)/turn_radius*base_speed ) *-1

                )
        await runloop.sleep_ms(15)

async def leds():
    while (1):
        current_front_wheel_angle = motor.relative_position(port.F) / 20 * 12
        speed = motor.velocity(port.A)
        color_matrix.set_pixel(port.E, 2,2, (color.WHITE, 10)) # front left indicator led
        color_matrix.set_pixel(port.E, 1,2, (color.WHITE, 10)) # front right indicator led
        if speed > 5:
            color_matrix.set_pixel(port.E, 2,0, (color.RED, 3)) # back left middle led
            color_matrix.set_pixel(port.E, 1,0, (color.RED, 3)) # back right middle led
            color_matrix.set_pixel(port.E, 0,0, (color.RED, 3)) # back right indicator led
            color_matrix.set_pixel(port.E, 0,1, (color.RED, 3)) # back left indicator led
        elif -2 <= speed <= 2:
            color_matrix.set_pixel(port.E, 2,0, (color.RED, 10)) # back left middle led
            color_matrix.set_pixel(port.E, 1,0, (color.RED, 10)) # back right middle led
            color_matrix.set_pixel(port.E, 0,0, (color.RED, 10)) # back right indicator led
            color_matrix.set_pixel(port.E, 0,1, (color.RED, 10)) # back left indicator led
        else:
            color_matrix.set_pixel(port.E, 2,0, (color.WHITE, 10)) # back left middle led
            color_matrix.set_pixel(port.E, 1,0, (color.WHITE, 10)) # back right middle led
            color_matrix.set_pixel(port.E, 0,0, (color.RED, 3)) # back right indicator led
            color_matrix.set_pixel(port.E, 0,1, (color.RED, 3)) # back left indicator led
        await runloop.sleep_ms(15)

        if current_front_wheel_angle >= 5:
            color_matrix.set_pixel(port.E, 2,2, (color.ORANGE, 10)) # front left indicator led
            color_matrix.set_pixel(port.E, 0,1, (color.ORANGE, 10)) # back left indicator led
            await runloop.sleep_ms(150)
            color_matrix.set_pixel(port.E, 2,2, (color.BLACK, 10)) # front left indicator led
            color_matrix.set_pixel(port.E, 0,1, (color.BLACK, 10)) # back left indicator led
            await runloop.sleep_ms(150)
        elif current_front_wheel_angle <= -5:
            color_matrix.set_pixel(port.E, 1,2, (color.ORANGE, 10)) # front right indicator led
            color_matrix.set_pixel(port.E, 0,0, (color.ORANGE, 10)) # back right indicator led
            await runloop.sleep_ms(150)
            color_matrix.set_pixel(port.E, 1,2, (color.BLACK, 10)) # front right indicator led
            color_matrix.set_pixel(port.E, 0,0, (color.BLACK, 10)) # back right indicator led
            await runloop.sleep_ms(150)

runloop.run(main(), leds())
