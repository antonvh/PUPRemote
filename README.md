# PUPRemote

Use this library to communicate as a Powered UP (PUP) Device with LEGO smart hubs. It has a basic PUPDeviceEmulator and a higher-level PUPRemote library that acts more like RPC (Remote Procedure Calling).

## Installation 

### ESP32

- load lpf2.py in flash
- load pupremote.py in flash
- copy demo_esp32.py to main.py and reset or run manually from REPL

### Pybricks

- import pupremote.py
- import demo_pybricks_inventorhub or _technichub

## Compatibility with Pybricks
If you get checksum errors it could be due to a known issue with 32 byte packet size in Pybricks. Pass max_packet_size=16 when instantiating PUPRemoteHub and PUPRemoteSensor classes to work around this issue.

## Contributing

Please fork and streamline the protocol. There are also some TODOs below you can help with. 
Please notify us of projects you made with this and share the code!

### TODO
- Emulate generic sensors
- Support SPIKE2 and Robot Inventor platforms (Only Pybricks is currently supported)
