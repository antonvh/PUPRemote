from PUPRemote.pd_emu import PUPDeviceEmulator
from machine import UART
uart = UART(1, 115200)
pd = PUPDeviceEmulator(uart)
while 1:
    for i in range(0, 100):
         pd.write(0, i) # write value to mode 0
    ret_val = pd.read(1) # read value from mode 1, set by remote hub.
                
