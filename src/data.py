from content import *

import sys,os,random,pygame
from pygame.locals import *

class TextBox:
    def __init__(self,game,image=False,caption="Caption",text=["TEXT"]):
        oBox=pygame.Surface((304,44+text.__len__()*20))
        iBox=pygame.Surface((300,39+text.__len__()*20))
        self.shadow=pygame.Surface((304,44+text.__len__()*20),pygame.SRCALPHA,32).convert()
        
        stext=[]
        for line in text:
            stext.append(createText(line, sFontBB, BLACK))
            
        sctext=createText(caption, sBFontBB, BLACK)
        oBox.fill(TOOL_TIP_COLOR2)
        iBox.fill(TOOL_TIP_COLOR)
        
        if image:
            iBox.blit(image,(5,5))
        iBox.blit(sctext,(50,5))
        
        x=0
        for line in stext:
            iBox.blit(line,(53,28+x))
            x+=22
            
        oBox.blit(iBox,(2,2))
        self.image=oBox.convert()
        self.image.set_alpha(0)
        
        self.shadow.set_alpha(0)
        self.game=game
        self.iamnew=True
        self.die=False
        self.alpha=0
        self.died=False
    def dieNow(self):
        self.die=True
        self.iamnew=False
    def draw(self):
        i1=self.image
        i2=self.shadow
        ax=15
        maxalpha=255

        if self.iamnew:
            i1.set_alpha(self.alpha)
            if self.alpha<=110:
                i2.set_alpha(self.alpha)
            
            self.alpha+=ax
            if self.alpha==maxalpha:
                self.iamnew=False
                
        if self.die:
            i1.set_alpha(self.alpha)
            if self.alpha-110>0:
                i2.set_alpha(self.alpha-110)
            
            
            if self.alpha>0:
                self.alpha-=ax

            if self.alpha<=15:
                self.died=True
                self.game.textbox=False
                
        self.game.screen.blit(self.shadow,(106,256))
        self.game.screen.blit(self.image,(100,250))

class Counter:
    def __init__(self,game,text,color,x,y):      
        
        self.__image=pygame.Surface((40,30), SRCALPHA, 32).convert()
        self.__image.fill(WHITE)
        self.__image.set_colorkey(WHITE)
        
        __text=createText(text, sBFontB, color,False)
        __text_shadow=createText(text, sBFontB, BLACK)
        
        self.__image.blit(__text_shadow,(0,0))
        self.__image.blit(__text,(1,1))
        
        self.__x=x
        self.__y=y
        self.__ttl=8
        self.__delay=0
        self.__image.set_alpha(255)
        self.__game=game
        game._GameEngine__addCounter(self)
        
    def update(self):
        
        self.__y-=1
            
        self.__delay+=1
        if self.__delay==6:
            self.__delay=0
            self.__ttl-=1
            self.__image.set_alpha(255-42*(6-self.__ttl))
            if self.__ttl==0:
                self.__game._GameEngine__removeCounter(self)    
                
    def getImage(self):
        return self.__image
    
    def getPos(self):
        return self.__x,self.__y

sFontS=pygame.font.Font(os.path.join('fonts','standard.ttf'),10)
sBFontS=pygame.font.Font(os.path.join('fonts','standardbd.ttf'),10)

sFont=pygame.font.Font(os.path.join('fonts','standard.ttf'),12)
sBFont=pygame.font.Font(os.path.join('fonts','standardbd.ttf'),12)

sFontB=pygame.font.Font(os.path.join('fonts','standard.ttf'),14)
sBFontB=pygame.font.Font(os.path.join('fonts','standardbd.ttf'),14)

sFontBB=pygame.font.Font(os.path.join('fonts','standard.ttf'),17)
sBFontBB=pygame.font.Font(os.path.join('fonts','standardbd.ttf'),17)

TextCache={}

def createText(text,font,color,aa=True):
    if not (text,font,color) in TextCache:#TextCache.has_key((text,font,color)):
        TextCache[(text,font,color)]=font.render(text,aa,color)
        
    return TextCache[(text,font,color)]

BLACK=(0,0,0)
WHITE=(255,255,255)
LIGHT_RED=(255,60,60)
RED=(255,0,0)
DARK_RED=(122,0,0)
GREEN=(0,255,0)

wflags={F_POISON:sFont.render('- poisonous',True,BLACK),
                     F_DEATHTOUCH:sFont.render('- Deathtouch',True,BLACK),
                     #F_UNHOLY:sFont.render('- Unholy',True,BLACK),
                     #F_HOLY:sFont.render('- Holy',True,BLACK),
                     F_SUPERKRIT:sFont.render('- extra critical',True,BLACK),
                     F_FREEATTACK:sFont.render('- free attack',True,BLACK),
                     F_LIVEDRAINING:sFont.render('- drains live',True,BLACK),
                     F_ENSLAVE:sFont.render('- enslaving',True,BLACK),
                     F_EXHAUSTING:sFont.render('- exhausting',True,BLACK),
                     #F_SPLASH:sFont.render('- splash damage',True,BLACK), # not implemented
                     F_SACRIFICE:sFont.render('- sacrifice',True,BLACK),
                     F_FIRE:sFont.render('- fire',True,BLACK),
                     F_HEAL:sFont.render('- heals',True,BLACK)}

wtypes={PIERCING:'(Piercing)',
                     BLUDGEONING:'(Bludgeoning)',
                     SLASHING:'(Slashing)',
                     TOUCH:'(Touch)'}
        
uflags={U_MINOR_BLUGDE_RESISTANCE:sFont.render('Bludgeon -20%',True,BLACK),
                     U_MINOR_PIERCE_RESISTANCE:sFont.render('Pierce -20%',True,BLACK),
                     U_MINOR_SLASH_RESISTANCE:sFont.render('Slash -20%',True,BLACK),
                     U_BLUGDE_RESISTANCE:sFont.render('Bludgeon -40%',True,BLACK),
                     U_SLASH_RESISTANCE:sFont.render('Slash -40%',True,BLACK),
                     U_PIERCE_RESISTANCE:sFont.render('Pierce -40%',True,BLACK),
                     U_SPECTRAL:sFont.render('Spectral Creature',True,BLACK),
                     #U_UNHOLY:sFont.render('Unholy Creature',True,BLACK),
                     U_CRITIMMUN:sFont.render('Immun to criticals',True,BLACK),
                     U_POISON_RESISTANCE:sFont.render('Poison Resist',True,BLACK),
                     U_UNDEAD:sFont.render('Undead',True,BLACK)}

# change me
TILESIZE=32
FPS=150

TIME_TILL_TOOLTIP=800
TOOL_TIP_COLOR=(230,190,120)
TOOL_TIP_COLOR2=(190,150,80)

EFFECT_PAUSE=15

TOOL_TIP_OFFSET=20
TOOL_TIP_SHADOW_OFFSET=5

DEBUG=False
CHEAT=False
def debug(*text):
    if DEBUG:
        for line in text:
            print (line)

# change me if you know what you are doing
DISPLAY_X=19
DISPLAY_Y=18

# do not change me
E_UNIT_TILE=1
E_UNIT_DIED=2
E_PLAYER_NO_UNITS=3
E_OBJ_ACHIEVED=4
E_OBJ_FAILED=5
E_NEW_ROUND=6

OBJ_UNITMAYNOTDIE=1001
OBJ_KILLALLUNDEAD=1002
OBJ_KILLALLENEMIES=1003
OBJ_UNITMUSTESCAPE=1004
OBJ_CUSTOM=1000

FAILED=2
RUNNING=0
ACHIEVED=1

NO_WAY_TO_TARGET=88
UNWALKABLE=99

POISON_COUNTER_OFFSET=8
ENSLAVED_COUNTER_OFFSET=0

PLAYER_SELECT_UNIT=1
PLAYER_SELECT_MOVE_TO=2
PLAYER_SELECT_FIGHT_TO=4
PLAYER_SELECTED_ENEMY=8
WAIT_FOR_SPACE=16

NEW_CAMPAIGN=1
LOAD_GAME=2
END_GAME=3

RIGHT=0
LEFT=1
DOWN=2
UP=3


if '-debug' in sys.argv:
    DEBUG=True  
    
if '-cheat' in sys.argv:
    CHEAT=True