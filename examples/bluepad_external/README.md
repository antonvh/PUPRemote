# External BluePad32
This is a demo for using an external BluePad32 module. The external module is programmed with the Bluepad32 UartRemote firmware and is connected to the LMS-ESP32 using its UART port. 
The LMS-ESP32 itself is using PUPRemote to comunicate to the PyBricks hub and only the status of the gamead is passed from the external module to the LMS-ESP32. 

## M5stamp Pico
We use the M5Stamp Pico module as a little external module.

![image](https://github.com/antonvh/PUPRemote/assets/51531682/6d886e61-8155-4db0-8edd-3d2b6613cc55)

The firmware is changed for using the pins on the Grove port (pins 32 and 33) which are connected to the Grove port on the LMS-ESP32 (pins 4 and 5):

```
In UartRemote\src\ in UartRemote.h change:

// ESP32 STAMP Pico
#define RXD1 32
#define TXD1 33
// LMS-ESP32
// #define RXD1 18
// #define TXD1 19
```

The voltage input on the M5Stamp Pico is connected to a 5V regulator, but is fed with only 3.3V from the LMS-ESP32. Consequently, we need to bypass the regulator on the M5Stamp Pico by connecting the 5V inut to the 3v3 pin.

![image](https://github.com/antonvh/PUPRemote/assets/51531682/64f869b5-82a2-4e52-b2cc-2529371309b3)


## Programming
### LMS-ESP32 MicroPython
On the LMS-ESP32 we initialize a UartRemote connection to the external BluePad module and a PUPRemote connection to the PyBricks hub:

```
u=UartRemote(rx_pin=4,tx_pin=5)
p=PUPRemoteSensor(sensor_id=SPIKE_ULTRASONIC)
```

Then we can define two function for reading the gamepad values and for checking wether the gamepad is connected to the external BluePad module:

```
def gmpd(*argv):
    ack,resp=u.call('gamepad')
    btn,dpad,lx,ly,rx,ry=resp
    return (lx,ly,rx,ry,btn,dpad)

def conn(*argv):
    global con
    ack,con=u.call('connected')
    return con

```
to read the gamepad values from the external Bluepad and to check connection of the gamepad we define two PUPRemote commands:

```
p.add_command('gmpd',to_hub_fmt="6h")
p.add_command('conn',to_hub_fmt="B")
```

### PyBricks
The following code runs on the OyBricks hub and allows for checking the gamepad connection and read the gamepad status:

```
pup = PUPRemoteHub(Port.A)
pup.add_command('gmpd',to_hub_fmt="6h")
pup.add_command('conn',to_hub_fmt="B")

while True:
    data=pup.call('gmpd')
    print(data)
    wait(0.1)
```
