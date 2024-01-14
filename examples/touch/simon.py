from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch
from pupremote import PUPRemoteHub
import urandom

hub = PrimeHub()


buttons={'y':(3,[4,4],'C#4/16'),'g':(4,[4,0],'E3/16'),'r':(6,[0,0],'A4/16'),'b':(5,[0,4],'E4/16')}

game=[]
level=0
holdoff=0

def show(col):
    hub.display.pixel(*buttons[col][1],100)
    hub.speaker.play_notes([buttons[col][2]])

def get_key_col(btns):
    for c in buttons:
         if btns[buttons[c][0]]==1:
            return c
    return None

def next():
    global level
    global game
    level+=1
    col='ygrb'[urandom.randint(0,3)]
    game.append(col)
    return col


p=PUPRemoteHub(Port.A)
p.add_command('touch','10B')    

hub.speaker.volume(20)
gameover=False
while True:
    if gameover:
        gameover=False
        game=[]
        level=0
    
    for l in range(10):
        col_new=next()
        for g in game:
            show(g)
            wait(200)
            hub.display.off()
            wait(100)
        #wait(1000)
        game_guess=[]
        for i,key in enumerate(range(len(game))):
            col=None
            while not col:    
                btns=p.call('touch')
                col=get_key_col(btns)
                wait(20)
            hub.display.off()
            show(col)
            if col!=game[i]:
                print('game over')
                gameover=True
                break
        wait(1000)
        if gameover:
            break       
            
