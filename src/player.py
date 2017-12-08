class Player:
    
    game=None
    
    def __init__(self,scenario,ID,name,AI=False):
        self.__ID=ID
        self.finished_movement=False
        self.name=name
        if AI:
            self.__AI=AI
            self.__AI.init(self)
        else:
            self.__AI=False
    
    def getAI(self):
        return self.__AI
    
    def act(self):
        if self.__AI:
            self.__AI.act()
        
    def getID(self):
        return self.__ID
            
    def getUnits(self):
        myunits=[]
        for unit in self.game.getUnits():
            if unit.getOwner()==self:
                myunits.append(unit)
                
        return myunits