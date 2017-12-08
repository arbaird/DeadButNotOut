from scenario import *

class firstOne(Scenario):

    def handleEvent(self,event):   
        Scenario.handleEvent(self,event)
        if event.type==E_UNIT_DIED:
             event.unit.talk(["I'll be back!"])
        
        if event.type==E_OBJ_ACHIEVED:
            units=getVar('Human').getUnits()
            u=random.choice(units)
            u.talk(["Cool, we have won!"])
            wait(100)
            messageBox("Goodbye",["See ya!"])
            sys.exit()
            
        if event.type==E_OBJ_FAILED:
            units=getVar('CPU').getUnits()
            u=random.choice(units)
            u.talk(["Better take care of","%s next time!"%(event.objective.unit.name)])   
            quake(50)
            for unit in units:
                unit.disappear()
                quake(50)
            wait(100)
            messageBox("Goodbye",["See ya!"])
            sys.exit()
            
    def tick(self):
        Scenario.tick(self)
        
    
Desc={'Name':'t.s.o.t.c.m.',
           'Desc':["The secret of the chocolate milk","A pretty silly campaign"],
           'Length':"short - 2 scenarios",
           'Start':firstOne('tsotcm_data',('01','01_LOAD'))}