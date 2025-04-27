# Trimmed version of pupremote that only runs on Pybricks hubs

import ustruct as struct
from pybricks.iodevices import PUPDevice
from pybricks.tools import wait
from micropython import const


MAX_PKT     = const(16)
#: OpenMV board platform type
OPENMV      = const(0)
#: LMS-ESP32 board platform type
ESP32       = const(1)

# Dictionary keys
NAME        = const(0)
SIZE        = const(1)
TO_HUB_FORMAT      = const(2)
FROM_HUB_FORMAT    = const(3)
CALLABLE    = const(4)

#: WeDo Ultrasonic sensor id
WEDO_ULTRASONIC = const(35)
#: SPIKE Color sensor id
SPIKE_COLOR = const(61)
#: SPIKE Ultrasonic sensor id
SPIKE_ULTRASONIC = const(62)

CALLBACK = const(0)
CHANNEL = const(1)

def connect(port):
    """
    Connect to LMS-ESP32. Pass Port as a string ('A') or a number (1=Port.A)
    """
    global pr
    if isinstance(port, str):
        pyport = eval('Port.'+port)
    if isinstance(port, int):
        pyport = eval('Port.'+chr(64+port))
    pr = PUPRemoteHub(pyport)

def call(*args):
    try:
        return pr.call(*args)
    except:
        print("Use the connect & add_channel or add_command blocks before call")
        raise

def add_channel(name, encoding):
    try:
        pr.add_channel(name, encoding)
    except:
        print("Use the connect command before adding a channel")
        raise

def add_command(name, to_hub, from_hub):
    try:
        pr.add_command(name, to_hub_fmt=to_hub, from_hub_fmt=from_hub)
    except:
        print("Use the connect command before adding a command")
        raise

class PUPRemote:
    """
    Base class for PUPRemoteHub and PUPRemoteSensor. Defines a list of commands
    and their formats. Contains encoding/decoding functions.
    """

    def __init__(self, max_packet_size=MAX_PKT):
        # Store commands, size and format
        self.commands = []
        # Store mode names (commands) to look up their index
        self.modes = {}
        # Optional override for max packet size for Pybricks compatibility
        self.max_packet_size = max_packet_size

    def add_channel(self, mode_name: str, to_hub_fmt: str =""):
        """
        Define a data channel to read on the hub. Use this function with identical parameters on both
        the sensor and the hub. You can call a channel like a command, but to update the data
        on the sensor side, you need to `update_channel(<name>, *args)`.

        :param mode_name: The name of the mode you defined on the sensor side.
        :type mode_name: str
        :param to_hub_fmt: The format string of the data sent from the sensor
            to the hub. Use 'repr' to receive any python object. Or use a struct format string,
            to receive a fixed size payload. See https://docs.python.org/3/library/struct.html

        :type to_hub_fmt: str
        """
        self.add_command(mode_name, to_hub_fmt=to_hub_fmt, command_type=CHANNEL)

    def add_command(
        self,
        mode_name: str,
        to_hub_fmt: str = "",
        from_hub_fmt: str = "",
        command_type=CALLBACK,
    ):
        """Define a remote call. Use this function with identical parameters on both
        the sensor and the hub.

        :param mode_name: The name of the mode you defined on the sensor side.
        :type mode_name: str
        :param to_hub_fmt: The format string of the data sent from the sensor
            to the hub. Use 'repr' to receive any python object. Or use a struct format string,
            to receive a fixed size payload. See https://docs.python.org/3/library/struct.html

        :type to_hub_fmt: str
        :param from_hub_fmt: The format string of the data sent from the hub
        :type from_hub_fmt: str

        """
        if to_hub_fmt == "repr" or from_hub_fmt == "repr":
            msg_size = self.max_packet_size
        else:
            size_to_hub_fmt = struct.calcsize(to_hub_fmt)
            size_from_hub_fmt = struct.calcsize(from_hub_fmt)
            msg_size = max(size_to_hub_fmt,size_from_hub_fmt )

        self.commands.append(
            {
            NAME: mode_name,
            TO_HUB_FORMAT: to_hub_fmt,
            SIZE: msg_size,
            }
        )
        if command_type == CALLBACK:
            self.commands[-1][FROM_HUB_FORMAT] = from_hub_fmt
            # self.commands[-1][CALLABLE] = eval(mode_name)

        # Build a dictionary of mode names and their index
        self.modes[mode_name] = len(self.commands)-1

    def decode(self, fmt: str, data: bytes):
        if fmt == "repr":
            # Remove trailing zero's (b'\x00') and eval the string
            clean = data.rstrip(b'\x00')
            if clean:
                return (eval(clean),)
            else:
                # Probably nothing left after stripping zero's
                return ('',)
            
        else:
            size = struct.calcsize(fmt)
            data = struct.unpack(fmt, data[:size])

        return data

    def encode(self, size, format, *argv):
        if format == "repr":
            s = bytes(repr(*argv), "UTF-8")
        else:
            s = struct.pack(format, *argv)

        assert len(s) <= size, "Payload exceeds maximum packet size"

        return s


class PUPRemoteHub(PUPRemote):
    """
    Class to communicate with a PUPRemoteSensor. Use this class on the hub side,
    on any hub that runs Pybricks. Copy the commands you defined on the sensor side
    to the hub side.

    :param port: The port to which the PUPRemoteSensor is connected.
    :type port: Port (Example: Port.A)
    :param max_packet_size: Set to 16 for Pybricks compatibility, defaults to 32.
    :type max_packet_size: int
    """
    
    def _int8_to_uint8(self,arr):
        return [((i+128)&0xff)-128 for i in arr]


    def __init__(self, port, max_packet_size=MAX_PKT):
        super().__init__(max_packet_size)
        self.port = port
        try:
            self.pup_device = PUPDevice(port)
        except OSError:
            self.pup_device = None
            print("Check wiring and remote script. Unable to connect on ", self.port)
            raise

    def add_command(self, mode_name, to_hub_fmt = "", from_hub_fmt = "", command_type=CALLBACK):
        super().add_command(mode_name, to_hub_fmt, from_hub_fmt, command_type)
        # Check the newly added commands against the advertised modes.
        modes = self.pup_device.info()['modes']
        n = len(self.commands)-1 # Zero indexed mode number
        assert len(self.commands) <= len(modes), "More commands than on remote side"
        assert mode_name == modes[n][0].rstrip(), \
            f"Expected '{modes[n][0].rstrip()}' as mode {n}, but got '{mode_name}'"
        assert self.commands[-1][SIZE] == modes[n][1], \
            f"Different parameter size than on remote side. Check formats."

    def call(self, mode_name: str, *argv, wait_ms=0):
        """
        Call a remote function on the sensor side with the mode_name you defined on both sides.

        :param mode_name: The name of the mode you defined on the sensor side.
        :type mode_name: str
        :param argv: As many arguments as you need to pass to the remote function.
        :type argv: Any
        :param wait_ms: The time to wait for the sensor to respond after
            a write from the hub, defaults to 0ms. This does not delay the read,
            i.e. when you don't pass any arguments, the read will happen immediately.
            A good value is the size of the write argument in bytes * 1.5ms
        :type wait_ms: int
        """
    
        mode = self.modes[mode_name]
        size = self.commands[mode][SIZE] 
        # Dummy read action to work around mode setting bug in Pybricks beta 2.2.0b8
        # Also check if a sensor or sensor emulator is connected.abs
        try:
            self.pup_device.read(mode)
        except:
            print("Check wiring and remote script. Unable to connect on ", self.port)
            raise

        if FROM_HUB_FORMAT in self.commands[mode]: 
            payl = self.encode(size, self.commands[mode][FROM_HUB_FORMAT], *argv)
            self.pup_device.write(
                mode, self._int8_to_uint8(tuple(payl + b"\x00" * (size - len(payl))))
            )
            wait(wait_ms)

     

        data = self.pup_device.read(mode)
        size=len(data)
        raw_data = struct.pack('%db'%size,*data)
        result = self.decode(
            self.commands[mode][TO_HUB_FORMAT],
            raw_data)
        # Convert tuple size 1 to single value
        if len(result)==1: 
            return result[0]
        else:
            return result
