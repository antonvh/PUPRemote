from pybricks.hubs import InventorHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch
from pybricks.iodevices import PUPDevice


hub = InventorHub()

    

import ustruct as struct
MAX_PKT=32


def next_power_of_2(v):
  v-=1
  v |= v >> 1
  v |= v >> 2
  v |= v >> 4
  v+=1
  return v

class PUPRemoteHub:
    def __init__(self):
        self.commands = []
        self.mode_names = {}
        self.pup_device=None

    
    def add_command(self, mode_name: str, format_pup_to_hub: str,*argv):
        format_hub_to_pup=""
        cb=None
        if argv:
            cb = argv[0]
            format_hub_to_pup=argv[1]
            
            
        if format_pup_to_hub == "repr" or format_hub_to_pup == "repr":
            size = 32
        else:
            size_pup_to_hub=struct.calcsize(format_pup_to_hub)
            size_hub_to_pub=struct.calcsize(format_hub_to_pup)
            size=next_power_of_2(max(size_pup_to_hub,size_hub_to_pub))

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
    
    def add_port(self,port):
            try:
                self.pup_device=PUPDevice(port)
            except:
                print("PUPdevice not ready on port",port)

    def decode(self, format, data):
        if format=='repr':
            return eval(data.replace(b'\x00',b'')) # strip zero's
        else:
            size=struct.calcsize(format)
            data=struct.unpack(format,data[:size])
            if len(data)==1:
            # convert from tuple size 1 to single value
              data=data[0]
        if all(d == 0 for d in data): # check for all zero's
          data=None
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
        print(payl)
        self.pup_device.write(mode,payl)
        
  
    def read(self,mode_name): # data just vtemporaily added for testing
        mode = self.mode_names[mode_name]
        format_pup_to_hub=self.commands[mode]['format_pup_to_hub']
        data = self.pup_device.read(mode)
        size=len(data)
        raw_data=struct.pack('%db'%size,*data)
        result = self.decode(format_pup_to_hub,raw_data)
        return result


p=PUPRemoteHub()
p.add_command('rgb','BBB')
p.add_command('gyro','HHH','set_gyro','BB')
p.add_port(Port.A)
print(p.read('gyro'))
p.write('gyro',123,222)
for i in range(20):
    print(p.read('rgb'))
    wait(100)