# This is a high level API for the LPF2 protocol. It is designed to be used with the 
# ESP32 and the LEGO Hub, similar to uartremote.py.


import gc,utime
import micropython
import lpf2_new as LPF2
from utime import ticks_ms
import struct

MAX_PKT=32


def next_power_of_2(v):
  v-=1
  v |= v >> 1
  v |= v >> 2
  v |= v >> 4
  v+=1
  return v
  
def cb(size,buf):
    print('cb')
    print(size,buf)

class PUPRemoteSensor:
 
    def __init__(self):
        self.connected = False
        self.commands = []
        self.mode_names = []
        self.lpup = LPF2.ESP_LPF2([])
        self.lpup.set_call_back(self.call_back)
        
 
    
    def add_command(self, mode_name: str, format_pup_to_hub: str,*argv):
        """
        Add a command for remote calling. And set up the matching LPUP mode.
        """
        
        format_hub_to_pup=""
        cb=None
        writable = 0
        if argv:
            format_hub_to_pup=argv[0]
            writable = LPF2.ABSOLUTE
            
        if format_pup_to_hub == "repr" or format_hub_to_pup == "repr":
            size = 32
        else:
            size_pup_to_hub=struct.calcsize(format_pup_to_hub)
            size_hub_to_pub=struct.calcsize(format_hub_to_pup)
            size=next_power_of_2(max(size_pup_to_hub,size_hub_to_pub))
            cb = "set_" + mode_name
        self.commands.append( {
            'name': mode_name,
            'format_pup_to_hub': format_pup_to_hub,
            'cb':cb,
            'format_hub_to_pup': format_hub_to_pup,
            'size':size
            }
            )
        self.lpup.modes.append( self.lpup.mode(mode_name, size,LPF2.DATA8,writable) )
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
    
    def process(self):
        # Call this function in your main loop, prefferably at least once every 20ms.
        # It will handle the communication with the LEGO Hub, connect to it if needed,
        # and call the registered commands.
        #if not self.connected:
        #    # Advertise once and check if the LEGO Hub is connects.
        #    self.connected = self.lpup.initialize()
        #else:
        self.lpup.heartbeat()
        mode=self.lpup.current_mode
        # execute the command
        format_pup_to_hub=self.commands[mode]['format_pup_to_hub']
        result = eval(self.commands[mode]['name'])()
        size=self.commands[mode]['size']
        #print("format_pup_to_hub,*result",format_pup_to_hub,result)
        payload = self.encode(size,format_pup_to_hub,*result)
        self.lpup.send_payload('Int8', list(payload))
        return self.connected
    
    def call_back(self,size,data):
        # data is received from hub
      
        mode=self.lpup.current_mode
        mode_name = self.commands[mode]
        format = self.commands[mode]['format_hub_to_pup']
        #print("call_back",mode,mode_name,format,data)
        cb = eval(self.commands[mode]['cb'])
        cb(*self.decode(format,data))
        
        
        
