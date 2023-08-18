try:
    import ustruct as struct
except ImportError:
    import struct

try:
    from micropython import const
except ImportError:
    # micropython.const() is not available on normal Python
    # but we can use a normal function instead for unit tests
    def const(x):
        return x

MAX_PKT     = const(32)
OPENMV      = const(0)
ESP32       = const(1)
NAME        = const(0)
SIZE        = const(1)
TO_HUB_FORMAT      = const(2)
FROM_HUB_FORMAT    = const(3)
CALLBACK    = const(4)



class PUPRemote:
    """
    Base class for PUPRemoteHub and PUPRemoteSensor. Defines a list of commands
    and their formats. Contains encoding/decoding functions.
    """
    
    def __init__(self):
        # Store commands, their callbacks, size and format
        self.commands = []
        self.modes = {}
           
    def add_command(self, mode_name: str, to_hub_fmt: str ="", from_hub_fmt: str="" ):
        """Define a remote call. Use this function with identical parameters on both 
        the sensor and the hub.

        :param mode_name: The name of the mode you defined on the sensor side.
        :type mode_name: str
        :param to_hub_fmt: The format string of the data sent from the sensor 
        to the hub. Use 'repr' to receive any python object. Or use a struct format string,
        to receive a fixed size payload. See https://docs.python.org/3/library/struct.html
        :type to_hub_fmt: str"""
        cb=None
        self.writable = 0
        if to_hub_fmt == "repr" or from_hub_fmt == "repr":
            msg_size = 32
        else:
            size_to_hub_fmt = struct.calcsize(to_hub_fmt)
            size_from_hub_fmt = struct.calcsize(from_hub_fmt)
            msg_size = max(size_to_hub_fmt,size_from_hub_fmt )
            cb = "set_" + mode_name
        self.commands.append( 
                {
                NAME: mode_name,
                TO_HUB_FORMAT: to_hub_fmt,
                CALLBACK: cb,
                FROM_HUB_FORMAT: from_hub_fmt,
                SIZE: msg_size,
                }
            )
        # Build a dictionary of mode names and their index
        self.modes[mode_name] = len(self.commands)-1
        
    def decode(self, format, data):
        if format=='repr':
            return eval(data.replace(b'\x00', b'')) # strip zero's
        else:
            size = struct.calcsize(format)
            data = struct.unpack(format, data[:size])
            if len(data)==1:
            # convert from tuple size 1 to single value
               data=data[0]
        return data

    def encode(self, size, format, *argv):
        if format=="repr":
            s=repr(*argv)
        else:
            s=struct.pack(format,*argv)
        if len(s) > MAX_PKT or len(s) > size:
            print("Payload exceeds maximum packet size")
        else:
          payl = s + b'\x00' * (size-len(s))
        # this can be more efficient if lpf2.send_payload has byte array input
        return struct.unpack('%db'%size,payl)
    
class PUPRemoteSensor(PUPRemote):
    try:
        import lpf2 as LPF2
    except:
        pass
    def __init__(self, sensor_id=1, power=False, platform=ESP32):
        super().__init__()
        self.connected = False
        self.power = power
        self.mode_names = []

        if platform == ESP32:
            self.lpup = self.LPF2.ESP_LPF2([],sensor_id=sensor_id)
        elif platform == OPENMV:
            self.lpup = self.LPF2.OpenMV_LPF2([],sensor_id=sensor_id)
        self.lpup.set_call_back(self.call_back)
    
    def add_command(self, mode_name: str,  to_hub_fmt: str ="", from_hub_fmt: str="" ):
        super().add_command(mode_name, to_hub_fmt = to_hub_fmt, from_hub_fmt = from_hub_fmt)
        writeable=0
        if from_hub_fmt != "":
            writeable = self.LPF2.ABSOLUTE
        max_mode_name_len = 5 if self.power else MAX_PKT
        if len(mode_name) > max_mode_name_len:
                print("Error: mode_name can't be longer than %d%s." % (max_mode_name_len," if power=True" if self.power else ""))
        else: # only enable power when len(mode_name)<=5
            if self.power:
                mode_name = mode_name.encode('ascii') + b'\x00'*(5-len(mode_name)) + b'\x00\x80\x00\x00\x00\x05\x04'
        self.lpup.modes.append( self.lpup.mode(mode_name, self.commands[mode_name][SIZE] , self.LPF2.DATA8,writeable) )

    def process(self):
        # Call this function in your main loop, prefferably at least once every 20ms.
        # It will handle the communication with the LEGO Hub, connect to it if needed,
        # and call the registered commands.
        self.lpup.heartbeat()
        mode=self.lpup.current_mode
        # execute the command
        to_hub_fmt=self.commands[mode][TO_HUB_FORMAT]
        result = eval(self.commands[mode][NAME])()
        size=self.commands[mode][SIZE] 
        payload = self.encode(size,to_hub_fmt,*result)
        self.lpup.send_payload(self.LPF2.DATA8, list(payload))
        return self.connected
    
    def call_back(self,size,data):
        # data is received from hub
        mode=self.lpup.current_mode
        mode_name = self.commands[mode]
        format = self.commands[mode][FROM_HUB_FORMAT]
        cb = eval(self.commands[mode][CALLBACK])
        cb(*self.decode(format,data))
        
     

class PUPRemoteHub(PUPRemote):
    """
    Class to communicate with a PUPRemoteSensor. Use this class on the hub side,
    on any hub that runs Pybricks. You can enable 8V power on the M+ wire,
    so the buck converter on the SPIKE-OPENMV or LMS-ESP32 board side can supply high 
    currents (op to 1700mA) to your appliances.

    :param port: The port to which the PUPRemoteSensor is connected.
    :type port: Port (Example: Port.A)
    :param power: Set to True if the PUPRemoteSensor needs 8V power on M+ wire.
    :type power: bool
    """
    
    def __init__(self, port, power = False):
        try:
            from pybricks.iodevices import PUPDevice
        except:
            pass
        super().__init__()
        
        self.port = port
        try:
            self.pup_device=PUPDevice(port)
        except OSError:
            self.pup_device=None
            print("PUPDevice not ready on port",port)

    def call(self, mode_name, *argv):
        try:
            if mode_name[:4] == 'set_':
                mode_name = mode_name [4:]
                mode = self.modes[mode_name]
                from_hub_fmt = self.commands[mode][FROM_HUB_FORMAT]
                size = self.commands[mode][SIZE] 
                payl = self.encode(size,from_hub_fmt,*argv)
                self.pup_device.read(mode) # dummy read to set mode
                self.pup_device.write(mode,payl)
            else:
                mode = self.modes[mode_name]
                to_hub_fmt = self.commands[mode][TO_HUB_FORMAT]
                data = self.pup_device.read(mode)
                size=len(data)
                raw_data = struct.pack('%db'%size,*data)
                result = self.decode(to_hub_fmt,raw_data)
                return result
        except OSError:
            print("PUPDevice not ready on port", self.port)
           


