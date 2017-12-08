# global import
from data import *

# DCR imports
import AStar
import math
from ai import AI
from res import Resource
from map import Map
from player import Player
from cursor import Cursor
from scenario import Scenario
from scenarios import camps
from unit import Unit
from event import *
import pickle
import gzip
#  dead creatures rising

#
# this project uses AStar - 1.1 by John Eriksson (wmjoers)
#
# http://www.pygame.org/project/195/
#
#
#Part or all of the graphic tiles used in this program is the public 
#domain roguelike tileset "RLTiles".
#Some of the tiles have been modified
#
#You can find the original tileset at:
#<http://rltiles.sf.net>
#
#Part or all of the graphic tiles used in this program are taken from
#<http://rivendell.fortunecity.com/goddess/268/>
#

print ("pygame version:")
print ( pygame.version.vernum)

if pygame.version.vernum[1]<8:
    _scale= pygame.transform.scale
    print ("It's recommend to use pygame 1.8 or higher")
else:
    _scale= pygame.transform.smoothscale
    

    
class GameEngine(object):
    
    def __init__(self):
        
        # prepare other class
        Unit.game=self
        Scenario.game=self
        Map.game=self
        AI.game=self
        Player.game=self
        Cursor.game=self
        
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (200,200)

        # create screen
        size = (DISPLAY_X*TILESIZE+192, DISPLAY_Y*TILESIZE) # 800x576
        #size = (800,480) pygame.DOUBLEBUF,pygame.NOFRAME
        self.screen = pygame.display.set_mode(size)
        
        # set window icon
        pygame.display.set_icon(pygame.image.load((os.path.join('tiles', 'icon.png'))))
        
        # set window title
        pygame.display.set_caption("Dead but not Out")

        # create a clock for timing
        self.clock = pygame.time.Clock()
        
        # create 2 surfaces to draw map/GUI
        self.main_screen=pygame.Surface((19*TILESIZE,18*TILESIZE)) # 19x18 tiles
        self.gui_screen =pygame.Surface((192,576))
        
        # load images/sounds
        # tilesheets
        debug( "loading tilesheets")
        self.Ressources={'foe_tiles':Resource(os.path.join('tiles', 'foes.png'), TILESIZE),
                         'cursor':Resource(os.path.join('tiles', 'cursor.png'), TILESIZE),
                         'indicator':Resource(os.path.join('tiles', 'indicator.png'), TILESIZE),
                         #'move':Resource(os.path.join('tiles', 'move.png'), TILESIZE),
                         'arrows':Resource(os.path.join('tiles', 'arrows.png'), TILESIZE),
                         'cursor_fx':Resource(os.path.join('tiles', 'cursor_fx.png'), TILESIZE)
                         }
        # single images
        debug( "loading images")
        self.images={'title_image':pygame.image.load(os.path.join('tiles', 'title.png')),
                     'gui_image':pygame.image.load(os.path.join('tiles', 'gui_back.png')),
                     'poison':pygame.image.load(os.path.join('tiles', 'poison.png')),
                     'enslaved':pygame.image.load(os.path.join('tiles', 'enslaved.png'))}
        
        # textbox to display text-messages
        self.textbox=False
        
        # the gamestate
        self.__state=0
        self.__old_state=0
        self.__round=0
        
        # create cursor
        self.cursor=Cursor()
        
        # draw empty GUI on screen 
        self.__gui_init()

        # is it necessary to redraw the gui?
        self.__gui_change=True
        
        # place for all damage indicators
        self.__counters=[]
        
        # a delay until the player can make new inputs
        self.__inputDelay=0
        
        # should be skip fighting?
        self.__skipFighting=False
        
        # should be skip a player?
        self.__skipPlayers=[]
        
        # a place to store the last movement for doing a 'undo'
        self.__undoCache=None
        
        # tiles that are highlighted
        self.__highlightedTiles=[]
        
        self.quit=False
        
        self.buffer=True
    def getState(self):
        return self.__state
    def disableFighting(self):
        self.__skipFighting=True
    def enableFighting(self):
        self.__skipFighting=False
    def skipPlayer(self,player):    
        self.__skipPlayers.append(player)
    def dontSkipPlayer(self,player):
        self.__skipPlayers.remove(player)
    def getActivePlayer(self):    
        return self.scenario.getActivePlayer()
    def getHumanPlayer(self):
        return self.scenario.getHumanPlayer()
    def getUnits(self):
        return self.scenario.getUnits()
    def fight(self,unit,eunit,counter=False,noharm=False):
        w=unit.getSelectedWeapon()
        dam=w[DAMAGE]
        d=0
        if not noharm:
            d=random.randrange(dam*8,dam*(10+unit.level))/10
        range=w['Range']
        dis=math.sqrt(math.pow((eunit.x-unit.x),2)+math.pow((eunit.y-unit.y),2))

        # check if target is in range
        if range<dis:
            return 1
        if range==2 and dis==1:
            return 1
        
        self.__waitForDelay()
        
        debug("%s fights %s"%(unit.name,eunit.name))
        
        if w[WEAPONFLAGS] & F_HEAL and not eunit.flags & U_UNDEAD:
            eunit.heal(d)
            debug("%s heals %s for %i damage with %s"%(unit.name,eunit.name,d,w[NAME])    )
            return 0
        
        # geting to to-hit-chance:
        toHit = self.__getToHit(eunit)
        
        if counter:
            toHit-=10
            d=round(d*0.9)
            
        z = random.randrange(0,100)
        if z > toHit:
            debug("miss!")
            d=0

        self.__drawUnitCombat(unit,eunit)
        
        if d>0:
            # test basic resistance
            if w[WEAPONTYPE] & BLUDGEONING and eunit.flags & U_BLUGDE_RESISTANCE:
                d=round(d*0.6)
            if w[WEAPONTYPE] & BLUDGEONING and eunit.flags & U_MINOR_BLUGDE_RESISTANCE:
                d=round(d*0.8)
                
            if w[WEAPONTYPE] & PIERCING and eunit.flags & U_PIERCE_RESISTANCE:
                d=round(d*0.6)
            if w[WEAPONTYPE] & PIERCING and eunit.flags & U_MINOR_PIERCE_RESISTANCE:
                d=round(d*0.8)
            
            if w[WEAPONTYPE] & SLASHING and eunit.flags & U_SLASH_RESISTANCE:
                d=round(d*0.6)
            if w[WEAPONTYPE] & SLASHING and eunit.flags & U_MINOR_SLASH_RESISTANCE:
                d=round(d*0.8)
                
            # test for deathtouch
            if w[WEAPONFLAGS] & F_DEATHTOUCH:
                z = random.randrange(0,100)
                if z > 50:
                    d=eunit.hp_ac-1
                    debug("%s deathtouches %s!"%(unit.name,eunit.name))
                    
            # test for crit
            z = random.randrange(0,100)
            if z > 90 and z <=94:
                debug("critical")
                d=d*2
                if z > 95 and w[WEAPONFLAGS] & F_SUPERKRIT:
                    debug("super critical!")
                    d=d*3
            
            # test for poison     
            if w[WEAPONFLAGS] & F_POISON and not eunit.flags & U_POISON_RESISTANCE:
                z = random.randrange(0,100)
                if z > 60:
                    eunit.poisoned=round(d/2)
                    debug("%s empoisoned %s!"%(unit.name,eunit.name))
            
            # test for livedraining
            if w[WEAPONFLAGS] & F_LIVEDRAINING and not eunit.flags & U_UNDEAD:
                z = random.randrange(0,100)
                if z > 40:
                    drain=round(d/2)
                    if z >=90:
                        drain=d
                    if d>0:
                        unit.heal(drain)
                        debug("%s drained %i HP from %s!"%(unit.name,drain,eunit.name))
                 
            # test for enslaving
            if w[WEAPONFLAGS] & F_ENSLAVE:
                z = random.randrange(0,100)
                if z > 70:     
                    eunit.enslave(unit)
        
        # test for exhausting
        if w[WEAPONFLAGS] & F_EXHAUSTING:
            z = random.randrange(0,100)
            if z > 50:     
                unit.getHit(round(d/4))
            unit.exhaust()
        
        # test for F_SACRIFICE
        if w[WEAPONFLAGS] & F_SACRIFICE:
            z = random.randrange(0,100)
            if z > 2:     
                unit.getHit(unit.hp_ac)
            else:
                unit.getHit(unit.hp_ac-1)
                unit.exhaust()    
        
        if d>0:
            debug("%s hits %s for %i damage with %s"%(unit.name,eunit.name,d,w[NAME]))
        else:
            debug("miss.......")
        if not noharm:
            eunit.getHit(round(d))
        
        self.wait(20)
        
        ans=0
        if not counter:
            if w[WEAPONFLAGS] & F_FREEATTACK and eunit.isAlive():
                unit.nextWeapon()
                ans=self.fight(unit,eunit,noharm=noharm)
                unit.freeAttackWeapon()
            else:
                if not noharm:
                    unit.finish()
            
        if not counter and ans==0 and random.randrange(0,100)>60 and eunit.isAlive() and unit.isAlive():
            if eunit.getSelectedWeapon()[WEAPONFLAGS] & F_HEAL and not eunit.flags & U_UNDEAD: 
                return 1
            debug( "------- start counter")
            self.fight(eunit,unit,counter=True,noharm=noharm)
            debug( "-------")
            return 1
        
        if unit.isAlive() and not w[WEAPONFLAGS] & F_FREEATTACK:
            xp=3
            if not eunit.isAlive():
                xp+=20*((10-(unit.level-eunit.level*2))/10.0)
            unit.getXP(xp)
            debug("%s gets %i XP"%(unit.name,xp))
            
        if eunit.isAlive():
            xp=1
            if not unit.isAlive():
                xp+=20*((10-(eunit.level-unit.level*2))/10.0)
            eunit.getXP(xp)
            debug("%s gets %i XP"%(eunit.name,xp))
    def moveUnit(self,unit,targetTile,infiniteMovement=False):
        # find a path
        startTile=unit.getPos()
        map=self.getMap()
        wmap=map.getWalkMap(unit)
        astar = AStar.AStar(AStar.SQ_MapHandler(wmap,map.iMapWidth,map.iMapHeight))
        start = AStar.SQ_Location(startTile[0],startTile[1])
        end = AStar.SQ_Location(targetTile[0],targetTile[1])

        p = astar.findPath(start,end)

        path=[]
        
        if not p:
            return NO_WAY_TO_TARGET
        
        for n in p.nodes:
            path.append((n.location.x,n.location.y))
        
        self.scenario.getMap().remove_unit(unit)
        
        cost=0
        
        self.__undoCache=(unit,unit.getPos(),path)

        while path.__len__()!=0:
            pygame.event.clear() #do not allow queue to build while drawing unit movement, this causes spinning beach ball to appear
            if not unit.isAlive():
                return 0
            
            if not infiniteMovement:
                if not unit.flying:
                    cost=self.scenario.getMap().getMoveCostFast(path[0],unit)
                else:
                    cost=1
                    
            if cost<=unit.ground_movement_ac:
                # if theres a unit, test if we can leave that tile
                toFar = False
                x=0
                tc=cost

                while self.scenario.getMap().getUnit(path[x]):
                    x+=1
                    tc+=self.scenario.getMap().getMoveCostFast(path[x],unit)
                    if not tc<=unit.ground_movement_ac:
                        toFar=True
                        break
                if not toFar:
                    self.__drawUnitMovement(unit,path[0])
                    UnitReachedTile(unit,path[0]).fire()
                    path=path[1:]
                    unit.moved(cost)
                else:
                    unit.moved(1000)
                    break
            else:
                unit.moved(1000)
            
            if unit.getMovementLeft()<1:
                break

        if not infiniteMovement:
            unit.moved(1000)
        
        if unit.isAlive():    
            self.scenario.getMap().add_unit(unit)
    def wait(self,amount):        
        self.__inputDelay+=amount

        self.__waitForDelay()
    def getMap(self):
        return self.scenario.getMap()
    def unitTalk(self,unit,text):
        i=_scale(unit.sImageColor,(43,43))
        self.__newTextbox(TextBox(self,i,unit.name+":",text))
    def showObjectives(self):
        text=[]
        for obj in self.scenario.getObjectives():
            text.append("- "+obj.descripe())
        if len(text)==0:
            text.append("- no objectives")
        self.messageBox("Objectives:",text)
    def messageBox(self,title,text):
        i=_scale(self.Ressources['foe_tiles'].get(14),(43,43))
        self.__newTextbox(TextBox(self,i,title,text))
    def loadScenario(self,s):
        self.__switchState(PLAYER_SELECT_UNIT)
        self.__round=1
        self.__counters=[]
        self.__highlightedTiles=[]
        self.scenario=s
        self.scenario.load()
        self.__updateScreen(nocursor=True)
        self.__showNextPlayer(self.scenario.getActivePlayer())        
    def quake(self,duration):
        pos=self.getMap().position
        x=0
        while duration:
            if duration > 0:
                duration -= 1
            self.getMap().move(x)
            self.__updateScreen(nocursor=True)
            x+=1
            if x==4:
                x=0
            pygame.event.clear()  # do not allow queue to build while drawing unit movement, this causes spinning beach ball to appear
        self.getMap().position=pos
    def highlight(self,tiles):    
        for tile in tiles:
            self.__highlightedTiles.append(tile)
    def getHighlight(self):
        return self.__highlightedTiles
    def stopHighlight(self):        
        self.__highlightedTiles=[]
    def getUnitAt(self,pos):
        return self.getMap().getUnit(pos)
    def moveMap(self,dir,count,noani=False):
        oldpos=self.getMap().position
        for _ in range(count): self.getMap().move(dir)
        newpos=self.getMap().position
        if not noani:
            self.__drawMapMovement(oldpos,newpos)
    def moveMapTo(self,pos,noani=False):
        oldpos=self.getMap().position
        self.getMap().moveTo(pos)
        newpos=self.getMap().position
        if not noani:
            self.__drawMapMovement(oldpos,newpos)
    def centerMap(self,pos,noani=False):
        if isinstance(pos,Unit):
            pos=pos.getPos()
        oldpos=self.getMap().position
        self.getMap().center(pos)
        newpos=self.getMap().position
        if not noani:
            self.__drawMapMovement(oldpos,newpos)
        
    def __getToHit(self, eunit):
        toHit = 80
        #if range > 1:
           # toHit = 70
        
        toHit -= self.getMap().getCover(eunit.getPos())
        if eunit.flags & U_SPECTRAL:
            toHit /= 2
        
        return toHit
    def __newTextbox(self,textbox):
        self.textbox=textbox
        self.__waitForSpace()
    def __addUnit(self,unit):
        self.getMap().add_unit(unit)
        self.scenario.addUnit(unit)
    def __removeUnit(self,unit): 
        self.getMap().remove_unit(unit)
        self.scenario.removeUnit(unit)
    def __getTileUnderMouse(self):
        """returns the tile (x,y) which is under the mouse"""
        x, y = self.scenario.getMap().absToMapPos(pygame.mouse.get_pos())
        return  int(x),int(y)

    def __waitForDelay(self):
        while self.__inputDelay:
            if self.__inputDelay > 0:
                self.__inputDelay -= 1
            self.__updateScreen(nocursor=True)
    def __showNextPlayer(self,player):
        self.__waitForDelay()
        self.messageBox("Next Player",["It's " +player.name+"'s turn"])
    def __waitForSpace(self):
        self.__switchState(WAIT_FOR_SPACE)

        while self.__state==WAIT_FOR_SPACE:
            self.__waitForDelay()
            self.__updateScreen()
            self.__updateInput()
        
        self.textbox.dieNow()
    def __checkCursor(self):
        pos=self.__getTileUnderMouse()
        if self.scenario.getMap().isOnMap(pos):
            unit=self.scenario.getMap().getUnit(pos)
            if unit:
                if unit!=self.cursor.unit:
                    self.cursor.setPosition(unit)
                    self.__gui_change=True
            else:
                self.cursor.reset()
        else:
            self.cursor.reset()
    def __updateLogic(self):
        
        if self.getActivePlayer()==self.getHumanPlayer():
        # check if unit is under cursor
            if self.__state==PLAYER_SELECT_UNIT:
                self.__checkCursor()
            else:
                self.cursor.findTilesToHighlight()
            
            if self.cursor.isActive():
                self.cursor.tick()
        
        else:
            self.getActivePlayer().act()
        
        if self.__inputDelay>0:
            self.__inputDelay-=1    
            
        # check if all units moved
        allmoved=True
        for unit in self.getActivePlayer().getUnits():
            if not unit.hasFinished():
                allmoved=False
        if allmoved:
            debug("active player finished movement")
            debug(self.getActivePlayer().name)
            self.__nextPlayer()
    def __newRound(self):
        for unit in self.getUnits():
            unit.reset()
        self.__round+=1
        NewRound(self.scenario).fire()
    def __nextPlayer(self,noshow=False):        
        self.__inputDelay+=15
        self.__undoCache=None
        for x in range(self.scenario.getNumberOfPlayers()):
            if self.getActivePlayer()==self.scenario._Scenario__players[x]:
                if x==self.scenario.getNumberOfPlayers()-1:
                    # current player is the last one in the list
                    x=-1
                    # start a new __round
                    self.scenario.setActivePlayer(self.scenario._Scenario__players[0])
                    self.__newRound()
                else:
                    # or simple next player of players with no units
                    self.scenario.setActivePlayer(self.scenario._Scenario__players[x+1])
                    if self.getActivePlayer() in self.__skipPlayers:
                        debug("skipping player %s"%(str(x+1)))
                        self.__nextPlayer(True)
                        break
                    a=False
                    for unit in self.getUnits():
                        if unit.getOwner() == self.getActivePlayer():
                            a=True
                    if not a:
                        debug("skipping player %s cause he got nothing"%(str(x+1)))
                        self.__nextPlayer(True)      
                break;
        
        if not noshow:
            units=self.getActivePlayer().getUnits()
            try:
                self.centerMap(units[0])
            except IndexError:
                pass
            self.__showNextPlayer(self.getActivePlayer())
    def __updateScreen(self,donotdraw=[],draw=[],nocursor=False):
        """Draw the standart-screen (Map+Units).
        noflip: pygame.display.flip() will not be called.
        nocursor: the cursor will not be shown."""
        x,y=self.getMap().position
        
        if self.textbox:
            nocursor=True
        
        self.screen.blit(self.getMap().sMapImage,self.getMap().position)        
        
        # highlighted tiles
        for tile in self.__highlightedTiles:
            self.screen.blit(self.Ressources['cursor'].get(4),(self.getMap().mapToAbsPos(tile)))
            # effect
            if self.cursor.c_fx_c>=0:
                self.screen.blit(self.cursor.c_fx.get(self.cursor.c_fx_c),self.getMap().mapToAbsPos(tile))    
                    
        for unit in self.getUnits():
            if unit not in donotdraw:
                unit.draw()

        for extra in draw:
            #unit.draw(indicator,healthbar,position)
            extra[0].draw(True,True,extra[1])
        
        #self.screen.blit(self.scenario.getMap().sMapNightImage,self.scenario.getMap().position)        
        self.__drawGUI(self.__gui_change)
        
        for counter in self.__counters:
            counter.update()
            self.screen.blit(counter.getImage(),counter.getPos())
        
        if not nocursor:
            self.cursor.show()
        
        if self.textbox:
            self.textbox.draw()

        self.clock.tick(FPS)
        
        pygame.display.flip() 
    def __gui_init(self):
        self.gui_screen.fill(TOOL_TIP_COLOR2)
        self.gui_screen.blit(self.images['gui_image'],(0,0))    
        self.screen.blit(self.gui_screen,(608,0))
    def __drawGUI(self,new):
        
        f=sFont
        fb=sBFont
        tX=18
        tY=15
        
        if self.cursor.unit and new:
            self.gui_screen.fill(TOOL_TIP_COLOR2)
            self.gui_screen.blit(self.images['gui_image'],(0,0))    
            unit=self.cursor.unit
            
            # creature name
            self.gui_screen.blit(createText(unit.name,fb,BLACK),(tX,tY))
            self.gui_screen.blit(createText(unit.getOwner().name,f,BLACK),(tX,tY+15))
            
            # creature image
            self.gui_screen.blit(_scale(unit.sImageColor,(43,43)),(tX,tY+TILESIZE+15))
            if unit.poisoned:
                self.gui_screen.blit(self.images['poison'],(tX,tY+TILESIZE+15+POISON_COUNTER_OFFSET))
            if unit.getOwner()!=unit.getRealOwner():
                self.gui_screen.blit(self.images['enslaved'],(tX,tY+TILESIZE+15+ENSLAVED_COUNTER_OFFSET))
            
            # creature hp
            strHP='HP    : %i/%i'%(unit.hp_ac,unit.hp)
            self.gui_screen.blit(createText(strHP,f,BLACK),(tX+TILESIZE+15,tY+TILESIZE+15))
            
            # creature level
            strLe='LVL   : %i'%(unit.level)
            strXP='EXP  : %i'%(unit.xp)
            self.gui_screen.blit(createText(strXP,f,BLACK),(tX+TILESIZE+15,tY+TILESIZE+30))
            self.gui_screen.blit(createText(strLe,f,BLACK),(tX+TILESIZE+15,tY+TILESIZE+45))

            
            
            # creature movement
            strMOV='%i/%i Movement Points'%(unit.ground_movement_ac,unit.ground_movement)
            self.gui_screen.blit(createText(strMOV,f,BLACK),(tX,tY+TILESIZE+61))
            
            
            # gathering information
            line_weaps=0
            weap=[]
            for weapon in unit.weapons:
                flags=[]
                for flag in FLAGS:
                    if weapon['Flags'] & flag:
                        flags.append(wflags[flag])
                
                damage="%i - %i Dam. "%((weapon['Damage']*8)/10,(weapon['Damage']*(10+unit.level))/10)
                
                damOrHeal=""
                if weapon['Flags'] & F_HEAL:
                    damOrHeal="heals "
                if unit.selectedWeapon==line_weaps/2:
                        weap.append(
                                    [fb.render("- " + weapon['Name']+" *",True,BLACK),
                                     f.render("Range: "+str(weapon['Range']),True,BLACK),
                                     f.render(damOrHeal+damage+ wtypes[weapon['Type']],True,BLACK),
                                     flags])
                else:
                        weap.append([fb.render("- " + weapon['Name'],True,BLACK),
                        f.render("Range: "+str(weapon['Range']),True,BLACK),
                        f.render(damOrHeal+damage + wtypes[weapon['Type']],True,BLACK),
                        flags])
                line_weaps+=2
            
            alluflags=[]
            for uflag in UFLAGS:
                if unit.flags & uflag:
                    alluflags.append(uflags[uflag])

            x=26+tY+TILESIZE+45+11
            
            if unit.flying:
                self.gui_screen.blit(createText("Flying",f,BLACK),(tX,2+x));x+=14
            
        
            for flag in alluflags:
                self.gui_screen.blit(flag,(tX,2+x));x+=14
        
            x+=14

            for weapon in weap:
                self.gui_screen.blit(weapon[0],(tX,2+x));x+=14
                self.gui_screen.blit(weapon[1],(tX+6,2+x));x+=14
                self.gui_screen.blit(weapon[2],(tX+6,2+x));x+=14
                for line in weapon[3]:
                    self.gui_screen.blit(line,(tX+6,2+x));x+=14

        self.screen.blit(self.gui_screen,(608,0))
        self.__gui_change=False   
    def __inputMoveUnit(self):
        pos=self.__getTileUnderMouse()
        unit=self.cursor.getUnit()
        if self.cursor.isReachable(pos):
            if not self.scenario.getMap().getUnit(pos):
                self.moveUnit(unit,pos)
                if unit.isAlive():
                    self.__switchState(PLAYER_SELECT_FIGHT_TO)
                else:
                    self.__switchState(PLAYER_SELECT_UNIT)
            elif pos==self.cursor.getUnit().getPos():
                unit.moved(999)
                if unit.isAlive():
                    self.__switchState(PLAYER_SELECT_FIGHT_TO)
                else:
                    self.__switchState(PLAYER_SELECT_UNIT)
            else:
                self.__switchState(PLAYER_SELECT_UNIT)
    def __inputSelectUnit(self):
        unit=self.cursor.getUnit()
        if unit:
            if not unit.hasFinished() and unit.getOwner()==self.getActivePlayer():
                self.__state=PLAYER_SELECT_MOVE_TO
            else:
                self.__state=PLAYER_SELECTED_ENEMY
    def __inputFightUnit(self):
        unit = self.cursor.getUnit()
        pos = self.scenario.getMap().absToMapPos(pygame.mouse.get_pos())
        toFightUnit = self.scenario.getMap().getUnit(pos)
        if self.cursor.isFightable(pos) and toFightUnit:
            a=toFightUnit.getOwner();b=unit.getOwner()
            heal=unit.weapons[0]['Flags'] & F_HEAL
            undead=toFightUnit.flags&U_UNDEAD
            if (a==b and heal) or (a!=b and not (heal and not undead)):
                self.fight(unit, toFightUnit)
            else:
                self.__inputUndo()
                return 0
        else:
            if pos!=unit.getPos():
                self.__inputUndo()
                return 0
        unit.finish()
        self.__undoCache = None
        self.__state = PLAYER_SELECT_UNIT
        self.cursor.reset()
    def __inputUndo(self):
        if self.__undoCache:
            self.__undoMovement()
        else:
            self.cursor.getUnit().resetMovement()
        self.__switchState(PLAYER_SELECT_UNIT)
    def __inputMoveCursor(self,e):
        x, y = pygame.mouse.get_pos()
        xm = 0
        ym = 0
        if e.key == pygame.K_UP:
            ym = -TILESIZE
        
        if e.key == pygame.K_DOWN:
            ym = TILESIZE
        
        if e.key == pygame.K_LEFT:
            xm = -TILESIZE
        
        if e.key == pygame.K_RIGHT:
            xm = TILESIZE
        pygame.mouse.set_pos(x + xm, y + ym)
        #self.centerMap((x + xm, y + ym))

    def __handleMouseEvent(self, e):
        
        if self.__state == WAIT_FOR_SPACE:
            self.__goToPreviousState()
        
        elif self.__state == PLAYER_SELECT_UNIT:
            if e.button == 1:
                self.__inputSelectUnit()
        
        elif self.__state == PLAYER_SELECT_MOVE_TO:
            if e.button == 1:
                self.__inputMoveUnit()
            if e.button == 3:
                self.__switchState(PLAYER_SELECT_UNIT)
        
        elif self.__state == PLAYER_SELECT_FIGHT_TO:
            if e.button == 1:
                self.__inputFightUnit()
            
            if e.button == 3:
                self.__inputUndo()
                
        elif self.__state == PLAYER_SELECTED_ENEMY:
            if e.button == 1:
                self.__switchState(PLAYER_SELECT_UNIT)
    def __handleKeyEvent(self, e):
        
        if CHEAT:
            u=self.getUnitAt(self.__getTileUnderMouse())
            if u:
                if e.key == pygame.K_1:
                    u.poisoned=10
                if e.key == pygame.K_2:
                    u.getHit(10)
                if e.key == pygame.K_3:
                    u.heal(10)
                if e.key == pygame.K_4:
                    u.getXP(100)
                self.__gui_change=True
                    
        if e.key == pygame.K_o:
            sys.exit()

        if e.key==pygame.K_F5:
            self.__save()
            
        if e.key==pygame.K_F8:
            self.__load()

        if e.key == pygame.K_F11:
            pygame.display.toggle_fullscreen()
        
        if e.key == pygame.K_F2:
            self.showObjectives()
        
        if self.getState() == PLAYER_SELECT_UNIT:
            if e.key == pygame.K_RETURN:
                self.__inputSelectUnit()
            
            elif e.key == pygame.K_s:
                if self.cursor.unit:
                    if self.cursor.unit.getOwner() == self.getHumanPlayer():
                        self.cursor.unit.nextWeapon()
                        self.cursor.resetToolTip()
                        self.__gui_change = True
            elif e.key == pygame.K_q:
                for unit in self.getActivePlayer().getUnits():
                    unit.finish()
                
        elif self.getState() == PLAYER_SELECT_MOVE_TO:
            if e.key == pygame.K_RETURN:
                self.__inputMoveUnit()
            if e.key == pygame.K_BACKSPACE:
                self.__switchState(PLAYER_SELECT_UNIT)
                
        elif self.getState() == PLAYER_SELECT_FIGHT_TO:
            if e.key == pygame.K_RETURN:
                self.__inputFightUnit()
            if e.key == pygame.K_BACKSPACE:
                self.__inputUndo()    
                
        elif self.getState() == PLAYER_SELECTED_ENEMY:
            if e.key == pygame.K_RETURN:
                self.__switchState(PLAYER_SELECT_UNIT)

        elif self.getState() == WAIT_FOR_SPACE:
            self.__goToPreviousState()
        
        if e.key in (pygame.K_UP,pygame.K_DOWN,pygame.K_RIGHT,pygame.K_LEFT):
            self.__inputMoveCursor(e)
         
            
        if e.key == pygame.K_LCTRL:
            pygame.event.clear(pygame.MOUSEMOTION)
            self.buffer=True
    def __handleMouseMotion(self,e):
        m=pygame.key.get_pressed()
        if m[pygame.K_LCTRL]:

            x,y=pygame.mouse.get_rel()

            if self.buffer:
                self.buffer=False
            else:
                self.getMap().new_move((x,y))
            #x,y=pygame.mouse.get_rel()
            #if x>0:
            #    self.scenario.getMap().move(RIGHT)
            #elif x<0:
            #    self.scenario.getMap().move(LEFT)
            #if y>0:
            #    self.scenario.getMap().move(DOWN)
            #elif y<0:
            #    self.scenario.getMap().move(UP)
    def __updateInput(self):
        for e in pygame.event.get():

            if e.type == pygame.QUIT:
                self.__exit()

            if e.type==pygame.KEYDOWN:
                self.__handleKeyEvent(e)
                pygame.event.clear(pygame.KEYDOWN)
                
            if e.type == pygame.MOUSEBUTTONUP:
                self.__handleMouseEvent(e)
                pygame.event.clear(pygame.MOUSEBUTTONUP)
                
            if e.type == pygame.MOUSEMOTION:
                self.__handleMouseMotion(e)
                pygame.event.clear(pygame.MOUSEMOTION)
    def __undoMovement(self):
        if self.__undoCache:
            unit, startPos, path=self.__undoCache
            self.scenario.getMap().remove_unit(unit)
            while path.__len__()!=0:
                self.__drawUnitMovement(unit,path[-1])
                path=path[:-1]
            self.__drawUnitMovement(unit,startPos)
            unit.resetMovement()
            self.scenario.getMap().add_unit(unit)
        self.__undoCache=None
    def __killUnit(self,unit):
        unit.sImage=unit.sImage.copy()
        z=0
        while z<255:
            d=0.0;dc=0
            for x in range(0,32):
                for y in range(0,32):
                    a,b,c,alpha=unit.sImage.get_at((x,y))
                    na=z+a
                    nb=z+b
                    nc=z+c
                    if na>255:
                        na=255
                    if nb>255:
                        nb=255
                    if nc>255:
                        nc=255
                    d+=na+nb+nc
                    dc+=3
                    unit.sImage.set_at((x,y),(na,nb,nc,alpha))
            if d/dc==255:
                break
            self.__updateScreen([unit],[(unit,unit.getAbsolutePosition())],True)
            z+=1
    def __drawMapMovement(self,oldpos,newpos):
        nx,ny=newpos
        while oldpos!=newpos:
            x,y=oldpos
            if x<nx:    
                x+=3
            elif x>nx:
                x-=3
            if x-nx in (-2,-1,1,2):
                x=nx
            if y<ny:
                y+=3
            elif y>ny:
                y-=3
            if y-ny in(-2,-1,1,2):
                y=ny
            oldpos=x,y
            self.getMap().position=oldpos
            self.__updateScreen(nocursor=True)

    def __drawUnitMovement(self,unit,target_pos):
        sx,sy=unit.getAbsolutePosition()
        tx,ty=self.scenario.getMap().mapToAbsPos(target_pos)
        
        while sx<tx:
            sx+=2
            self.__updateScreen([unit],[(unit,(sx,sy))],True)
            
        while sx>tx:
            sx-=2
            self.__updateScreen([unit],[(unit,(sx,sy))],True)
            
        while sy<ty:
            sy+=2
            self.__updateScreen([unit],[(unit,(sx,sy))],True)
            
        while sy>ty:
            sy-=2
            self.__updateScreen([unit],[(unit,(sx,sy))],True)
        
        unit.setPos(target_pos)
    def __drawUnitCombat(self,unit,munit):
        sx,sy=unit.getAbsolutePosition()
        ux,uy=unit.getAbsolutePosition()
        
        tx,ty=munit.getAbsolutePosition()

        if sx<tx:
            tx=sx+8
        elif sx>tx:
            tx=sx-8
        if sy<ty:
            ty=sy+8
        elif sy>ty:
            ty=sy-8
        
        # move right
        while sx<tx:
            sx+=1
            if sy<ty:
                sy+=1
            elif ty<sy:
                sy-=1
            #self.clock.tick(55)
            self.__updateScreen([unit],[(unit,(sx,sy))],True)
            
        while sx>tx:
            sx-=1
            if sy<ty:
                sy+=1
            elif ty<sy:
                sy-=1
            #self.clock.tick(55)
            self.__updateScreen([unit],[(unit,(sx,sy))],True)
            
        while sy<ty:
            #self.clock.tick(55)
            sy+=1
            self.__updateScreen([unit],[(unit,(sx,sy))],True)
            
        while sy>ty:
            #self.clock.tick(55)
            sy-=1
            self.__updateScreen([unit],[(unit,(sx,sy))],True)
        
        tx=ux
        ty=uy
        
        while sx<tx:
            sx+=1
            if sy<ty:
                sy+=1
            elif ty<sy:
                sy-=1
            #self.clock.tick(55)
            self.__updateScreen([unit],[(unit,(sx,sy))],True)    
            
        while sx>tx:
            sx-=1
            if sy<ty:
                sy+=1
            elif ty<sy:
                sy-=1
            #self.clock.tick(55)
            self.__updateScreen([unit],[(unit,(sx,sy))],True)    
            
        while sy<ty:
            #self.clock.tick(55)
            sy+=1
            self.__updateScreen([unit],[(unit,(sx,sy))],True)    

            
        while sy>ty:
            #self.clock.tick(55)
            sy-=1
            self.__updateScreen([unit],[(unit,(sx,sy))],True)    
    def __showTitleScreen(self):   
        
        timage=self.images['title_image']
        self.screen.blit(timage,(0,0))
        
        f=pygame.font.Font(os.path.join('fonts','menu2.ttf'),40)
        
        tNewCamp=f.render('new campaign',True,WHITE)
        tLoadGame=f.render('load game',True,WHITE)
        tQuit=f.render('quit game',True,WHITE)
        
        tNewCampS=f.render('new campaign',True,LIGHT_RED)
        tLoadGameS=f.render('load game',True,LIGHT_RED)
        tQuitS=f.render('quit game',True,LIGHT_RED)
        
        r1=tNewCamp.get_rect()
        r2=tLoadGame.get_rect()
        r3=tQuit.get_rect()

        selected=False
        n_selected=False
        
        x=40
        
        while not selected:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if e.type==pygame.KEYDOWN:
                    if e.key==K_f:
                        pygame.display.toggle_fullscreen()
            
                if e.type==pygame.MOUSEBUTTONUP:
                    if n_selected:
                        selected=n_selected
                    
            n_selected=False
            
            mx,my=pygame.mouse.get_pos()
            
            if r1.collidepoint([mx-500,my-400]):
                n_selected=NEW_CAMPAIGN
            elif r2.collidepoint([mx-500,my-400-x]):
                n_selected=LOAD_GAME
            elif r3.collidepoint([mx-500,my-400-2*x]):
                n_selected=END_GAME
        
            self.screen.fill(BLACK)
            self.screen.blit(timage,(0,0))
            
            if not n_selected==1:
                self.screen.blit(tNewCamp,(500,400)) 
            else:
                self.screen.blit(tNewCampS,(500,400)) 
            if not n_selected==2:
                self.screen.blit(tLoadGame,(500,400+x)) 
            else:
                self.screen.blit(tLoadGameS,(500,400+x)) 
            if not n_selected==3:
                self.screen.blit(tQuit,(500,400+2*x)) 
            else:
                self.screen.blit(tQuitS,(500,400+2*x)) 
            
            pygame.display.flip()    
        
        pygame.event.clear()
        return selected
    def __campaignSelection(self):
        timage=self.images['title_image']
        self.screen.blit(timage,(0,0))
        
        f=pygame.font.Font(os.path.join('fonts','menu2.ttf'),40)
        f2=sFont
        f3=sBFont
        
        tDescription=f3.render('Description:',True,WHITE)
        tLength=f3.render('Lenght:',True,WHITE)
        campinfo=[]
        
        for camp in camps:
            try:
                title = f.render(camp['Name'],True,WHITE)
                titleS = f.render(camp['Name'],True,LIGHT_RED)
                rect = title.get_rect()
                desc  = []
                for line in camp['Desc']:
                    desc.append(f2.render(line,True,WHITE))
                length= f2.render(camp['Length'],True,WHITE)
                campinfo.append([title,titleS,rect,desc,length])
            except:
                print ("There's a problem with a campaign")
                print ("Invalid Desc Error")
                sys.exit()
                
        selected=False
        n_selected=False
        
        while not selected:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if e.type==pygame.KEYDOWN:
                    if e.key==K_f:
                        pygame.display.toggle_fullscreen()
            
                if e.type==pygame.MOUSEBUTTONUP:
                    if n_selected:
                        selected=n_selected
            
            n_selected=False
            
            mx,my=pygame.mouse.get_pos()
            
            self.screen.fill(BLACK)
            self.screen.blit(timage,(0,0))
            
            x=0
            s=1
            for camp in campinfo:
                if not camp[2].collidepoint(mx-50,my-200-x):
                    self.screen.blit(camp[0],(50,200+x))
                else:
                    self.screen.blit(camp[1],(50,200+x))
                    y=30
                    
                    self.screen.blit(tDescription,(390,200))
                    for line in camp[3]:
                        self.screen.blit(line,(400,200+y))
                        y+=30
                        
                    self.screen.blit(tLength,(390,200+y));y+=30
                    self.screen.blit(camp[4],(400,200+y))
                    
                    n_selected=s
                    
                x=x+50
                s+=1
            
            
            pygame.display.flip()    
        
        pygame.event.clear()
        
        return selected-1
    def __addCounter(self,counter):
        self.__counters.append(counter)
    def __removeCounter(self,counter):
        self.__counters.remove(counter)
    def __goToPreviousState(self):
        self.__state=self.__old_state
    def __switchState(self,newstate):
        if newstate!=self.__state:
            self.__old_state=self.__state
            self.__state=newstate
            self.cursor.lightReset()
    def __exit(self):
        self.quit=True
        sys.exit()
    def __save(self):

        Scenario.game=None
        Unit.game=None
        Map.game=None
        AI.game=None
        Player.game=None
        Cursor.game=None       
        
        
        data=(self.scenario,self.__state,self.__old_state,self.__round,
            self.__skipFighting,self.__skipPlayers,
            self.__undoCache,self.__highlightedTiles)

        try:
            FILE=gzip.open('save.gz', 'w')
            pickle.dump(data, FILE, 2)
            FILE.close()
            Unit.game=self
            Scenario.game=self
            Map.game=self
            AI.game=self
            Player.game=self
            Cursor.game=self
            self.messageBox('Load/Save', ['- Game saved'])
        except:
            Unit.game=self
            Scenario.game=self
            Map.game=self
            AI.game=self
            Player.game=self
            Cursor.game=self
            self.messageBox('Load/Save', ['- Error while saving'])

    def __load(self,title=False):
        if not title:
            s=self.scenario
        self.scenario=None
        
        try:
            FILE=gzip.open('save.gz', 'r', 2)
            self.scenario,self.__state,self.__old_state,self.round,\
            self.__skipFighting,self.__skipPlayers, \
            self.__undoCache,self.__highlightedTiles=pickle.load(FILE)
            FILE.close()
        
            self.getMap().re_init()
            for unit in self.getUnits():
                unit.re_init()
        
            self.messageBox('Load/Save', ['- Game Loaded'])
        except:
            if not title:
                self.scenario=s
                self.messageBox('Load/Save', ['- Error while loading'])
            else:
                return False
        
    def run(self):

        selection=self.__showTitleScreen()
        if selection==END_GAME:
            sys.exit(0)
        elif selection==NEW_CAMPAIGN:
            campaign=self.__campaignSelection()
            debug(camps[campaign]['Name'])
            self.loadScenario(camps[campaign]['Start'])
        elif selection==LOAD_GAME:
            r=self.__load(True)
            if r == False:
                self.run()
                sys.exit()
                
            
        
        lt=pygame.time.get_ticks()
        # main loop
        while not self.quit:
            
            self.__waitForDelay()
            self.__updateScreen()
            if not self.__counters.__len__():
                self.scenario.tick()
            self.__updateInput()
            self.__updateLogic()
            
            if pygame.time.get_ticks()-lt>=100:
                self.cursor.imageEffect()
                lt=pygame.time.get_ticks()
