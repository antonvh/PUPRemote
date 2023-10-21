__author__ = "Anton Vanhoucke & Ste7an"
__copyright__ = "Copyright 2023, AntonsMindstorms.com"
__license__ = "GPL"
__version__ = "1.0.0"
__status__ = "Production"


from pupremote import PUPRemoteHub

FILL = 0x10
ZERO = 0x20
SET  = 0x30
CONFIG = 0x40
WRITE = 0x80

class BluePad:
    """
    Class for using LMS-ESP32 running BluePad32 LPF2 firmware. Defines methods for reading
    connected Bluetooth gamepad (such as PS4 or Nintendo Switch) and for driving NeoPixels and Servo motors connected
    to the LMS-ESP32 board.
   
    :param port: The port to which the LMS-ESp32 running BluePad32 is connected.
    :type port: Port (Example: Port.A)
   
    """

    try:
        from pupremote import PUPRemoteHub
    except:
        pass
    def __init__(self,port):
        self.prh=PUPRemoteHub(port)
        self.prh.add_command('gpled','hhhhHH','16B')
        self.prh.add_command('gpsrv','hhhhHH','8H')
        self.cur_mode=0
        self.nr_leds=64

    def gamepad(self):
        """
        Returns the reading of a gamepad as a tuple. Returns the x- and y values of the left and right
        pads. Buttons are encoded as single bits in `buttonss`. The dpad values are encoded in `dpad`.
         
        :return: Tuple (left_pad_x,left_pad_y,right_pad_x,right_pad_y,buttons,dpad)
        """
    
        if self.cur_mode==0:
            return self.prh.call('gpled')
        elif self.cur_mode==1:
            return self.prh.call('gpsrv')
        else:
            return None


    def neopixel_init(self,nr_leds,pin):
        """
        Initializes a NeoPixel string with the given number of LEDs aconnected to the specified GPIO pin.

        :param nr_leds: The number of leds in the NeoPixel string
        :type nr_leds: byte
        :param pin: The GPIO pin number connected to the NeoPixel string
        :type pin: byte
        """
        leds=[0]*16
        leds[0]=CONFIG
        leds[1]=nr_leds
        leds[2]=pin
        r=self.prh.call('gpled',*leds)
        self.cur_mode=0
        self.nr_leds=nr_leds
        return r

    def neopixel_fill(self,r,g,b,write=True):
        """
        Fills all the neopixels with the same color.

        :param r: red color value
        :type r: byte
        :param g: green color value
        :type g: byte
        :param b: blue color value
        :type b: byte
        :param write: If True write the output to the NeoPixels. Defaults to True.
        :type write: bool
        """
        global cur_mode
        leds=[0]*16
        leds[0]=FILL|WRITE if write else FILL
        leds[1:4]=[r,g,b]
        r=self.prh.call('gpled',*leds)
        self.cur_mode=0
        return r

    def neopixel_zero(self,write=True):
        """
        Zeros all neopixels with value (0,0,0)
 
        :param write: If True writes the output to the NeoPixels. Defaults to False.
        :type write: bool
        """
        leds=[0]*16
        leds[0]=ZERO|WRITE if write else FILL
        r=self.prh.call('gpled',*leds)
        self.cur_mode=0
        return r


    def neopixel_set(self,led_nr,color,write=True):
        """
        Sets single NeoPixel at position led_nr with color=(r,g,b).

        :param led_nr: Position of the led to set (counting from 0)
        :type led_nr: byte
        :param color: Tuple with color for led (r,g,b)
        :param color: (r,g,b) with r,g,b bytes
        :param write: If True writes the output to the NeoPixels. Defaults to True.
        :type write: bool
        """
        leds=[0]*16
        leds[0]=SET|WRITE if write else FILL
        leds[1]=1
        leds[2]=led_nr
        if led_nr>=self.nr_leds:
            print("error neopixel_set: led_nr larger than number of leds!")
            r=None
        else:
            leds[3:6]=color
            r=self.prh.call('gpled',*leds)
        self.cur_mode=0
        return r

    def neopixel_set_multi(self,start_led,nr_led,led_arr,write=True):
        """
        Sets multiple NeoPixel value(s). Maximum number os leds is 4.

        :param start_led: Starting led number (counting from 0).
        :type start_led: byte
        :param nr_led: Number of leds to set.
        :type nr_led: byte
        :param led_arr: Array containing tuples (r,g,b) for each neopixel. Led dimension must correspond to 
        :param write: If True write the output to the NeoPixels. Defaults to True.
        :type write: bool
        """
        leds=[0]*16
        leds[0]=SET|WRITE if write else FILL
        leds[1]=nr_led
        leds[2]=start_led
        if nr_led>4:
            print("error neopixel_set_multi: led_nr larger than 4!")
            r=None
        else:
            if len(led_arr)==3*nr_led:
                leds[3:3+nr_led*3]=led_arr
                r=self.prh.call('gpled',*leds)
            else:
                print("error neopixel_set_multi: led_nr does not correspons with led_arr")
                r=None
        self.cur_mode=0
        return r

    def servo(self,servo_nr,pos):
        """
        Sets Servo motor servo_nr to the specified position. Servo motors should be connected to
        GPIO pins 21, 22, 23 and 25.

        :param servo_nr: Servo motor counting from 0
        :type servo_nr: byte
        :param pos: Position of the Servo motor
        :type: word (2 byte int)
        """
        global cur_mode
        s=[0]*4
        s[servo_nr]=pos%180
        r=self.prh.call('gpsrv',*s)
        cur_mode=1
        return r


