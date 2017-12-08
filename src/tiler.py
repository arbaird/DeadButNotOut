#! /usr/bin/python

import pygame,sys,os
from res import *

pygame.init()
screen = pygame.display.set_mode((1024,64))

r=Resource(os.path.join('tiles', 'foes.png'), 32)

x=0
y=20
sFont=pygame.font.Font(os.path.join('fonts','standard.ttf'),12)

while True:
    
    screen.fill((0,0,0))
    for n in range(0,y):
        screen.blit(r.get(x+n),(0+n*32,0))
        screen.blit(sFont.render(str(x+n),True,(255,255,255)),(10+n*32,8))
        
    screen.blit(sFont.render(str(x/y),True,(255,255,255)),(0,32))
        
    pygame.display.flip()
    
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if e.type==pygame.MOUSEBUTTONUP:
            x+=y
        if e.type==pygame.KEYDOWN:
            if e.key==pygame.K_UP:
                x+=y
            if e.key==pygame.K_DOWN:
                x-=y