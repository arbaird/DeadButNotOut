import pygame

class Resource:
    def __init__(self, name, tilesize,surf=False):
        
        self.res=self.load_image(name)
        _, _, w, h=self.res.get_rect()
        self.tiles=[]
        for y in range(0, int(h/tilesize)):
            for x in range(0, int(w/tilesize)):
                tile = pygame.Surface((tilesize, tilesize), depth=self.res)
                chop_rect=(x*tilesize, y*tilesize, tilesize, tilesize)
                tile.blit(self.res, (0, 0), chop_rect)
                self.tiles.append(tile)
                
    def get(self, no):
        return self.tiles[no]
    
    def load_image(self, name):
        try:
            image = pygame.image.load(name)
        except pygame.error:#, message:
            print ('Cannot load imageCursor:', name)
            raise SystemExit#, message

        image = image.convert_alpha()
        image.set_alpha(255, pygame.RLEACCEL)
        return image