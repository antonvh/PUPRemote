# SPIKEv3 BluePad32 example

Here you find some examples of how to use BluePad32 together with SPIKEv3. You can use the BluePad32 Spikev3 firmware to read out the controls of a gamepad (Nintendo, PS3, PS4).

## Block Template
This is a template SPIKEv3 block program that allows you to read:
- the x and y cooirdinate the left joystick (lx,ly)
- the x and y coordnate of the right joystick (rx,ry)
- the status of the buttons (button)
- the status of the dpad (dpad)

You can use these variables in your own program. the values get updated every time you call the `dpad` function in your main loop of the program.
## Block Pixel example
This example show a pixel on the SPIKE 5x5 matrix corresponding to the position of the joysticks on the gamepad
