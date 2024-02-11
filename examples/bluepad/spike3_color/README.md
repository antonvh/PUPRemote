# SPIKEv3 BluePad32 example

Here you find some examples of how to use BluePad32 together with SPIKEv3. You can use the BluePad32 Spikev3 firmware to read out the controls of a gamepad (Nintendo, PS3, PS4).

## Block Template
This is a template SPIKEv3 block program that allows you to read:
- the x and y cooirdinate the left joystick (lx,ly) from 0 to 255
- the x and y coordnate of the right joystick (rx,ry) from 0 to 255
- the status of the buttons (button) [A=2, B=1, X=8, Y=4, R=32, L=16 for Nintendo Switch Pro controller]
- the status of the dpad (dpad) [U=1, D=2, R=4, L=8]

These values might be different for different controllers. Run the template program and view the variables by clicking the two small vertical lines button in the right of the program screen.


![image](https://github.com/antonvh/PUPRemote/assets/51531682/1c5ceb8f-6049-4a44-bed5-5a8ec795ffe0)

You can use these variables in your own program. the values get updated every time you call the `dpad` function in your main loop of the program.

![image](https://github.com/antonvh/PUPRemote/assets/51531682/8c165b6a-9cc7-4647-8d25-39db9bff441b)

## Block Pixel example
This example show a pixel on the SPIKE 5x5 matrix corresponding to the position of the joysticks on the gamepad. We map the values of the joystick, which are from 0 to 255, to the pixel x and y coordinates from 1 to 5.
