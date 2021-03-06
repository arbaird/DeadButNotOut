from map import Map
from tmxparser import TMXParser
from res import Resource
from data import *
from event import *
from objective import *
from player import Player
from unit import Unit
from ai import *
from objective import *

#TODO figure out how unit sprite is being set
class Scenario:
    
    game=None
    
    def __init__(self,datadir,start,other=None):
        
        self.__units=[]
        self.__players=[]
        self.__humanplayer=None
        self.__map=None
        self.__vars={}
        self.__objectives=[]
        self.__dataDir=datadir
        self.__start=start
        self.__state=0
        self.setVar('remains',other)
        
    def setState(self,s):
        self.__state=s
    
    def getState(self):
        return self.__state
        
    def load(self):
        self.execute(self.__start[0],self.__start[1])
        
    def execute(self,dir,file):
        file=open(os.path.join('scenarios',self.__dataDir,dir,file))
        print(file)
        exec (file.read())

    def getObjectives(self):
        return self.__objectives
    
    def addObjective(self,objective):
        self.__objectives.append(objective)
        
    def remAllObjectives(self):
        self.__objectives=[]
    
    def remObjective(self,objective):
        if objective in self.__objectives:
            self.__objectives.remove(objective)
    def setVar(self,key,value):
        self.__vars[key]=value
    
    def getVar(self,key):
        if key in self.__vars:#self.__vars.has_key(key):
            return self.__vars[key]
        else:
            return False
    
    def getPlayer(self,ID):
        for player in self.__players:
            if player.getID()==ID:
                return player
    
    def addUnit(self,unit):
        self.__units.append(unit)
    
    def removeUnit(self,unit):
        self.__units.remove(unit)
        
    def getUnits(self):
        return self.__units
    
    def setMap(self,mappath,maptiles,mapdesc):
        file=open(os.path.join('scenarios',self.__dataDir,mapdesc))
        stuff=file.readlines()
        """
        python 2 code, exec can't modify program variables in python3
        for line in stuff:
            if len(line)>1:
                if line[-2]=='\\':
                    tmp+=line[:-2]
                else:
                    if tmp:
                        tmp+=line
                        exec(tmp)
                        tmp=''
                    else:
                        exec (line)
        """
        tiletypes = {}
        mapdesc = []
        for line in stuff:
            if len(line) > 1 and not line.startswith("#"):
                if line[-2] == '\\':
                    line = line[:-2]
                    tmp = line.split(",")
                    for t in tmp:
                        t = t.strip()
                        if t == "":
                            continue
                        tile_info = tiletypes[t]
                        mapdesc.append(tile_info)
                else:
                    tmp = line.split()
                    tile_name = tmp[0]
                    move_cover = tmp[2].split(",")
                    move_cover= [int(info) for info in move_cover]
                    tiletypes[tile_name]  = move_cover

        map=TMXParser().create(os.path.join('scenarios',self.__dataDir,mappath))
        self.__map=Map(map,os.path.join('scenarios',self.__dataDir,maptiles),mapdesc)
    
    def getMap(self):
        return self.__map
    
    def addPlayer(self,player):
        self.__players.append(player)
    
    def setActivePlayer(self,player):
        self.activeplayer=player
        
    def getActivePlayer(self):    
        return self.activeplayer
    
    def setHumanPlayer(self,player):
        self.__humanplayer=player
        
    def getHumanPlayer(self):    
        return self.__humanplayer
    
    def getNumberOfPlayers(self):
        return len(self.__players)
    
    def resetAllUnits(self):
        for unit in self.__units:
            unit.reset()
    
    def removeAllUnits(self):
        self.__units=[]
    
    def tick(self):
        for objective in self.__objectives:
            if objective.test() == FAILED:
                self.game.messageBox("Objective failed:",[objective.descripe()])
                self.remObjective(objective)
                ObjectiveFailed(objective).fire()
            if objective.test() == ACHIEVED:
                self.game.messageBox("Objective achieved:",[objective.descripe()])
                self.remObjective(objective)
                ObjectiveAchieved(objective).fire()
        
        for player in self.__players:
            units=player.getUnits()
            if len(units)==0:
                PlayerHasNotUnits(player).fire()
                
    def handleEvent(self,event):
        pass
        
def fight(attacker,defender,noharm=False):
    Scenario.game.fight(attacker,defender,noharm=noharm)

def getUnitAt(pos):
    return Scenario.game.getUnitAt(pos)

def centerMap(pos,noani=False):
    Scenario.game.centerMap(pos,noani)

def moveMap(dir,count=1,noani=False):
    Scenario.game.moveMap(dir,count,noani)

def moveMapTo(pos,noani=False):
    Scenario.game.moveMapTo(pos,noani)

def getState():    
    return Scenario.game.scenario.getState()

def setState(newstate):
    Scenario.game.scenario.setState(newstate)

def wait(time):
    """Pause the game for 'time'-milliseconds"""
    Scenario.game.wait(time)

def quake(time):
    """The earth will quake for 'time'-milliseconds"""
    Scenario.game.quake(time)

def setVar(key,value):
    """Set variable 'key' to 'value'"""
    Scenario.game.scenario.setVar(key, value)
    
def getVar(key):
    """Get variable 'key'"""
    return Scenario.game.scenario.getVar(key)

def addPlayer(player):
    """Adds a new player to the scenario"""
    Scenario.game.scenario.addPlayer(player)
    
def setHumanPlayer(player):
    """Sets the human player (the player that is controled by the player)"""
    Scenario.game.scenario.setHumanPlayer(player)
    
def setActivePlayer(player):
    """Sets the active player (the player who starts)"""
    Scenario.game.scenario.setActivePlayer(player)

def setMap(a,b,c):
    """Sets the map. a=filename, b=tiles to be used, c=tiles-description"""
    Scenario.game.scenario.setMap(a,b,c)
    
def addObjective(o):
    """Adds a new objective"""
    Scenario.game.scenario.addObjective(o)
    
def showObjectives():
    """Show all objectives"""
    Scenario.game.showObjectives()
    
def remAllObjectives():
    """Removes all objectives"""
    Scenario.game.scenario.remAllObjectives()
    
def highlight(h):
    """Choose tiles that begin to highlight. h must be a tuple like ((2,3),(2,4))"""
    Scenario.game.highlight(h)
    
def getHighlight():
    """Returns all tiles that are highlighted"""
    return Scenario.game.getHighlight()
    
def messageBox(a,b):
    """Shows a message box with title=a and text=b"""
    Scenario.game.messageBox(a,b)

def loadScenario(s):
    """Load a new scenario"""
    Scenario.game.scenario.removeAllUnits()
    Scenario.game.loadScenario(s)
    
def resetAllUnits():
    """Resets all units"""
    Scenario.game.scenario.resetAllUnits()
    
def execute(dir,file):
    Scenario.game.scenario.execute(dir,file)