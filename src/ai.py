import math
import AStar
from data import debug
class AI:
    
    game=None
    
    def __init__(self):
        self.player=False
    
    def act(self):
        pass
    
    def init(self,player):
        self.player=player
    
    def findNearestEnemyUnit(self,unit,target_player=None):
        """Returns the nearest enemy Unit of 'unit'. [unit,distance]"""
        eu=[]
        for eunit in self.player.game.getUnits():
            if not target_player:
                if eunit.getOwner() != self.player:
                    eu.append(eunit)
            else:
                if eunit.getOwner()==target_player:
                    eu.append(eunit)
        
        nearest=False

        if eu.__len__()==0:
            debug("ouch, no units found!")
            
        for eunit in eu:
            dis=math.sqrt(math.pow((eunit.x-unit.x),2)+math.pow((eunit.y-unit.y),2))
            if nearest:
                if dis < nearest[1]:
                    nearest=(eunit,dis)
            else:
                nearest=(eunit,dis)
        
        return nearest
    
    def findPathToNearestTile(self,unit,tile,distance=1):
        """Returns the path from 'unit' to a tile in distance of 'distance' to 'tile',
        if possible""" 
        # check which is the shortest path (4 possibilities)
        startTile=unit.getPos()
        x,y=tile    
                    
        map=self.player.game.getMap()
        wmap=map.getWalkMap(unit)
                        
        astar = AStar.AStar(AStar.SQ_MapHandler(wmap,map.iMapWidth,map.iMapHeight))
        start = AStar.SQ_Location(startTile[0],startTile[1])
                        
        spath=False
        
        tiles={0:(tile,),
               1:((x+1,y),(x-1,y),(x,y+1),(x,y-1))}
        
        posToTest=tiles[distance]
        for ntile in posToTest:
            if not unit.game.getMap().getUnit(ntile):
                try:
                    end = AStar.SQ_Location(ntile[0],ntile[1]);path=[]
                    for n in astar.findPath(start,end).nodes:
                        path.append((n.location.x,n.location.y));
                    if spath:
                        if path.__len__() < spath.__len__():
                            spath=path
                    else:
                        spath=path
                except:
                    pass
                
        if spath:    
            debug("%s walking to %s"%(unit.name,str(spath[-1])))
        return spath
    
    def getMyUnits(self):
        u=[]
        for unit in self.player.game.getUnits():
            if unit.getOwner() == self.player:
                u.append(unit)
        return u
    
class DummyAI(AI):
    
    def act(self):
        for unit in self.getMyUnits():
            unit.finish()
            
class SimpleAI(AI):
    
    def __init__(self):
        AI.__init__(self)
        self.foe=None
    
    def attackOnly(self,player):
        self.foe=player

    def act(self):
        for unit in self.getMyUnits():
            if not unit.hasFinished():
            
                nearest=self.findNearestEnemyUnit(unit,self.foe)
                # move to nearest unit if dis > 1
                if nearest:
                    debug("%s (%i %i) -> %s (%i %i)"%(unit.name,unit.x,unit.y,nearest[0].name,nearest[0].x,nearest[0].y))
                    if nearest[1]>1:
                        spath=self.findPathToNearestTile(unit, nearest[0].getPos(), 1)
                        if spath:
                            self.game.centerMap(unit)
                            self.player.game.moveUnit(unit,spath[-1])
                        else:
                            debug( "%s finds no way to target..."%(unit.name))
                                
                    nearest=self.findNearestEnemyUnit(unit,self.foe)
                    if nearest[1]==1:
                        self.game.centerMap(unit)
                        self.player.game.fight(unit,nearest[0])            
            
            unit.finish()
            self.game.wait(60)
            
class CowardAI(AI):
    def __init__(self):
        self.safe=None
        
    def setSafe(self,tiles):
        self.safe=tiles
    
    def findNearestSafe(self,unit):
        nearest=False
        for pos in self.safe:
            x,y=pos
            dis=math.sqrt(math.pow((x-unit.x),2)+math.pow((y-unit.y),2))
            if nearest:
                if dis < nearest[1]:
                    nearest=(pos,dis)
            else:
                nearest=(pos,dis)
        
        return nearest
        
    def act(self):
        for unit in self.getMyUnits():
            if not unit.hasFinished():
                nearest=self.findNearestSafe(unit)
                if nearest:
                    if nearest[1]>0:
                        spath=self.findPathToNearestTile(unit, nearest[0], 0)
                        if spath:
                            self.game.centerMap(unit)
                            unit.walkTo(spath[-1])
            if unit.getPos() in self.safe:
                unit.escape()
            unit.finish()
            self.game.wait(60)