from machine import SoftI2C, Pin

REG_GET_CMD_ID = 0x02
REG_PLAY_CMD_ID = 0x03

REG_SET_VOL = 0x05

CMD_IDS = {
    0: '?',
    2: 'Yes',
    22: 'Go forward',
    25: 'Turn left ninety degrees',
    28: 'Turn right ninety degrees',
    23: 'Retreat',
    
}

class SENS0539:
    def __init__(self, i2c=None, addr=0x64):
        if i2c is None:
            i2c = SoftI2C(scl=Pin(2), sda=Pin(26))
        self.i2c = i2c
        self.addr = addr

    def get_cmd_id(self):
        id = self.i2c.readfrom_mem(self.addr, REG_GET_CMD_ID, 1)

        return id[0]
    
