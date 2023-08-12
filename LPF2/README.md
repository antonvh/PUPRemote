# PUPRemote

## Symmetric

We define two classes: `PUPRemote` and `PUPRemoteHub`, running on the sensor and the hub, respectively.

On the pup sensor we define a new sensor as follows:
```
pup=PUPRemoteSensor()
pup.add_command('rgb','BBB')
pup.add_command('gyro','HHH','BB') # this mode supports a set function
```

On the hub this is exactly similar:
```
pup=PUPRemoteHub(Port.A)
pup.add_command('rgb','BBB')
pup.add_command('gyro','HHH','BB') # this mode supports a set function and is writable
```

On the pup sensor the user has to define the functions following functions:
```
def rgb():
    # do reading of a color sensor
    # return 3 bytes
    r,g,b = read_color()
    return r,g,b

def gyro():
    # do reading of a gyro sensor
    # return 3 words
    y,p,r = read_gyro()
    return y,p,r

def set_gyro(reg,val):  # this name should be 'set_<mode_name>'
   set_gyro_reg_val(reg,val)
```

On the hub we use the functions as follows:
```
pup.add_port(Port.A)
print(pup.read('gyro'))
pup.write('gyro',123,222)
for i in range(20):
    print(pup.read('rgb'))
```

## Compatibility

Below the test result with different hub and os-es are shown:

|HUB/OS | data from pup to hub | data from hub to pup | multiple modes? |
|--------|---------------------|----------------------|-----------------|
| PyBricks (technic, spike and mindstorms hub) | 32 byte data      | 32 bye data | up to 7 (current LPF2) |
| Mindstorms Inventor Python| 8 values of DATA8 | write_direct not working | up to 7 (current LPF2 |
| SPIKE 3 MicroPython | 8 values DATA16 | None | just mode 0 |


## Limitations
- only a single PUPRemote sensor is supported on a single port on the hub.
- to keep the `add_command` method compatible between the pup sensor and the hub, we define the command function and the call back function as `str` instead of `callable`


## To do
- make one single library of the two classes with full documentation
- power on M2
- move payload as binary data between lpf2 and pupremote
- build in fail save: sensor not present, writing to non writable sensor, etc.
  
# LPF2
This is the original code that we used for emulating a PUPdevice using a microcontroller (ESP32, OpenMV) running MicroPython.

## Heartbeat
The Hub sends every 100ms a NACK_BYTE (0x02). It expects that the sensor send a [MESSAGE_CMD|LENGTH_1|CMD_EXT_MODE,EXT_CODE_m,CKHS] followed by the data of the sensor in its current mode. The EXT_CODE_m is ether 0x00 or 0x08 for extended modes>7. In the current LPF2 the extended modes are not yet supoorted, therefore, this message is always [0x46, 0x00, 0xc9].

## Old LPF2
The old `LPF2.py` code uses a timer to send periodically the measurement data. Because the main program also sends measurement data, things can get corrupted if the timer sends and the user program sends collide.

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
