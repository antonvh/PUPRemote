# LPF2 class allows communication between LEGO SPIKE Prime and third party devices.
__author__ = "Anton Vanhoucke & Ste7an"
__copyright__ = "Copyright 2023, AntonsMindstorms.com"
__license__ = "GPL"
__version__ = "1.1"
__status__ = "Production"

import machine
import struct
import utime
import binascii
from micropython import const
from sys import implementation

# OpenMV board platform type
# sys.implementation[2]: OPENMV4P-STM32H743
OPENMV = const(0)
# LMS-ESP32 board platform type
# sys.implementation[2]: ESP32 module (lvgl,ulab,spiram) with ESP32
ESP32 = const(1)
# OpenMV RT board platform type
# sys.implementation[2]: OpenMV IMXRT1060-MIMXRT1062DVJ6A
OPENMVRT = const(2)

MAX_PKT = const(32)

BYTE_NACK = const(0x02)
BYTE_ACK = const(0x04)
CMD_Type = const(0x40)  # @, set sensor type command
CMD_Select = const(0x43)  #  C, sets modes on the fly
CMD_Mode = const(0x49)  # I, set mode type command
CMD_Baud = const(0x52)  # R, set the transmission baud rate
CMD_Vers = const(0x5F)  # _,  set the version number
CMD_ModeInfo = const(0x80)  # name command
CMD_Data = const(0xC0)  # data command
CMD_EXT_MODE = const(0x6)
EXT_MODE_0 = const(0x00)
EXT_MODE_8 = const(0x08)  # only used for extended mode > 7
CMD_LLL_SHIFT = const(3)

NAME = const(0x0)
RAW = const(0x1)
Pct = const(0x2)
SI = const(0x3)
SYM = const(0x4)
FCT = const(0x5)
FMT = const(0x80)

DATA8 = const(0)
DATA16 = const(1)
DATA32 = const(2)
DATAF = const(3)

ABSOLUTE = const(16)
RELATIVE = const(8)
DISCRETE = const(4)

STRUCT_FMT = ("B", "H", "I", "f")

HEARTBEAT_PERIOD = const(200)  # time of inactivity after which we reset sensor


def __num_bits(x):
    # Return the number of bits required to represent x
    n = 0
    while x > 0:
        x >>= 1
        n += 1
    return n


class LPF2(object):
    def __init__(
        self,
        modes,
        sensor_id=62,
        debug=False,
        max_packet_size=MAX_PKT,
        rx=None,
        tx=None,
        uart_n=None,
    ):
        self.modes = modes
        self.current_mode = 0
        self.sensor_id = sensor_id
        self.connected = False
        self.payloads = {}
        self.last_nack = 0
        self.debug = debug
        self.max_packet_size = max_packet_size
        self.UART_N = uart_n
        self.TX_PIN_N = tx
        self.RX_PIN_N = rx
        if "RT1060" in implementation[2]:
            self.BOARD = OPENMVRT
            if uart_n == None:
                self.UART_N = 1
            print("OpenMV RT defaults loaded")
        elif "OPENMV4P" in implementation[2]:
            self.BOARD = OPENMV
            if uart_n == None:
                self.UART_N = 3
            print("OpenMV H7 defaults loaded")
        else:
            # default to pure ESP32 micorpython
            self.BOARD = ESP32
            if tx == None:
                print("LMS-ESP32 defaults loaded")
                self.TX_PIN_N = 19
            if rx == None:
                self.RX_PIN_N = 18
            if uart_n == None:
                self.UART_N = 2

    @staticmethod
    def mode(
        name,
        size=1,
        data_type=DATA8,
        writable=0,
        format="3.0",
        raw_range=[0, 100],
        percent_range=[0, 100],
        si_range=[0, 100],
        symbol="",
        functionmap=[ABSOLUTE, ABSOLUTE],
        view=True,
    ):
        fig, dec = format.split(".")
        functionmap = [ABSOLUTE, writable]
        total_data_size = size * 2**data_type  # Byte size of data set.
        # Find the power of 2 that is greater than the length of the data
        # -1 because of the header byte. # Really?
        bit_size = __num_bits(total_data_size - 1)
        mode_list = [
            name,  # 0
            [size, data_type, int(fig), int(dec)],  # 1
            raw_range,  # 2
            percent_range,  # 3
            si_range,  # 4
            symbol,  # 5
            functionmap,  # 6
            view,  # 7
            total_data_size,  # 8
            bit_size,  # 9
        ]
        return mode_list

    def slow_uart(self):
        if self.BOARD == ESP32:
            tx_pin = machine.Pin(self.TX_PIN_N, machine.Pin.OUT, machine.Pin.PULL_DOWN)
            tx_pin.value(0)
            utime.sleep_ms(500)
            tx_pin.value(1)
            self.uart = machine.UART(
                self.UART_N,
                baudrate=2400,
                rx=self.RX_PIN_N,
                tx=self.TX_PIN_N,
            )

        elif self.BOARD == OPENMVRT:
            tx_pin = machine.Pin("P4", machine.Pin.OUT, machine.Pin.PULL_DOWN)
            tx_pin.value(0)
            utime.sleep_ms(500)
            tx_pin.value(1)
            self.uart = machine.UART(self.UART_N, 2400)

        elif self.BOARD == OPENMV:
            import pyb

            tx_pin = pyb.Pin("P4", pyb.Pin.OUT_PP)
            tx_pin.value(0)
            utime.sleep_ms(500)
            tx_pin.value(1)
            self.uart = pyb.UART(self.UART_N, 2400)

    def fast_uart(self):
        if self.BOARD == ESP32:
            self.uart = machine.UART(
                self.UART_N,
                baudrate=115200,
                rx=self.RX_PIN_N,
                tx=self.TX_PIN_N,
            )

        elif self.BOARD == OPENMVRT:
            self.uart = machine.UART(self.UART_N, 115200)

        elif self.BOARD == OPENMV:
            import pyb

            self.uart = pyb.UART(self.UART_N, 115200)

    # -------- Payload definition

    def load_payload(self, data, data_type=DATA8, mode=None):
        if mode is None:
            mode = self.current_mode
        if isinstance(data, bytes):
            bin_data = data
        elif isinstance(data, bytearray):
            bin_data = data
        elif isinstance(data, list):
            # We have a list of integers. Pack them as bytes.
            bin_data = struct.pack("%d" % len(data) + STRUCT_FMT[data_type], *data)
        elif isinstance(data, float) or isinstance(data, int):
            bin_data = struct.pack(STRUCT_FMT[data_type], data)
        elif isinstance(data, str):
            # String. Convert to bytes of max size.
            bin_data = bytes(data, "UTF-8")[: self.max_packet_size]
        else:
            raise ValueError("Wrong data type: %s" % type(data))

        bytesize = self.modes[mode][8]
        bit = self.modes[mode][9]

        assert len(bin_data) > 0, "Payload is empty"
        assert len(bin_data) <= bytesize, "Wrong payload size"

        payload = bytearray(2**bit + 2)
        cksm = 0xFF
        payload[0] = CMD_Data | (bit << CMD_LLL_SHIFT) | mode
        cksm ^= payload[0]
        for i in range(len(bin_data)):
            payload[i + 1] = bin_data[i]
            cksm ^= bin_data[i]
        payload[-1] = cksm  # No need to checksum zero bytes.

        self.payloads[mode] = payload

    def send_payload(self, data=None, data_type=DATA8):
        """
        Convert bytes of data to a proper LPF2 payload,
        save it to the payload of the current mode,
        and write it to the hub. If there is no data, just
        send current payload.
        """
        if not (data == None):
            self.load_payload(data, data_type)
        if self.connected:
            self.writeIt(self.payloads[self.current_mode])
        else:
            if self.debug:
                print("Write payload, but not connected.")

    # ----- comm stuff

    def readchar(self):
        c = self.uart.read(1)
        if self.debug:
            print(c)
        if c == None:
            return -1
        else:
            return ord(c)

    def heartbeat(self):
        if not self.connected:
            print("Checking heartbeat, but not connected. Initializing.")
            self.initialize()
            return

        if (utime.ticks_ms() - self.last_nack) > HEARTBEAT_PERIOD:
            print("Checking heartbeat, but line is dead. Re-initializing.")
            self.connected = False
            self.initialize()
            return

        b = self.readchar()  # Read in any heartbeat or command bytes
        if b > 0:  # There is data, let's see what it is.
            if b == BYTE_NACK:
                # Regular heartbeat pulse from the hub. We have to reply with data.
                self.last_nack = utime.ticks_ms()  # reset heartbeat timer

                # Now send the payload
                self.writeIt(self.payloads[self.current_mode])
                # print("payload", self.payloads[self.current_mode])

            elif b == CMD_Select:
                self.last_nack = utime.ticks_ms()  # reset heartbeat timer
                # The hub is asking us to change mode.
                mode = self.readchar()
                cksm = self.readchar()
                # Calculate the checksum for two bytes.
                if cksm == 0xFF ^ CMD_Select ^ mode:
                    self.current_mode = mode

            elif b == 0x46:
                self.last_nack = utime.ticks_ms()  # reset heartbeat timer
                # Data from hub to sensor should read 0x46, 0x00, 0xb9
                # print("cmd recv")
                ext_mode = self.readchar()  # 0x00 or 0x08
                cksm = self.readchar()  # 0xb9

                if cksm == 0xFF ^ 0x46 ^ ext_mode:
                    b = self.readchar()  # CMD_Data | LENGTH | MODE

                    # Bitmask and then shift to get the size exponent of the data
                    size = 2 ** ((b & 0b111000) >> 3)

                    # Bitmask to get the mode number
                    self.current_mode = (b & 0b111) + ext_mode

                    # Keep track of the checksum while reading data
                    ck = 0xFF ^ b

                    buf = bytearray(size)
                    for i in range(size):
                        buf[i] = self.readchar()
                        # Keep track of the checksum
                        ck ^= buf[i]

                    if ck == self.readchar():
                        return buf
                    else:
                        print(
                            "Checksum error. Try reducing max_packet_size to 16 if using Pybricks."
                        )

    def writeIt(self, array):
        if self.debug:
            print("WriteIt:", binascii.hexlify(array))
        return self.uart.write(array)

    @staticmethod
    def calc_cksm(array):
        chksm = 0xFF
        for b in array:
            chksm ^= b
        return chksm

    def addChksm(self, array):
        return array + self.calc_cksm(array).to_bytes(1, "little")

    # ---- settup definitions

    def setType(self, sensorType):
        return self.addChksm(bytearray([CMD_Type, sensorType]))

    def defineBaud(self, baud):
        rate = baud.to_bytes(4, "little")
        return self.addChksm(bytearray([CMD_Baud]) + rate)

    def defineVers(self, hardware, software):
        hard = hardware.to_bytes(4, "big")
        soft = software.to_bytes(4, "big")
        return self.addChksm(bytearray([CMD_Vers]) + hard + soft)

    def padString(self, string, num, startNum):
        reply = bytearray(string, "UTF-8")
        reply = reply[: self.max_packet_size]
        exp = __num_bits(len(reply) - 1)
        reply = reply + b"\x00" * (2**exp - len(string))
        exp = exp << 3
        return self.addChksm(bytearray([CMD_ModeInfo | exp | num, startNum]) + reply)

    def buildFunctMap(self, mode, num, Type):
        exp = 1 << CMD_LLL_SHIFT
        mapType = mode[0]
        mapOut = mode[1]
        return self.addChksm(
            bytearray([CMD_ModeInfo | exp | num, Type, mapType, mapOut])
        )

    def buildFormat(self, mode, num, Type):
        exp = 2 << CMD_LLL_SHIFT
        sampleSize = mode[0] & 0xFF
        dataType = mode[1] & 0xFF
        figures = mode[2] & 0xFF
        decimals = mode[3] & 0xFF
        return self.addChksm(
            bytearray(
                [
                    CMD_ModeInfo | exp | num,
                    Type,
                    sampleSize,
                    dataType,
                    figures,
                    decimals,
                ]
            )
        )

    def buildRange(self, settings, num, rangeType):
        exp = 3 << CMD_LLL_SHIFT
        minVal = struct.pack("<f", settings[0])
        maxVal = struct.pack("<f", settings[1])
        return self.addChksm(
            bytearray([CMD_ModeInfo | exp | num, rangeType]) + minVal + maxVal
        )

    def defineModes(self):
        length = (len(self.modes) - 1) & 0xFF
        views = 0
        for i in range(len(self.modes)):
            mode = self.modes[i]
            if mode[7]:
                views = views + 1

            # Initialize the payload for this mode
            self.load_payload(b"\x00" * mode[8], mode=i)

        views = (views - 1) & 0xFF
        return self.addChksm(bytearray([CMD_Mode, length, views]))

    def setupMode(self, mode, num):
        self.writeIt(self.padString(mode[0], num, NAME))  # write name
        self.writeIt(self.buildRange(mode[2], num, RAW))  # write RAW range
        self.writeIt(self.buildRange(mode[3], num, Pct))  # write Percent range
        self.writeIt(self.buildRange(mode[4], num, SI))  # write SI range
        self.writeIt(self.padString(mode[5], num, SYM))  # write symbol
        self.writeIt(self.buildFunctMap(mode[6], num, FCT))  # write Function Map
        self.writeIt(self.buildFormat(mode[1], num, FMT))  # write format

    # -----   Start everything up

    def initialize(self):
        # self.debug = True
        self.slow_uart()
        self.writeIt(b"\x00")
        self.writeIt(self.setType(self.sensor_id))
        self.writeIt(self.defineModes())  # tell how many modes
        self.writeIt(self.defineBaud(115200))
        self.writeIt(self.defineVers(2, 2))
        num = len(self.modes) - 1
        for mode in reversed(self.modes):
            self.setupMode(mode, num)
            num -= 1
            utime.sleep_ms(5)

        self.writeIt(b"\x04")  # ACK
        end = utime.ticks_ms() + 2500
        while utime.ticks_ms() < end:  # Wait for ack
            data = self.uart.read(1)
            if data == None:
                continue
            elif data == b"\x04":
                self.connected = True
                self.uart.deinit()  # We're done with slow UART
                break
            else:
                # We're getting crap data, there's probably no hub.
                self.uart.read(self.uart.any())  # Flush
                break

        if self.connected:
            self.last_nack = utime.ticks_ms()
            print("Successfully connected to hub")
            self.fast_uart()
            self.load_payload(b"\x00")
        else:
            print("Failed to connect to hub")
