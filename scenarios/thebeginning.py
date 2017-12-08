from scenario import *

class part01(Scenario):
        
    def handleEvent(self,event):   
        Scenario.handleEvent(self,event)
        
        if event.type == E_OBJ_ACHIEVED and getState()==1:
            if event.objective.type == OBJ_KILLALLENEMIES:
                 setState(2)
            
        if event.type == E_OBJ_FAILED:
            execute('01','01_LOSE')
            
        if event.type == E_PLAYER_NO_UNITS:
            if event.player == getVar('Player'):
                if getState()==3:
                    execute('01','01_WIN')
                    loadScenario(part02('thebeginning_data',('02','02_LOAD'),getVar('escaped')))
                else:
                    execute('01','01_LOSE')
        
        if event.type == E_UNIT_TILE and getState()==3:
            if event.unit.getOwner() == getVar('Player'):
                if event.tile in getHighlight():
                    v=getVar('escaped')
                    v.append(event.unit)
                    setVar('escaped',v)
                    event.unit.escape()
                    
    def tick(self):
        Scenario.tick(self)
        if getState()==2:
            execute('01','01_2')
    
class part02(Scenario):
    
    def handleEvent(self,event):   
        Scenario.handleEvent(self,event)
        if event.type == E_NEW_ROUND:
            if getState()==1:
                r=getVar('Round')
                if not r:
                    setVar('Round',1)
                else:
                    setVar('Round',getVar('Round')+1)
                if getVar('Round')==2:
                    execute('02','02_2')
                if getVar('Round')==3:
                    execute('02','02_3')
        if event.type==E_UNIT_TILE:
            if event.tile in getHighlight():
                if event.unit.getOwner()==getVar('Folks'):
                    messageBox('Objective achieved:',['- A citizen escaped'])
                    
        if event.type == E_OBJ_ACHIEVED:
            execute('02','02_WIN')
        if event.type == E_OBJ_FAILED:
            execute('02','02_LOSE')
    
    def tick(self):
        Scenario.tick(self)
        
            
            
Desc={'Name':'The Beginning ',
        'Desc':["This is the the new main campaign."],
        'Length':"medium",
        'Start':part01('thebeginning_data',('01','01_LOAD'))}        
        
