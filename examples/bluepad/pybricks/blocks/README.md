# Bluepad32 in Blocks Pybricks
Here you find some examples for using the BluePad32 firmware together with the Block-based pybricks. First you need to install the `pupremote.py`, `bluepad.py` and `blocks_bp.py` from the [src directory](https://github.com/antonvh/PUPRemote/tree/main/src) of this repo.

## Template
The `bp_template.py` contains the blocks needed for importing the bluepad library in the blocks version of PyBricks. When using this template, the user can deploy the following functions:
* bp_init
  
![image](https://github.com/antonvh/PUPRemote/assets/51531682/7e4c0def-6edb-45f0-a1f9-d4894bd9716a)

First parameter is the port ("A", as a string) and second parameter indicates that the controller is a Nintendo controller (True) or False for e.g. a Sony PS4 controller.
* gamepad
  
![image](https://github.com/antonvh/PUPRemote/assets/51531682/9f187e40-a63f-4acf-91e2-c6f15dad9283)

This function reads the current gamepad values and populates the left and right pad x- adn y-positions and the buttons and dpad global variables. 
* lpad_x
  
![image](https://github.com/antonvh/PUPRemote/assets/51531682/1b7afb32-1008-41fc-a0d4-7c6f30df803b)

Reads the global left pad x position (read by the last gamepad() call)
* lpad_y

Reads the left pad y-coordinate.
* rpad_x

Reads the right pad x-coordinate.
* rpad_y

Reads the right pad y-coordinate.
* neopixel_init
  
![image](https://github.com/antonvh/PUPRemote/assets/51531682/1778e84a-5e9b-4e8c-b8e6-3d6574b8b2f1)

Initializes the NeoPixel with a number of pixels (first parameter) and the hardware GPIO port to which the NeoPixels are connected (second parameter).

* neopixel_zero
  
![image](https://github.com/antonvh/PUPRemote/assets/51531682/3041b99f-6ebb-4f7b-bc1c-e6c84c2dee16)

Turn off all NeoPixels.

* neopixel_set
  
![image](https://github.com/antonvh/PUPRemote/assets/51531682/de9ce041-2604-4a09-be7f-8eb6476c092f)

Set a NeoPixel at number `n` (first parameter) to a color with `r`,`g`,`b` values (parameter 2 until 4). The fifth optional parameter is a boolean that determines whether the pixels are written to the physical neopixels, default is True.
* neopixel_fill
  
![image](https://github.com/antonvh/PUPRemote/assets/51531682/6f0b2ea3-18b7-4fac-b9d0-5d3500304218)

Fills all NeoPixels with the same color defined by `r`,`g` and `b` (parameter 1 until 3).

* servo
  
![image](https://github.com/antonvh/PUPRemote/assets/51531682/1e9bfcee-e3f5-4d2d-86bf-455fcecf91d0)

The first parameter indicates the servo motor number `n` ( where servo number 0 is attached to GPIO pin 21, servo 1 to pin 22, servo 2 to pin 23, and servo  4 to pin 25). The second parameter `angle` is the angle to which the servo is set (usually between 0 and 180).
## get started
Take the following steps to get started with BluePad32 using blcoks in PyBricks:
- flash you LMS-ESP32 board with the 'BluePad32 LPF2 for PyBricks projects' from [firmware.antonsmindstorms.com](https://firmware.antonsmindstorms.com/).
- upload the files `pupremote.py` (or `pupremote_hub.py` renamed to `pupremote.py`), `bluepad.py` and `blocks_bp.py` from the [src directory](https://github.com/antonvh/PUPRemote/tree/main/src) to the PyBricks programming environment.
- upload the template (`bp_template.py`) or the demo ('bp_demo.py') to the Pybricks programming environment
- connect the LMS-ESp32 to a port of the Mindstorms Hub (ny default we assume thattis is port "A"). Change the port correspondingly in the template or demo program.
- connect a bluetooth game controller
- start the Pybricks template or demo program
