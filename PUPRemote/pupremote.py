import ustruct as struct
try:
    from pybricks.iodevices import PUPDevice
except:
    pass

MAX_PKT=32

class PUPRemote:
    
    def __init__(self):
        self.commands = []
        self.msg_size = 0
           
    def add_command(self, mode_name: str, to_hub_fmt: str ="", from_hub_fmt: str="" ):
        """Add a command to call on the remote sensor unit.
        :param mode_name: The name of the mode you defined on the sensor side.
        :type mode_name: str
        :param to_hub_fmt: The format string of the data sent from the sensor 
        to the hub. Use 'repr' to receive any python object. Or use a struct format string,
        to receive a fixed size payload. See https://docs.python.org/3/library/struct.html
        :type to_hub_fmt: str"""
        cb=None
        self.writable = 0
        if to_hub_fmt == "repr" or from_hub_fmt == "repr":
            self.msg_size = 32
        else:
            size_to_hub_fmt = struct.calcsize(to_hub_fmt)
            size_from_hub_fmt = struct.calcsize(from_hub_fmt)
            self.msg_size = max(size_to_hub_fmt,size_from_hub_fmt )
            cb = "set_" + mode_name
        self.commands.append( {
            'name': mode_name,
            'to_hub_fmt': to_hub_fmt,
            'cb':cb,
            'from_hub_fmt': from_hub_fmt,
            'size':self.msg_size
            }
            )
        
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
            print("payload exceeds maximum packet size")
        else:
          payl = s + b'\x00' * (size-len(s))
        # this can be more efficient if lpf2.send_payload has byte array input
        return struct.unpack('%db'%size,payl)
    
class PUPRemoteSensor(PUPRemote):
    try:
        import lpf2 as LPF2
    except:
        pass
    def __init__(self, sensor_id=1, power=False):
        super().__init__()
        self.connected = False
        self.power = power
        self.mode_names = []
        self.lpup = self.LPF2.ESP_LPF2([],sensor_id=sensor_id)
        self.lpup.set_call_back(self.call_back)
    
    def add_command(self, mode_name: str,  to_hub_fmt: str ="", from_hub_fmt: str="" ):
        super().add_command(mode_name, to_hub_fmt = to_hub_fmt, from_hub_fmt = from_hub_fmt)
        writeable=0
        if from_hub_fmt != "":
            writeable = self.LPF2.ABSOLUTE
        max_mode_name_len = 5 if self.power else MAX_PKT
        if len(mode_name) > max_mode_name_len:
                print('Error: mode_name should not be longer than %d%s.' % (max_mode_name_len," if power=True" if self.power else ""))
        else: # only enable power when len(mode_name)<=5
            if self.power:
                mode_name = mode_name.encode('ascii') + b'\x00'*(5-len(mode_name)) + b'\x00\x80\x00\x00\x00\x05\x04'
        self.lpup.modes.append( self.lpup.mode(mode_name, self.msg_size,self.LPF2.DATA8,writeable) )

    def process(self):
        # Call this function in your main loop, prefferably at least once every 20ms.
        # It will handle the communication with the LEGO Hub, connect to it if needed,
        # and call the registered commands.
        self.lpup.heartbeat()
        mode=self.lpup.current_mode
        # execute the command
        to_hub_fmt=self.commands[mode]['to_hub_fmt']
        result = eval(self.commands[mode]['name'])()
        size=self.commands[mode]['size']
        payload = self.encode(size,to_hub_fmt,*result)
        self.lpup.send_payload(self.LPF2.DATA8, list(payload))
        return self.connected
    
    def call_back(self,size,data):
        # data is received from hub
        mode=self.lpup.current_mode
        mode_name = self.commands[mode]
        format = self.commands[mode]['from_hub_fmt']
        cb = eval(self.commands[mode]['cb'])
        cb(*self.decode(format,data))
        
     

class PUPRemoteHub(PUPRemote):
    def __init__(self, port, power = False):
        super().__init__()
        self.modes = {}
        try:
            self.pup_device=PUPDevice(port)
        except:
            print("PUPRemote device not ready on port",port)

    def add_command(self, mode_name: str, to_hub_fmt: str ="", from_hub_fmt: str=""):
        super().add_command( mode_name,  to_hub_fmt = to_hub_fmt, from_hub_fmt = from_hub_fmt)
        self.modes[mode_name] = len(self.commands)-1
    
    def write(self,mode_name,*argv):
        mode = self.modes[mode_name]
        from_hub_fmt = self.commands[mode]['from_hub_fmt']
        size = self.commands[mode]['size']
        payl = self.encode(size,from_hub_fmt,*argv)
        discard = self.pup_device.read(mode) # dummy read to set mode
        self.pup_device.write(mode,payl)
  
    def read(self,mode_name): # data just vtemporaily added for testing
        mode = self.modes[mode_name]
        to_hub_fmt = self.commands[mode]['to_hub_fmt']
        data = self.pup_device.read(mode)
        size=len(data)
        raw_data = struct.pack('%db'%size,*data)
        result = self.decode(to_hub_fmt,raw_data)
        return result

