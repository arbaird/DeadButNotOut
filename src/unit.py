from data import *
from event import UnitDied

def darkImage(image):
    image=image.copy()
    for x in range(0,32):
        for y in range(0,32):
            a,b,c,alpha=image.get_at((x,y))
            na=makeZero(a-70)
            nb=makeZero(b-70)
            nc=makeZero(c-70)
            image.set_at((x,y),(na,nb,nc,alpha))
    return image

def makeZero(num):
    if num<0:
        return 0
    else:
        return num

class Unit:
    
    game=None
    
    def __init__(self,description,owner,custom_name=False):
        self.desc=description
        self.name=description[NAME]
        if custom_name:
            self.name=custom_name
        self.ground_movement=description[GM]
        self.ground_movement_ac=self.ground_movement
        self.flying=description[FLY]
        self.hp=description[HP]
        self.hp_ac=self.hp
        self.weapons=description[WEAPONS]
        self.flags=description[NUNITFLAGS]
        
        self.sImageColor=self.game.Ressources['foe_tiles'].get(description[TILE])
        self.sImage=self.sImageColor
        self.sImageDark=darkImage(self.sImage)

        self.x=0
        self.y=0
        self.game._GameEngine__addUnit(self)
        self.finished=False
        self.owner=owner
        self.real_owner=owner
        self.selectedWeapon=0
        self.poisoned=False
        self.alive=True
        self.master=False
        self.exhausted=False
        self.event=UnitDied(self)
        self.xp=0
        self.level=1
        self.disappeared=False
        self.escaped=False
    
    def reuse(self,owner):    
        newone=Unit(self.desc,owner,self.name)
        newone.flags=self.flags
        newone.weapons=self.weapons
        newone.selectedWeapon=self.selectedWeapon
        newone.hp_ac=self.hp_ac
        newone.xp=self.xp
        newone.level=self.level
        newone.hp=self.hp
        return newone
    
    def re_init(self):
        self.sImageColor=self.game.Ressources['foe_tiles'].get(self.desc[TILE])
        self.sImageDark=darkImage(self.sImageColor)
        if self.finished:
            self.sImage=self.sImageDark
        else:   
            self.sImage=self.sImageColor

    def getXP(self,amount): 
        if amount > 100:
            amount=100   
        self.xp+=amount
        if self.xp>=100:
            self.xp-=100
            self.levelUp()
        return self
    def levelUp(self):
        self.level+=1
        self.hp=round(self.hp*1.1)
        self.hp_ac=self.hp
        debug("%s level up!!!!!"%(self.name))
    def exhaust(self):
        self.exhausted=True
        
    def enslave(self,unit):    
        self.owner=unit.getOwner()
        self.master=unit
        self.finish()
        
    def freeFromEnslave(self):
        self.owner=self.real_owner
    
    def resetImage(self):
        if not self.exhausted:
            self.sImage=self.sImageColor
    
    def freeAttackWeapon(self):
        # select freeattack weapon
        x=0
        i=self.selectedWeapon
        for weapon in self.weapons:
            if weapon['Flags'] & F_FREEATTACK:
                i=x
                break
            x+=1
        self.selectedWeapon=i
    
    def check(self):
        if self.poisoned:
            self.game.centerMap(self)
            debug("Poison hurts")
            self.getHit(5)
            self.game.wait(80)
            self.poisoned-=1
            if self.poisoned==0:
                self.poisoned=False
                debug("Poison gets away")
        
        if self.master:
            if not self.master.isAlive():
                self.freeFromEnslave()
    def nextWeapon(self):
        if self.weapons.__len__()>0:
            if self.selectedWeapon!=self.weapons.__len__()-1:
                self.selectedWeapon+=1
            else:
                self.selectedWeapon=0
    
    def getOwner(self):
        return self.owner
    
    def getRealOwner(self):
        return self.real_owner
    
    def reset(self):
        if not self.exhausted:
            self.finished=False
            self.ground_movement_ac=self.ground_movement
            self.resetImage()
        else:
            self.exhausted=False
            
        self.check()
        self.freeAttackWeapon()
    def resetMovement(self):    
        self.ground_movement_ac=self.ground_movement
        
    def getMovementLeft(self):
        return self.ground_movement_ac
    
    def getSelectedWeapon(self):
        return self.weapons[self.selectedWeapon]
    
    def hasFinished(self):
        return self.finished
    
    def finish(self):
        self.finished=True
        self.ground_movement_ac=0
        self.sImage=self.sImageDark
    
    def moved(self,cost):    
        self.ground_movement_ac-=cost
        if self.ground_movement_ac<0:
            self.ground_movement_ac=0
    
    def setPos(self,pos):
        self.x=pos[0]
        self.y=pos[1]
        return self
    
    def jumpTo(self,pos):
        self.game.getMap().remove_unit(self)
        self.x=pos[0]
        self.y=pos[1]
        self.game.getMap().add_unit(self)
        return self
    
    def getPos(self):
        return self.x,self.y
    
    def getAbsolutePosition(self,xoff=0,yoff=0):
        x,y=self.game.getMap().mapToAbsPos([self.x,self.y])
        return (x+xoff,y+yoff)
   
    def walkTo(self,tile,infinite=False):
        self.game.moveUnit(self,tile,infinite)
        return self
    
    def heal(self,amount):
        amount=int(amount)
        x,y=self.getAbsolutePosition()
        self.hp_ac+=amount
        Counter(self.game,str(amount),GREEN,x+TILESIZE,y)
        if self.hp_ac>self.hp:
            self.hp_ac=self.hp
        return self
    
    def getHit(self,amount):
        amount=int(amount)
        x,y=self.getAbsolutePosition()
        self.hp_ac-=amount
        if amount==0:
            amount="MISS!"
        Counter(self.game,str(amount),RED,x+TILESIZE,y)
        if self.hp_ac<1:
            self.die()
        return self
    
    def isAlive(self):
        return self.alive
    
    def __offset(self,pos,xoff,yoff):
        x,y=pos
        return x+xoff,y+yoff
    
    def draw(self,indicator=True,healthbar=True,pos=False):
        
        if not pos:
            pos=self.getAbsolutePosition()
        
        if indicator:
            self.game.screen.blit(self.game.Ressources['indicator'].get(self.getOwner().getID()),pos)
        
        self.game.screen.blit(self.sImage,pos)
        
        if healthbar:    
            if self.poisoned:
                self.game.screen.blit(self.game.images['poison'],self.__offset(pos,0,POISON_COUNTER_OFFSET))
            
            if self.getOwner()!=self.getRealOwner():
                self.game.screen.blit(self.game.images['enslaved'],self.__offset(pos,0,ENSLAVED_COUNTER_OFFSET))
            
            x_size=round(30*((self.hp_ac*1.0)/(self.hp*1.0)))
            if x_size<0:
                x_size=0
            hd=pygame.surface.Surface((x_size,2))
            hd.fill(LIGHT_RED)
            hdl=pygame.surface.Surface((30,2))
            hdl.fill(DARK_RED)    
            if self.poisoned:
                hd.fill(GREEN)
            
            self.game.screen.blit(hdl,self.__offset(pos,1,30))
            self.game.screen.blit(hd,self.__offset(pos,1,30))
    
    def disappear(self):
        self.game._GameEngine__removeUnit(self)
        self.game._GameEngine__undoCache=None
        self.alive=False
        self.disappeared=True
        debug( "%s: I disappeared...."%(self.name))
    def escape(self):
        self.game._GameEngine__removeUnit(self)
        self.game._GameEngine__undoCache=None
        self.alive=False
        self.escaped=True
        debug( "%s: I escaped...."%(self.name))
    def die(self):
        self.game._GameEngine__killUnit(self)
        self.game._GameEngine__removeUnit(self)
        self.event.fire()
        debug( "%s: I died...."%(self.name))
        self.alive=False
        
    def talk(self,text):
        self.game.unitTalk(self,text)