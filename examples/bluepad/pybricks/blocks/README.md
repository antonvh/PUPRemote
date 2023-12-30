# Bluepad32 in Blocks Pybricks
Here you find some examples for using the BluePad32 firmware together with the Block-based pybricks

## Template
The `bp_template.py` contains the blocks needed for importing the bluepad library in the blocks version of pybricks. When using this template, the user can deploy the following functions:
* bp_init
* gamepad
* lpad_x
* lpad_y
* rpad_x
* rpad_y
* neopixel_init
* neopixel_zero
* neopixel_set
* neopixel_fill
* servo
  
## get started
Take the followijg steps to get started with bluepad32 using blcoks in PyBricks:
- flash you LMS-ESP32 board with the 'BluePad32 LPF2 for PyBricks projects' from [firmware.antonsmindstorms.com](https://firmware.antonsmindstorms.com/).
- upload the file [blocks_bp.py](blocks_bp.py) to the PyBricks programming environment.
- upload the template (`bp_template.py`) or the demo ('bp_demo.py') to the Pybricks programming environment
- connect the LMS-ESp32 to a port of the Mindstorms Hub (ny default we assume thattis is port "A"). Change the port correspondingly in the template or demo program.
- connect a bluetooth game controller
- start the Pybricks template or demo program
