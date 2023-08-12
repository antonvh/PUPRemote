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

   
    def add_command(self, mode_name: str, format_pup_to_hub: str,*argv):
        format_hub_to_pup=""
        cb=None
        self.writable = 0
        if argv:
            format_hub_to_pup=argv[0]

            
        if format_pup_to_hub == "repr" or format_hub_to_pup == "repr":
            self.msg_size = 32
        else:
            size_pup_to_hub=struct.calcsize(format_pup_to_hub)
            size_hub_to_pub=struct.calcsize(format_hub_to_pup)
            self.msg_size=max(size_pup_to_hub,size_hub_to_pub)
            cb = "set_" + mode_name
        self.commands.append( {
            'name': mode_name,
            'format_pup_to_hub': format_pup_to_hub,
            'cb':cb,
            'format_hub_to_pup': format_hub_to_pup,
            'size':self.msg_size
            }
            )
        
    def decode(self, format, data):
        if format=='repr':
            return eval(data.replace(b'\x00',b'')) # strip zero's
        else:
            size=struct.calcsize(format)
            data=struct.unpack(format,data[:size])
            if len(data)==1:
            # convert from tuple size 1 to single value
              data=data[0]
        #if all(d == 0 for d in data): # check for all zero's
        #  data=None
        return data

    def encode(self,size,format,*argv):
        if format=="repr":
            s=repr(*argv)
        else:
            s=struct.pack(format,*argv)
        if len(s)>MAX_PKT or len(s)>size:
            print("payload exceeds maximum packet size")
        else:
          payl = s+b'\x00'*(size-len(s))
        # this can be more efficient if lpf2.send_payload has byte array input
        return struct.unpack('%db'%size,payl)
    
class PUPRemoteSensor(PUPRemote):
    try:
        import lpf2 as LPF2
    except:
        pass
    def __init__(self, sensor_id=1):
        super().__init__()
        self.connected = False
        self.mode_names = []
        self.lpup = self.LPF2.ESP_LPF2([],sensor_id=sensor_id)
        self.lpup.set_call_back(self.call_back)
    
    def add_command(self, mode_name: str, format_pup_to_hub: str,*argv):
        super().add_command(mode_name, format_pup_to_hub,*argv)
        writeable=0
        if argv:
            writeable = self.LPF2.ABSOLUTE
        self.lpup.modes.append( self.lpup.mode(mode_name, self.msg_size,self.LPF2.DATA8,writeable) )

    def process(self):
        # Call this function in your main loop, prefferably at least once every 20ms.
        # It will handle the communication with the LEGO Hub, connect to it if needed,
        # and call the registered commands.
        self.lpup.heartbeat()
        mode=self.lpup.current_mode
        # execute the command
        format_pup_to_hub=self.commands[mode]['format_pup_to_hub']
        result = eval(self.commands[mode]['name'])()
        size=self.commands[mode]['size']
        payload = self.encode(size,format_pup_to_hub,*result)
        self.lpup.send_payload(self.LPF2.DATA8, list(payload))
        return self.connected
    
    def call_back(self,size,data):
        # data is received from hub
      
        mode=self.lpup.current_mode
        mode_name = self.commands[mode]
        format = self.commands[mode]['format_hub_to_pup']
        cb = eval(self.commands[mode]['cb'])
        cb(*self.decode(format,data))
        
     

class PUPRemoteHub(PUPRemote):
    def __init__(self, port):
        super().__init__()
        self.modes = {}
        #try:
        self.pup_device=PUPDevice(port)
        #except:
        #    print("PUPRemote device not ready on port",port)

    
    def add_command(self, mode_name: str, format_pup_to_hub: str,*argv):
        super().add_command( mode_name, format_pup_to_hub,*argv)
        self.modes[mode_name]=len(self.commands)-1
    
    def write(self,mode_name,*argv):
        mode = self.modes[mode_name]
        format_hub_to_pup = self.commands[mode]['format_hub_to_pup']
        size = self.commands[mode]['size']
        payl = self.encode(size,format_hub_to_pup,*argv)
        discard = self.pup_device.read(mode) # dummy read to set mode
        self.pup_device.write(mode,payl)
        
  
    def read(self,mode_name): # data just vtemporaily added for testing
        mode = self.modes[mode_name]
        format_pup_to_hub=self.commands[mode]['format_pup_to_hub']
        data = self.pup_device.read(mode)
        size=len(data)
        raw_data=struct.pack('%db'%size,*data)
        result = self.decode(format_pup_to_hub,raw_data)
        return result

