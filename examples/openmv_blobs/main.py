# Copy this file to OpenMV Cam H7 Plus
# Comment out the lcd lines if you don't have a lcd shield

### Setup pupremote code

from pupremote import PUPRemoteSensor, OPENMV
from utime import ticks_ms
from time import sleep

WeDo_Ultrasonic, SPIKE_Color, SPIKE_Ultrasonic = 35, 61, 62

x,y,pixels = 0,0,0

def get_blob():
    global x,y,pixels
    return x,y,pixels

def msg(txt):
    print(txt)
    return txt+txt

def num(n):
    print(n)
    return 2*n

p=PUPRemoteSensor(sensor_id=SPIKE_Ultrasonic, platform=OPENMV)
p.add_command('get_blob','hhh')
p.add_command('msg',"repr","repr")
p.add_command('num',from_hub_fmt="b", to_hub_fmt="b")

### End of pupremote setup code



# Single Color RGB565 Blob Tracking Example
#
# This example shows off single color RGB565 tracking using the OpenMV Cam.

import sensor, image, time, math, lcd

lcd.init()

threshold_index = 0 # 0 for red, 1 for green, 2 for blue

# Color Tracking Thresholds (L Min, L Max, A Min, A Max, B Min, B Max)
# The below thresholds track in general red/green/blue things. You may wish to tune them...
thresholds = [(20, 100, 15, 127, 15, 127), # generic_red_thresholds
              (30, 100, -64, -8, -32, 32), # generic_green_thresholds
              (0, 30, 0, 64, -128, 0)] # generic_blue_thresholds

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False) # must be turned off for color tracking
sensor.set_auto_whitebal(False) # must be turned off for color tracking
clock = time.clock()

# Only blobs that with more pixels than "pixel_threshold" and more area than "area_threshold" are
# returned by "find_blobs" below. Change "pixels_threshold" and "area_threshold" if you change the
# camera resolution. "merge=True" merges all overlapping blobs in the image.

while(True):
    clock.tick()
    img = sensor.snapshot()
    blobs = img.find_blobs([thresholds[threshold_index]], pixels_threshold=200, area_threshold=200, merge=True)
    pixels = 0
    largest_blob = {}
    for blob in blobs:
        if blob.pixels() > pixels:
            largest_blob = blob
            pixels = blob.pixels()
        # These values depend on the blob not being circular - otherwise they will be shaky.
#        if blob.elongation() > 0.5:
#            img.draw_edges(blob.min_corners(), color=(255,0,0))
#            img.draw_line(blob.major_axis_line(), color=(0,255,0))
#            img.draw_line(blob.minor_axis_line(), color=(0,0,255))
        # These values are stable all the time.
    if pixels > 0:
        img.draw_rectangle(largest_blob.rect(), thickness = 2)
        x = largest_blob.cx()
        y = largest_blob.cy()
        img.draw_cross(largest_blob.cx(), largest_blob.cy(), thickness=2)
        # Note - the blob rotation is unique to 0-180 only.
#        img.draw_keypoints([(blob.cx(), blob.cy(), int(math.degrees(blob.rotation())))], size=20)
    lcd.display(img.scale(x_scale=0.4, y_scale=0.4, copy=True))

    state=p.process()
#    print(clock.fps())
