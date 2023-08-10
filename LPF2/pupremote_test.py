#import PUPremote
from utime import ticks_ms

count = 0
def rgb():
    global count
    count+=1
    count%=30
    return count,count*2,count*3

def gyro():
    return 1123,3221,2321

def set_gyro(r,v):
    print('set_gyro',r,v)
    
    
def cb(size,buf):
    print(size,buf)
    
p=PUPRemoteSensor()
# self, command: callable, mode_name: str, format_hub_to_pup: str,*argv):
p.add_command('rgb','BBB')
p.add_command('gyro','HHH','BB')

last_heartbeat = ticks_ms()
last_send = ticks_ms()
# Loop
while True:
    if (ticks_ms() - last_heartbeat > 20):
        last_heartbeat = ticks_ms()
        state=p.process()
        #if not lpf2.connected:
        #      utime.sleep_ms(200)
                  
        #else:

