from data import *
import AStar
class Cursor:
    """The cursor-class is for selecting units and showing the tiles a unit can reach with its
    movement or during a fight. It also shows tooltips when hoovering with the mouse over an
    unit."""
    game=None
    
    def __init__(self):

        self.position=False
        self.__image=self.game.Ressources['cursor'].get(0)
        self.imageCursor2=self.game.Ressources['cursor'].get(1)
        self.imageBlue=self.game.Ressources['cursor'].get(2)
        self.imageRed=self.game.Ressources['cursor'].get(3)
        self.imageGreen=self.game.Ressources['cursor'].get(4)
        
        self.arrows=[]
        for x in range (8):
            self.arrows.append(self.game.Ressources['arrows'].get(x))
        
        #self.sword=self.game.Ressources['move'].get(0)
        #self.move=self.game.Ressources['move'].get(1)
        #self.heal=self.game.Ressources['move'].get(2)
        
        self.c_fx=self.game.Ressources['cursor_fx']
        self.c_fx_c=-EFFECT_PAUSE
        
        self.tooltip=False
        self.last_tick=False
        self.unit=False
        self.highlightMove=[]
        self.highlightFight=[]
        self.toolTipFont=sFont
        self.toolTipFontBold=sBFont
        
        self.wflags=wflags
        self.uflags=uflags
        self.wtypes=wtypes
        
    def imageEffect(self):
        self.c_fx_c+=1
        if self.c_fx_c==6:
            self.c_fx_c=-EFFECT_PAUSE
        
    def isActive(self): 
        if self.position:
            return True
        
    def setPosition(self,unit):
        if unit!=self.unit:
            self.reset()
            self.position=unit.getAbsolutePosition()
            self.unit=unit
            self.resetToolTip()
        
    def reset(self):
        self.position=False
        self.last_tick=False
        self.tooltip=False
        self.unit=False
        self.highlightMove=[]
        self.highlightFight=[]
    
    def lightReset(self):    
        self.highlightMove=[]
        self.highlightFight=[]
        
    def __test(self,pointToTest):
        
        x,y,mpLeft=pointToTest
        n=self.game.getMap().getMoveCostFast([x,y-1],self.unit)
        s=self.game.getMap().getMoveCostFast([x,y+1],self.unit)
        w=self.game.getMap().getMoveCostFast([x-1,y],self.unit)
        e=self.game.getMap().getMoveCostFast([x+1,y],self.unit)
        return mpLeft-n,mpLeft-s,mpLeft-w,mpLeft-e
        
    def findTilesToHighlight(self):
        """Determinate Tiles which the Unit can reach this turn."""
        if self.highlightMove:
            return False
        
        if self.unit:
            if not self.unit.isAlive():
                return False
        else:
            return False
        
        
        allreadyTestet=[]
        
        # Tiles we want to __test
        fieldsToTest=[]
        
        # Tiles that can be reached
        fieldsOK=[]    

        # start with the tile the unit is standing on
        fieldsToTest.append((self.unit.x,self.unit.y,self.unit.getMovementLeft()))
        
        # as long as there are tile we need to __test, __test them ;)
        while len(fieldsToTest)!=0:
            
            # get the first tile and the movement points that are left
            f=fieldsToTest[0]
            
            # sx: x_position, sy: y_position, m: movement points left
            sx,sy,m=f
            
            # __test if there would be mp left if we would move in n,s,w or e direction
            if f not in allreadyTestet:
                allreadyTestet.append(f)
                n,s,w,e=self.__test(f)
                
                if (n>=0):
                    fieldsOK.append((sx,sy-1))
                    if n>0:
                        # movement points left, so add point to checklist
                        if not [sx,sy-1,n] in fieldsToTest:
                            fieldsToTest.append((sx,sy-1,n))
                if (s>=0):
                    fieldsOK.append((sx,sy+1))
                    if s>0:
                        if not [sx,sy+1,n] in fieldsToTest:
                            fieldsToTest.append((sx,sy+1,s))
                if (w>=0):
                    fieldsOK.append((sx-1,sy))
                    if w>0:
                        if not [sx-1,sy,n] in fieldsToTest:
                            fieldsToTest.append((sx-1,sy,w))
                if (e>=0):
                    fieldsOK.append((sx+1,sy))
                    if e>0:
                        if not [sx+1,sy,n] in fieldsToTest:
                            fieldsToTest.append((sx+1,sy,e))
            
            # remove testet tile
            fieldsToTest=fieldsToTest[1:]
            
        
        fieldsOK.append(self.unit.getPos())
            
        # remove duplicates
        b=[]
        [b.append(i) for i in fieldsOK if not b.count(i)]
        
        # remove tiles already containing a unit 
        # only if unit is flying, because map.getMoveCost handles it so ;)
        if self.unit.flying:  
            listToRemove=[]
            for tile in b:
                if self.game.getMap().arrayUnitData[tile[1]][tile[0]]:
                    listToRemove.append(tile)
            for tile in listToRemove:
                b.remove(tile)
        
        #b = all tiles we can reach, now find all tiles we can attack
        #r = all tiles we can fight
        r=[]
        for tile in b:
            tilesToTest=self.findTilesToHighlightFight(tile)
            for newTile in tilesToTest:
                if newTile not in b and newTile not in r and newTile != (self.unit.x,self.unit.y):
                    r.append(newTile)
        
        if b.__len__()==0:
            tilesToTest=self.findTilesToHighlightFight((self.unit.x,self.unit.y))
            for newTile in tilesToTest:
                if newTile not in b and newTile not in r and newTile != (self.unit.x,self.unit.y):
                    r.append(newTile)
        
        self.highlightMove=b
        self.highlightFight=r
        
    def findTilesToHighlightFight(self,tile=None):

        if not tile:
            tile=(self.unit.x,self.unit.y)

        range=self.unit.weapons[self.unit.selectedWeapon]['Range']
                
        x=tile[0]
        y=tile[1]
        fields=[]
        if range==1 or range==3:
            fields.append((x+1,y))  
            fields.append((x-1,y))  
            fields.append((x,y+1))  
            fields.append((x,y-1))  
        if range==2 or range==3:
            fields.append((x+2,y))  
            fields.append((x-2,y))  
            fields.append((x,y+2))  
            fields.append((x,y-2))  
            
            fields.append((x+1,y+1))  
            fields.append((x-1,y-1))  
            fields.append((x-1,y+1))  
            fields.append((x+1,y-1))  
         
        return fields
            
    def show(self):
        
        state=self.game.getState()
        
        if self.unit:
            self.position=self.unit.getAbsolutePosition()
        
        # activce: cursor is over an unit
        if self.isActive():
            
            # the player can select a unit, so show the cursor
            if state==PLAYER_SELECT_UNIT:
                self.game.screen.blit(self.__image,self.position)
                if self.tooltip:
                    self.game.screen.blit(self.tooltip[1],(self.position[0]+TOOL_TIP_OFFSET+TOOL_TIP_SHADOW_OFFSET,self.position[1]+TOOL_TIP_OFFSET+TOOL_TIP_SHADOW_OFFSET)) 
                    self.game.screen.blit(self.tooltip[0],(self.position[0]+TOOL_TIP_OFFSET,self.position[1]+TOOL_TIP_OFFSET)) 
            
            else:
                # findTilesToHighlight all tiles the unit can reach
                for field in self.highlightMove:
                    self.game.screen.blit(self.imageBlue,self.game.getMap().mapToAbsPos(field))
                    if self.c_fx_c>=0:
                        self.game.screen.blit(self.c_fx.get(self.c_fx_c),self.game.getMap().mapToAbsPos(field))    
                
                # cursor pos
                x,y=self.game.getMap().absToMapPos(pygame.mouse.get_pos())
                if (x,y) in self.highlightMove and (x,y) != self.unit.getPos():
                        # we can reach the tile
                        # create a path
                        startTile=self.unit.getPos()
                        map=self.game.getMap()
                        wmap=map.getWalkMap(self.unit)
                        astar = AStar.AStar(AStar.SQ_MapHandler(wmap,map.iMapWidth,map.iMapHeight))
                        start = AStar.SQ_Location(startTile[0],startTile[1])
                        end = AStar.SQ_Location(x,y)
                        p = astar.findPath(start,end)
                        path=[]
                        
                        for n in p.nodes:
                            path.append((n.location.x,n.location.y))
                        
                        x=0

                        for pos in path:
                            if len(path)>x+1:
                                i=0
                                if path[x+1][0] < pos[0]:
                                    i=6
                                elif path[x+1][0] > pos[0]:
                                    i=2
                                else:
                                    if path[x+1][1] < pos[1]:
                                        i=4
                                    if path[x+1][1] > pos[1]:
                                        i=0
                                self.game.screen.blit(self.arrows[i],self.game.getMap().mapToAbsPos((pos)))
                                x+=1
                
                #self.game.screen.blit(self.arrows[0],self.game.getMap().mapToAbsPos(field))
                
                
                # attack    
                if self.unit.weapons[0]['Flags'] & F_HEAL:
                    img=self.imageGreen
                else:
                    img=self.imageRed
                    
                for field in self.highlightFight:
                    # when a unit is selected, show all tiles it could attack
                    if state==PLAYER_SELECT_MOVE_TO:
                        self.game.screen.blit(img,self.game.getMap().mapToAbsPos(field))
                        if self.c_fx_c>=0:
                            self.game.screen.blit(self.c_fx.get(self.c_fx_c),self.game.getMap().mapToAbsPos(field))
                    else:
                        eu=self.game.getMap().getUnit(field)
                        if eu:
                            a=eu.getOwner();b=self.unit.getOwner()
                            heal=self.unit.weapons[0]['Flags'] & F_HEAL
                            undead=eu.flags&U_UNDEAD
                            if (a==b and heal) or (a!=b and not (heal and not undead)):
                                self.game.screen.blit(img,self.game.getMap().mapToAbsPos(field))
                                # to hit
                                if eu.getOwner()!=self.unit.getOwner():
                                    text=createText("%i %%"%(self.game._GameEngine__getToHit(eu)),sBFontS,WHITE)
                                    x,y=self.game.getMap().mapToAbsPos(field)
                                    self.game.screen.blit(text,(x,y+16))
                                    #self.game.screen.blit(self.sword,(x,y))
                                # effect
                                if self.c_fx_c>=0:
                                    self.game.screen.blit(self.c_fx.get(self.c_fx_c),self.game.getMap().mapToAbsPos(field))
            
                # draw cursor around selected unit
                self.game.screen.blit(self.__image,self.position)
                
                # draw the cursor
                if state==PLAYER_SELECT_MOVE_TO:
                    # draw cursor if mouse is over a tile the unit can reach
                    x,y=self.game.getMap().absToMapPos(pygame.mouse.get_pos())
                    if (x,y) in self.highlightMove:
                        # cursor !!!!!! --------------------
                        self.game.screen.blit(self.__image,self.game.getMap().mapToAbsPos((x,y)))
       
                if state==PLAYER_SELECT_FIGHT_TO:
                    # draw cursor if mouse is over a tile the unit can reach
                    x,y=self.game.getMap().absToMapPos(pygame.mouse.get_pos())
                    eu=self.game.getMap().getUnit((x,y))
                    if eu and (x,y) in self.highlightFight:
                        a=eu.getOwner();b=self.unit.getOwner()
                        heal=self.unit.weapons[0]['Flags'] & F_HEAL
                        undead=eu.flags&U_UNDEAD
                        if (a==b and heal) or (a!=b and not (heal and not undead)):
                            self.game.screen.blit(self.__image,self.game.getMap().mapToAbsPos((x,y)))
        else:
            x,y=self.game.getMap().absToMapPos(pygame.mouse.get_pos())
            mx,my=self.game.getMap().position
            if x<self.game.getMap().iMapWidth and y<self.game.getMap().iMapHeight:
                if x<DISPLAY_X-mx/TILESIZE:
                    self.game.screen.blit(self.imageCursor2,self.game.getMap().mapToAbsPos([x,y]))
            
    def createNewTooltip(self):
        f=self.toolTipFont
        fb=self.toolTipFontBold
        u=self.unit
        
        line_flags=0
        line_weaps=0
        line_uflags=0
        weap=[]
        for weapon in u.weapons:
            flags=[]
            for flag in FLAGS:
                if weapon['Flags'] & flag:
                    flags.append(self.wflags[flag])
                    line_flags+=1
                    
            damOrHeal=""
            if weapon['Flags'] & F_HEAL:
                damOrHeal="heals "
            if self.unit.selectedWeapon==line_weaps/2:
                weap.append([fb.render("- " + weapon['Name']+" *",True,BLACK),
                        f.render(damOrHeal+" "+str(weapon['Damage'])+" Dam. average "+ self.wtypes[weapon['Type']],True,BLACK),
                        flags])
            else:
                weap.append([fb.render("- " + weapon['Name'],True,BLACK),
                        f.render(damOrHeal+"  "+str(weapon['Damage'])+" Dam. average "+ self.wtypes[weapon['Type']],True,BLACK),
                        flags])
            line_weaps+=2
        
        alluflags=[]
        for uflag in UFLAGS:
            if u.flags & uflag:
                alluflags.append(self.uflags[uflag])
                line_uflags+=1
            
        all=line_weaps+line_flags+line_uflags
        tooltip=pygame.Surface((165,(all+3)*14))
        border=pygame.Surface((165+8,(all+3)*14+8))
        
        shadowpart=pygame.Surface((165+8,(all+3)*14+8),pygame.SRCALPHA,32).convert()
        shadowpart.set_alpha(100)

        tooltip.fill(TOOL_TIP_COLOR)
        border.fill(TOOL_TIP_COLOR2)
        
        t=fb.render(u.name,True,BLACK)
        tooltip.blit(t,(2,2))
        
        s="%s - %i/%i HP"%(u.getOwner().name,u.hp_ac,u.hp)
        tooltip.blit(f.render(s,True,BLACK),(2,15))

        x=26
        
        for flag in alluflags:
            
            tooltip.blit(flag,(2,2+x));x+=14
        
        x+=14
        for weapon in weap:
            tooltip.blit(weapon[0],(2,2+x));x+=14
            tooltip.blit(weapon[1],(2,2+x));x+=14
            for line in weapon[2]:
                tooltip.blit(line,(8,2+x));x+=14

        
        border.blit(tooltip,(4,4))
        #toolTipSurface.blit(shadowpart,(4,4))        
        #toolTipSurface.blit(border,(0,0))
        self.tooltip=border,shadowpart
            
    def getUnit(self):
        if self.isActive():
            return self.unit
        else:
            return False
            
    def isReachable(self,pos):
        if pos in self.highlightMove:
            return True
        else:
            return False
    def isFightable(self,pos):
        if pos in self.highlightFight:
            return True
        else:
            return False
        
    def resetToolTip(self):
        self.tooltip=False
    
    def tick(self):    
        if self.last_tick==False:
            self.last_tick=pygame.time.get_ticks()
        else:
            if pygame.time.get_ticks()-self.last_tick>=TIME_TILL_TOOLTIP:
                if not self.tooltip:
                    self.createNewTooltip()
            