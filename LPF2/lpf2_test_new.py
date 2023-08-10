import gc,utime
import micropython
import lpf2_new as LPF2
from utime import ticks_ms
#from machine import Pin
#micropython.alloc_emergency_exception_buf(200)

#modes = [
#LPF2.mode('int8',type = LPF2.DATA8),
#LPF2.mode('int16', type = LPF2.DATA16),
#LPF2.mode('int32', type = LPF2.DATA32),
#LPF2.mode('float', format = '2.1', type = LPF2.DATAF),
#LPF2.mode('int8_array',size = 4, type = LPF2.DATA8),
#LPF2.mode('int16_array',size = 4, type = LPF2.DATA16),
#LPF2.mode('int32_array',size = 4, type = LPF2.DATA32),
#LPF2.mode('float_array',size = 4, format = '2.1', type = LPF2.DATAF)
#]

# Name, Format [# datasets, type, figures, decimals],
# raw [min,max], Percent [min,max], SI [min,max], Symbol, functionMap [map in:data send type, map out: data rcv type], view in telemetry
mode0 = ['LPF2-DETECT',[32,LPF2.DATA8,5,0],[0,1023],[0,100],[0,1023],'',[LPF2.ABSOLUTE,LPF2.ABSOLUTE],True]
mode1 = ['LPF2-COUNT',[2,LPF2.DATA16,5,0],[0,100],[0,100],[0,100],'CNT',[LPF2.ABSOLUTE,0],True]
mode2 = ['LPF2-CAL',[1,LPF2.DATAF,8,3],[0,1023],[0,100],[0,1023],'RAW',[LPF2.ABSOLUTE,LPF2.ABSOLUTE],False]
modes2 = [mode0,mode1,mode2]

#led = Pin(2, mode=Pin.OUT)
#led.on()

lpf2 = LPF2.ESP_LPF2(modes2, type=LPF2.SPIKE_Ultrasonic, timer = 1, freq = 20)    # ESP
#lpf2 = LPF2.Prime_LPF2(1, 'Y1', 'Y2', modes, LPF2.SPIKE_Ultrasonic, timer = 4, freq = 5)    # PyBoard
# use EV3_LPF2 or Prime_LPF2 - also make sure to select the port type on the EV3 to be ev3-uart

lpf2.initialize()

def cb(size,buf):
    print('own callback')
    print(size,[i for i in buf])

lpf2.set_call_back(cb)

                 
value = 0

last_heartbeat = ticks_ms()
last_send = ticks_ms()
# Loop
while True:
    if (ticks_ms() - last_heartbeat > 20):
        last_heartbeat = ticks_ms()
        lpf2.heartbeat()
        #if not lpf2.connected:
        #      utime.sleep_ms(200)
                  
        #else:
          #led.off()
        if ((ticks_ms() - last_send)>1000) and lpf2.connected:
              last_send=ticks_ms()
              if value < 9:
                  value = value + 1
              else:
                  value = 0

              mode=lpf2.current_mode
              print(mode)
              if mode==0:
                  lpf2.send_payload('Int8',[value*i for i in range(32)])
              elif mode==1:
                  lpf2.send_payload('Int16',[32767,65535])
              elif mode==2:
                  lpf2.send_payload('float',value*1.010101)
              print(value)
          