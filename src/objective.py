from data import *

class Objective:
    
    game=None
    
    def __init__(self,scenario,type):
        self.desc="Emtpy event"
        self.type=type
        self.scenario=scenario
    
    def isAchieved(self):
        return False
    
    def describe(self):
        return "empty"

    def test(self):
        return RUNNING

class ObjCustom(Objective):
    def __init__(self,scenario,text):
        Objective.__init__(self,scenario,OBJ_CUSTOM)
        self.text=text
    
    def descripe(self):
        return self.text
    
class ObjUnitMayNotDie(Objective):
    def __init__(self,unit):
        Objective.__init__(self,unit.game.scenario,OBJ_UNITMAYNOTDIE)
        self.unit=unit
        
    def test(self):
        if self.unit.isAlive() or self.unit.escaped:
            return RUNNING
        else:
            return FAILED
        
    def descripe(self):
        return self.unit.name + " may not die"

class ObjUnitMustEscape(Objective):
    def __init__(self,unit):
        Objective.__init__(self,unit.game.scenario,OBJ_UNITMUSTESCAPE)
        self.unit=unit
        
    def test(self):
        if self.unit.escaped:
            return ACHIEVED
        else:
            if self.unit.isAlive():
                return RUNNING
            else:
                return FAILED
        
    def descripe(self):
        return self.unit.name + " must escape"
    
class ObjKillAllUndead(Objective):
    def __init__(self,scenario):
        Objective.__init__(self,scenario,OBJ_KILLALLUNDEAD)
        
    def test(self):
        units=self.scenario.getUnits()
        for unit in units:
            if unit.flags & U_UNDEAD:
                    return RUNNING
        return ACHIEVED
    
    def descripe(self):
        return "Kill all Undead"
    
class ObjKillEnemies(Objective):
    def __init__(self,scenario):
        Objective.__init__(self,scenario,OBJ_KILLALLENEMIES)
        
    def test(self):
        units=self.scenario.getUnits()
        for unit in units:
            if unit.getOwner() != self.scenario.getHumanPlayer():
                    return RUNNING
        return ACHIEVED
    
    def descripe(self):
        return "Kill all Enemies"
    