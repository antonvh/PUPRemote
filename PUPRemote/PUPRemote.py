# the mode dicttionary is still based on LPF2.py format. In a later stage, this can be migrated to the PUPDeviceEmulator class.
#
# The functions are compatible with the limited MicroPython implementation of PyBricks
import struct

DATA8,DATA16,DATA32,DATAF = 0,1,2,3  # Data type codes
ABSOLUTE,RELATIVE,DISCRETE = 16,8,4
MAK_PKT=14


class PUPRemote:
  def __init__(self):
    self.mode_list=[]
    self.command_mode_dict={}
    self.mode_command=[]
    # {'gyro':{'f_P_h':'HHH','f_h_P','BB','mode':1},'rgb':{f_P_h':'HHH','mode':2}}

  
  def encode(self,format_string,*argv):
    print("argv=",*argv)
    if argv:
        #try:
            f = format_string
            # struct pack
            s = struct.pack(f, *argv)
            f = bytes(f,'utf-8')
            f = f[:-1] + bytes( (f[-1]|0x80,) ) # mark end of fmt stringf = bytes(f,'utf-8')
            s = f + s
        #except:
        #  pass
    else:
      s=b''      
    #print(s)
    if len(s)>MAX_PKT:
        raise Exception("Sorry, payload length exceeds 15 bytes")
    # s = bytes((len(s),)) + s
    return s+b'\x00'*(MAX_PKT-len(s))

  def decode(self,data):
    len_f=0
    while (len_f<MAX_PKT) and data[len_f]&0x80==0:
        len_f+=1
    if len_f!= MAX_PKT:
      f=data[:len_f]+bytes((data[len_f]&0x7f,))
      #print('fmt=',f)
      #print(data[len_f+1:len_f+1+len_s])
      len_s=struct.calcsize(f)
      data=struct.unpack(f,data[len_f+1:len_f+1+len_s])
      if len(data)==1:
          # convert from tuple size 1 to single value
          data=data[0]
    if all(d == 0 for d in data): # check for all zero's
          data=None
  
    return data


  def add_mode(self,command_name):
    default_mode=[command_name,[32,DATA8,3,0],[0,1023],[0,100],[0,1023],'RAW',[ABSOLUTE,ABSOLUTE],False]
    self.mode_list.append(default_mode)
    self.command_mode_dict[command_name]['mode']=len(self.mode_list) # add last added mode ad number.
    self.mode_command.append(command_name)

  def add_command(self,command_name,format_pup_to_hub,*argv):
    if argv:
       format_hub_to_pup=argv[0]
       call_back=argv[1]
    else:
      format_hub_to_pup=''
      call_back=None
    self.command_mode_dict[command_name]={'f_P_h':format_pup_to_hub,'f_h_P':format_hub_to_pup,'cb':call_back}
    self.add_mode(command_name)


  def send(self,command_name,*argv):
    format_pup_to_hub=self.command_mode_dict[command_name]['f_P_h']
    print(format_pup_to_hub,*argv)
    payl=encode(format_pup_to_hub,*argv)
    print(payl)

  def read(self,command_name,data): # data just vtemporaily added for testing
    format_hub_to_pub=self.command_mode_dict[command_name]['f_h_P']
    print(format_hub_to_pub,data)
    payl=decode(data)
    print(payl)

  def call_back(self,mode,data):
    command=mode+command[mode]
    #############
    # not finised
    cb=if self.command_mode_dict[command]


"""
callback in LPF2:

in heartbeat call call_back:
   PUP_remote_call_back(mode,data)
"""
