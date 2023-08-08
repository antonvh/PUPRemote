# LPF2
This is the original code that we used for emulating a PUPdevice using a microcontroller (ESP32, OpenMV) running MicroPython.

## Heartbeat
The Hub sends every 100ms a NACK_BYTE (0x02). It expects that the sensor send a [MESSAGE_CMD|LENGTH_1|CMD_EXT_MODE,EXT_CODE_m,CKHS] followed by the data of the sensor in its current mode. The EXT_CODE_m is ether 0x00 or 0x08 for extended modes>7. In the current LPF2 the extended modes are not yet supoorted, therefore, this message is always [0x46, 0x00, 0xc9].

## Old LPF2
The old `LPF2.py` code uses a timer to send periodically the measurment data. Because the main program also send measurement data, things can get corrupted if the timer send and the user program send collide.

## New LPF2 Clean Heartbeat
In`LPF2_new.py` a heartbeat method is used that takes care of detecting a NACK_BYTE and sending te response of the CMD_EXT_MODE and the last pyaload data. It should do that at least every HEARTBEAT_PERIOD, which is defined as 200ms.

The main loop in the user program looks like this:

```
last_heartbeat = ticks_ms()
last_send = ticks_ms()
# Loop
while True:
    if (ticks_ms() - last_heartbeat > 20):
        last_heartbeat = ticks_ms()
        lpf2.heartbeat()
        if ((ticks_ms() - last_send)>1000) and lpf2.connected:
              last_send=ticks_ms()
              mode=lpf2.current_mode
	      if mode==0:
                  lpf2.send_payload('Int16',[value,value*2,value*3,value*4,value*5,value*6,value*7,value*8])
              elif mode==1:
                  lpf2.send_payload('Int32',(value+1000000000*value)&0x7fffffff)
              elif mode==2:
                  lpf2.send_payload('float',value*1.010101)
          
```

A call back function is defined for catching data send by the hub to the sensor:

```
def cb(size,buf):
    print('own callback')
    print(size,[i for i in buf])

lpf2.set_call_back(cb)

```