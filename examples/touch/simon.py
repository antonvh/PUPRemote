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
highscore=0
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
#gameover=True
level=0
while True:
    if gameover:
        hub.speaker.play_notes(["C5/8","B4/8","A#4/8","A4/8","G#4/4"])
        wait(1000)
        tens=level//10
        for t in range(tens):
            hub.display.pixel(0,0,100)
            hub.display.pixel(0,4,100)
            hub.display.pixel(4,0,100)
            hub.display.pixel(4,4,100)
            wait(200)
            hub.display.off()
            wait(200)
        ones=level%10
        for o in range(ones):
            hub.display.pixel(4,0,100)
            wait(200)
            hub.display.off()
            wait(200)
        wait(1000)
        gameover=False
        game=[]
        level=0
    start=0
    while not start:
        hub.display.pixel(4,0,100)
        btns=p.call('touch')
        col=get_key_col(btns)
        start=col=='g'
        wait(100)
        hub.display.pixel(4,0,0)
        wait(100)
    wait(500)
    hub.speaker.play_notes(["G4/8","C5/8","F5/8"])
    wait(500)
            
    while not gameover:
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
            wait(100)
            if col!=game[i]:
                print('game over')
                gameover=True
                break
        wait(200)
        hub.display.off()
        wait(800)
        if gameover:
            break       
            
