from pupremote import PUPRemoteSensor
from utime import ticks_ms

WeDo_Ultrasonic, SPIKE_Color, SPIKE_Ultrasonic = 35, 61, 62

count = 0
def rgb():
    global count
    count+=1
    count%=30
    return count,count*2,count*3

def set_rgb(*argv):
    print("set_rgb",argv)

def gyroscoop():
    resp = [i+1 for i in range(8)]
    return resp

def set_gyroscoop(*argv):
    print('set_gyro',argv)
    
    
def cb(size,buf):
    print(size,buf)
    
p=PUPRemoteSensor(sensor_id=SPIKE_Ultrasonic)
# self, command: callable, mode_name: str, format_hub_to_pup: str,*argv):
p.add_command('rgb','BBB','BBB')
p.add_command('gyroscoop','8B','8B')

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

