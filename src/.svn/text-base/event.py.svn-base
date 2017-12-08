from data import *

class Event:
    def __init__(self,scenario,type):
        self.type=type
        self.scenario=scenario
        
    def fire(self):
        self.scenario.handleEvent(self)

class NewRound(Event):
    def __init__(self,scenario):
        Event.__init__(self,scenario,E_NEW_ROUND)
        
class UnitReachedTile(Event):    
    def __init__(self,unit,tile):
        Event.__init__(self,unit.game.scenario,E_UNIT_TILE)
        self.unit=unit
        self.tile=tile

class UnitDied(Event):
    def __init__(self,unit):
        Event.__init__(self,unit.game.scenario,E_UNIT_DIED)
        self.unit=unit
        
class PlayerHasNotUnits(Event):
    def __init__(self,player):
        Event.__init__(self,player.game.scenario,E_PLAYER_NO_UNITS)
        self.player=player

class ObjectiveAchieved(Event):
    def __init__(self,objective):
        Event.__init__(self,objective.scenario,E_OBJ_ACHIEVED)
        self.objective=objective
        
class ObjectiveFailed(Event):
    def __init__(self,objective):
        Event.__init__(self,objective.scenario,E_OBJ_FAILED)
        self.objective=objective
