from data import *
from res import Resource

class Map:
    
    game=None
    
    def __init__(self, arrayMapData, rMapTiles, mapTerDesc):
        self.iMapWidth=arrayMapData[0].__len__()
        self.iMapHeight=arrayMapData.__len__()
        self.position=(0,0)
        self.path=rMapTiles
        self.rMapTiles=Resource(rMapTiles, TILESIZE)
        self.mapDesc=mapTerDesc
        # Mapdata contains of chars representing the enviroment, like plains or mountains
        self.arrayMapData=arrayMapData
        
        # UnitData contains informations if a tile is occupied by a unit
        self.arrayUnitData = [None] * self.iMapHeight
        
        for q in range(self.iMapHeight):
            self.arrayUnitData[q]= [0] * self.iMapWidth
        
        # WalkData contains informations of the movementcost of the  tiles
        self.arrayWalkData = [None] * self.iMapHeight
        
        for q in range(self.iMapHeight):
            self.arrayWalkData[q]= [0] * self.iMapWidth
        
        x=0
        y=0
        for line in self.arrayWalkData:
            for c in line:
                m=self.getMoveCost([x,y])
                self.arrayWalkData[y][x]=m
                x+=1
            x=0
            y+=1

        
        self.create_image()
        
    def re_init(self): 
        self.rMapTiles=Resource(self.path, TILESIZE)
        self.create_image()
        
    def getWalkMap(self,unit):
        game=unit.game
        tmp = [None] * self.iMapHeight
        
        for q in range(self.iMapHeight):
            tmp[q]= [0] * self.iMapWidth
        
        x=0
        y=0
        for line in self.arrayWalkData:
            for c in line:
                if not unit.flying:
                    ID=self.arrayUnitData[y][x]
                    if ID:# is there a unit?
                    
                        o=ID.getOwner()
                        if o!= unit.getOwner():
                            tmp[y][x]=-1
                        else:
                            tmp[y][x]=c
                    elif c==99: # 99 is unwalkable
                        tmp[y][x]=-1
                    else:
                        tmp[y][x]=c
                else:
                    tmp[y][x]=1
                x+=1
            x=0
            y+=1
        
        astar_tmp=[]
        for line in tmp:
            for c in line:
                astar_tmp.append(c)
        
        return astar_tmp
    def getUnit(self,pos):
        if self.isOnMap(pos):
            x,y=pos
            unit=self.arrayUnitData[y][x]
            return unit
            
        else:
            return False
          
    def absToMapPos(self,pos):
        x,y=pos
        x=(x-self.position[0])/TILESIZE
        y=(y-self.position[1])/TILESIZE
        return int(x),int(y)
    
    def isOnMap(self,pos):
        x,y=pos
        if x>self.iMapWidth-1 or x<0 or y>self.iMapHeight-1 or y<0:
            return False
        else:
            
            return True
        
    def mapToAbsPos(self,pos):
        x,y=pos
        x=x*TILESIZE+self.position[0]
        y=y*TILESIZE+self.position[1]
        return (x,y)
    
    def getCover(self,pos):
        x,y=pos
        return self.mapDesc[self.arrayMapData[y][x]][1]
    
    def getMoveCostFast(self,pos,unit=None):
        x,y=pos
        
        if unit:
            fly=unit.flying
        else:
            fly=False
            
        if not self.isOnMap(pos):
            return 99
        else:
            if fly:
                return 1
            else:
                if self.arrayUnitData[y][x]:
                    if unit.getOwner()==self.arrayUnitData[y][x].getOwner():
                        return self.arrayWalkData[y][x]
                    else:
                        return 99
                else:
                    return self.arrayWalkData[y][x]
            
    def getMoveCost(self,pos):
        x,y=pos
        
        if not self.isOnMap(pos):
            return 99
        else:
            if self.arrayUnitData[y][x]:
                return 99
            else:
                return self.mapDesc[self.arrayMapData[y][x]][0]
                

    def create_image(self):    
        """creates an imageCursor (self.sMapImage) representing the map"""
        x=0
        y=0
        self.sMapImage=pygame.Surface((self.iMapWidth*TILESIZE, self.iMapHeight*TILESIZE))
        for line in self.arrayMapData:
            for c in line:
                self.sMapImage.blit(self.rMapTiles.get(c), (x*TILESIZE, y*TILESIZE))
                x+=1
            x=0    
            y+=1        
    
    def add_unit(self,unit):
        self.arrayUnitData[unit.y][unit.x]=unit

    def remove_unit(self,unit):    
        x,y=unit.getPos()
        self.arrayUnitData[y][x]=0

    def moveTo(self,position):
        x,y=position
        self.position=-x*TILESIZE,-y*TILESIZE
        self.correctPos()        
        return self
    
    def center(self,pos):
        nx,ny=pos
        #x,y=self.position
        self.position=-(nx-DISPLAY_X/2)*TILESIZE,-(ny-DISPLAY_Y/2)*TILESIZE
        self.correctPos()
        return self
    
    def correctPos(self):
        x,y=self.position
        if x>0:
            x=0
        if y>0:
            y=0
        if x<(DISPLAY_X-self.iMapWidth)*TILESIZE:
            x=(DISPLAY_X-self.iMapWidth)*TILESIZE
        if y<(DISPLAY_Y-self.iMapHeight)*TILESIZE:
            y=(DISPLAY_Y-self.iMapHeight)*TILESIZE
        self.position=x,y
    def new_move(self,pos):    
        x,y=pos
        ax,ay=self.position
        self.position=ax+x,ay+y
        self.correctPos()
    def move(self,direction):
        x,y=self.position
        off=0
        iff=0
        if x<0:
            if direction==RIGHT:
                off=1
        
        if x>(DISPLAY_X-self.iMapWidth)*TILESIZE:
            if direction==LEFT:
                off=-1
        
        if y<0:
            if direction==DOWN:
                iff=1
        if y>(DISPLAY_Y-self.iMapHeight)*TILESIZE:
            if direction==UP:
                iff=-1
        
        self.position=x+off*TILESIZE,y+iff*TILESIZE
        return self