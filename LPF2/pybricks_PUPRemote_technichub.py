from pybricks.hubs import TechnicHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch
from pybricks.iodevices import PUPDevice


hub = TechnicHub()

from pybricks.hubs import TechnicHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

from pybricks.iodevices import PUPDevice


hub = TechnicHub()

    

import ustruct as struct
MAX_PKT=32

class PUPRemoteHub:
    def __init__(self,port):
        self.commands = []
        self.mode_names = {}
        try:
            self.pup_device=PUPDevice(port)
        except:
            print("PUPRemote device not ready on port",port)

    
    def add_command(self, mode_name: str, format_pup_to_hub: str,*argv):
        format_hub_to_pup=""
        cb=None
        if argv:
            format_hub_to_pup=argv[0]
            
            
        if format_pup_to_hub == "repr" or format_hub_to_pup == "repr":
            size = 32
        else:
            size_pup_to_hub=struct.calcsize(format_pup_to_hub)
            size_hub_to_pub=struct.calcsize(format_hub_to_pup)
            size=max(size_pup_to_hub,size_hub_to_pub)


        self.commands.append( {
            'name': mode_name,
            'format_pup_to_hub': format_pup_to_hub,
            'cb':cb,
            'format_hub_to_pup': format_hub_to_pup,
            'size':size
            }
            )
        self.mode_names[mode_name]=len(self.commands)-1
        #self.lpup.modes.append( self.lpup.mode(mode_name, size) )
        # Reconnect as needed with new mode if we are already connected.
        #self.disconnect()
    
    def decode(self, format, data):
        if format=='repr':
            return eval(data.replace(b'\x00',b'')) # strip zero's
        else:
            size=struct.calcsize(format)
            data=struct.unpack(format,data[:size])
            if len(data)==1:
            # convert from tuple size 1 to single value
              data=data[0]
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
    
    
    def write(self,mode_name,*argv):
        mode = self.mode_names[mode_name]
        format_hub_to_pup = self.commands[mode]['format_hub_to_pup']
        size = self.commands[mode]['size']
        payl = self.encode(size,format_hub_to_pup,*argv)
        discard = self.pup_device.read(mode) # dummy read to set mode
        self.pup_device.write(mode,payl)
        
  
    def read(self,mode_name): # data just vtemporaily added for testing
        mode = self.mode_names[mode_name]
        format_pup_to_hub=self.commands[mode]['format_pup_to_hub']
        data = self.pup_device.read(mode)
        size=len(data)
        raw_data=struct.pack('%db'%size,*data)
        result = self.decode(format_pup_to_hub,raw_data)
        return result


p=PUPRemoteHub(Port.A)
p.add_command('rgb','BBB','BBB')
p.add_command('gyro','8B','8B')
print('gyro:',p.read('gyro'))
p.write('gyro',*[i for i in range(8)])
p.write('rgb',5,6,7)
for i in range(5):
    print(p.read('rgb'))
    wait(20)
