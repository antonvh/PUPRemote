import VL53L0X
from lpf2 import LPF2, DATA16
from machine import Pin, SoftI2C

# lms-esp32 defaults
i2c = SoftI2C(scl=Pin(4), sda=Pin(5), freq=100000)

print(i2c.scan())  # scan for devices

# Create a VL53L0X object
tof = VL53L0X.VL53L0X(i2c)

single_mode_ds = [
    LPF2.mode(
        "DISTL",
        1,
        DATA16,
        format="5.1",
        symbol="CM",
        raw_range=(0.0, 250.0),
        percent_range=(0.0, 100.0),
        si_range=(0.0, 2500.0),
        functionmap=[0, 145],
    )
]

sensor_emu = LPF2(single_mode_ds, 62)

while True:
    # Start ranging
    tof.start()
    d = tof.read()
    print(d)
    tof.stop()
    # Send data to hub
    sensor_emu.send_payload(d)
    # Look alive!
    sensor_emu.heartbeat()
