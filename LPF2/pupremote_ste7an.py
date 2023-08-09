# This is a high level API for the LPF2 protocol. It is designed to be used with the 
# ESP32 and the LEGO Hub, similar to uartremote.py.


import gc,utime
import micropython
import lpf2_new as LPF2
from utime import ticks_ms
import struct

def next_power_of_2(v):
  v-=1
  v |= v >> 1
  v |= v >> 2
  v |= v >> 4
  v+=1
  return v
  
  

class PUPRemoteSensor():
    """
    Use this class on your custom electronics sensor or camera board.
    It will handle the communication with the LEGO Hub.
    :example:

        .. code-block:: python

        def read_sensor():
            global sensor_value
            return sensor_value

        def adjust_sensor_settings(settings:dict):
            pass

        lp = PUPRemoteSensor(uart)
        # Add a command for remote calling.
        # Pass a 5 character string as the command name.
        # and a struct format string for the return value.
        lp.add_command(read_sensor, "MYSENS", "bbb")
        # The repr format string is default and optional. It will repr/eval the return value.
        lp.add_command(adjust_sensor_settings, "MYSETT", "repr")
        
        while True:
            # Update all sensor values, process images etc.
            sensor.update()
            # Process incoming commands and send requested data.
            # Returns True if the LEGO Hub is (still) connected.
            connected = lp.process()
    """
    def __init__(self, uart):
        self.uart = uart
        self.connected = False
        self.commands = []
        self.mode_names = []
        self.lpup = LPF2.ESP_LPF2()
        self.lpup.set_call_back = self.call_back
        
 
    
    def add_command(self, command: callable, mode_name: str, format_hub_to_pup: str,*argv):
        """
        Add a command for remote calling. And set up the matching LPUP mode.
        """
        format_hub_to_pup=""
        cb=None
        if argv:
            format_hub_to_pup=argv[0]
            cb = argv[1]
            
        if format_pup_to_hub == "repr" or format_hub_to_pup == "repr":
            size = 32
        else:
            size_pup_to_hub=struct.calcsize(format_pup_to_hub)
            size_hub_to_pub=struct.calcsize(format_hub_to_pup)
            size=next_power_of_2(max(size_pup_to_hub,size_hub_to_pub))

        self.commands.append( {
            'command': command,
            'format_pup_to_hub': format_pup_to_hub,
            'cb':cb,
            'format_hub_to_pup': format_hub_to_pup,
            'size':size
            }
            )
        self.lpup.modes.append( self.lpup.mode(mode_name, size) )
        # Reconnect as needed with new mode if we are already connected.
        self.disconnect()
    
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
        
        
    def process(self):
        """
        Call this function in your main loop, prefferably at least once every 20ms.
        It will handle the communication with the LEGO Hub, connect to it if needed,
        and call the registered commands.
        """
        if not self.connected:
            # Advertise once and check if the LEGO Hub is connects.
            self.connected = self.lpup.initialize()
        else:
            self.lpup.hearbeat()
            mode=self.lpup.current_mode
            # execute the command
            format_pup_to_hub=self.commands[mode]['format_pup_to_hub']
            payload = encode(format_pup_to_hub,self.commands[mode]['command']())
            self.lpup.send_payload(LPF2.DATA8, *payload)
        return self.connected
    
    def call_back(self,mode,data):
        # data is received from hub
        mode_name = self.mode_names[mode]
        format = commands[mode]['format_hub_to_pup']
        cb = commands[mode]['cb']
        cb(*decode(format,data))
        
        
        
class PUPRemoteHub():
    """
    Use this class on your LEGO hub.
    It will handle the communication with the remote sensor.

    Even better would be if would add custom bound methods...
    https://stackoverflow.com/questions/972/adding-a-method-to-an-existing-object-instance-in-python
    
    :example:
        
        .. code-block:: python
        
        """
    def __init__(self, port, format_map=None):
        self.lpup = PUPDevice(port)
        if format_map is None:
            format_map = {
                'ECHO': 'repr',
            }

    def call(self, mode, payload=None):
        """
        Call a procedure on the remote sensor.
        """
        self.lpup.write(mode, payload)
        data = self.lpup.read(mode)
        return self.decode(data, self.format_map[mode])
    