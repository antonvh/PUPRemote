# This is a high level API for the LPF2 protocol. It is designed to be used with the 
# ESP32 and the LEGO Hub, similar to uartremote.py.


import gc,utime
import micropython
import lpf2_new as LPF2
from utime import ticks_ms
import struct


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
        self.commands = {}
        self.lpup = LPF2.ESP_LPF2()
        
    def add_command(self, command: callable, mode_name: str, return_format: str):
        """
        Add a command for remote calling. And set up the matching LPUP mode.
        """
        if return_format == "repr":
            size = 32
        else:
            size = struct.calcsize(return_format)
        
        self.commands[mode_name] = {
            'command': command,
            'format': return_format,
        }
        self.lpup.modes.append( self.lpup.mode(mode_name, size) )
        # Reconnect as needed with new mode if we are already connected.
        self.disconnect()
    
    def decode(self, size, buf):
        pass

    def process(self):
        """
        Call this function in your main loop, prefferably at least once every 20ms.
        It will handle the communication with the LEGO Hub, connect to it if needed,
        and call the registered commands.
        """
        if not self.connected:
            # Advertise once and check if the LEGO Hub is connects.
            self.connected = self.lpup.advertise()
        else:
            self.lpup.hearbeat()
            mode=self.lpup.current_mode
            # execute the command
            lpup_fmt, payload = self.encode(
                self.commands[mode](),
                self.commands[mode]['format']
            )
            self.lpup.send_payload(lpup_fmt, payload)
        return self.connected
        
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
    
