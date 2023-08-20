= changes made

== Not working:

- sending 'repr' format data to the sensor

== LPF2


in `def load_payload`

added expetion for single valued float or ints.
```
        elif isinstance(data,float) or isinstance(data,int):
            bin_data = struct.pack(format[data_type], data)

```

removed default payload line 193
```
                    # TODO: make size calculation on mode creation
                    size = self.modes[mode][1][0]
                    dtype = self.modes[mode][1][1]
                    bsize = size * 2 ** dtype
                    if len(self.payload) != bsize+2:
                        self.send_payload(bsize * [0])

```

added uart config to object
```

    def __init__(self, modes, sensor_id=WeDo_Ultrasonic):
        self.tx_pin_nr = 19
        self.rx_pin_nr = 18
        self.uartchannel = 2
        super().__init__(modes, sensor_id)

```


== PUPRemote

always send a value to the hub if there is a format defined fot TO_HUB_FORMAT

```        # if there is a value to be send to the hub, get that value
        if self.commands[mode][TO_HUB_FORMAT]:
            result = eval(self.commands[mode][NAME])()
```
