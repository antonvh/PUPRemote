import VL53L0X
from machine import Pin, SoftI2C

# lms-esp32 defaults
i2c = SoftI2C(scl=Pin(4), sda=Pin(5), freq=100000)

print(i2c.scan())  # Scan for devices. The VL53L0X should show up.

# Setup VL53L0X
tof = VL53L0X.VL53L0X(i2c)

# TODO: find out what this does?
# tof.set_Vcsel_pulse_period(tof.vcsel_period_type[0], 18)
# tof.set_Vcsel_pulse_period(tof.vcsel_period_type[1], 14)


while True:
    # Start ranging
    tof.start()
    tof.read()
    print(tof.read())
    tof.stop()
