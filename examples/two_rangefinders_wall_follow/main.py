import VL53L0X
from machine import Pin, SoftI2C
from pupremote import PUPRemoteSensor

pr = PUPRemoteSensor()
pr.add_channel('dists','hh')

# lms-esp32 defaults
i2c1 = SoftI2C(scl=Pin(4), sda=Pin(5))
i2c2 = SoftI2C(scl=Pin(15), sda=Pin(13))

tof_right = VL53L0X.VL53L0X(i2c1)
tof_front = VL53L0X.VL53L0X(i2c2)

tof_front.start()
tof_right.start()
        
while True:
    f = tof_front.read()
    r = tof_right.read()
    print(f, r)
    pr.update_channel('dists', f, r)
    pr.process()
    # Send data to hub
    
