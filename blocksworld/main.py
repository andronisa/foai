import pygame, sys, time
from pygame.locals import *
from py8puzzel import *

puzzle=puzzel() 
#puzzle.Solve()

pygame.init()
WINDOWWIDTH = 600
WINDOWHEIGHT = 600
BASICFONT = pygame.font.Font('freesansbold.ttf',50)
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption('8 Puzzle')

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE=(255,255,255)
Text=(0,0,0)

blockTOP=0;
blockLEFT=0;
blocks=[]
blockNumber=1

for i in range(3):
    for j in range(3):
       
        if blockNumber>8:
            blocks.append({'rect':pygame.Rect(blockLEFT,blockTOP,99,99),'color':BLACK,'block':str(0)})
        else:
            blocks.append({'rect':pygame.Rect(blockLEFT,blockTOP,99,99),'color':GREEN,'block':str(blockNumber)})
        blockNumber+=1
        blockLEFT+=100
    blockTOP+=100
    blockLEFT=0

for b in blocks:        
        pygame.draw.rect(windowSurface, b['color'], b['rect'])
        textSurf = BASICFONT.render(b['block'], True,Text)
        textRect = textSurf.get_rect()
        textRect.center = b['rect'].left+50,b['rect'].top+50
        windowSurface.blit(textSurf, textRect)
pygame.display.update()
     
numShufles=50
evt=False  
while True:
    # check for the QUIT event
    for event in pygame.event.get():
        if event.type==MOUSEBUTTONDOWN and event.button==1:
            evt=True
            
    while numShufles>0:
        puzzle.shufler()
        puzzle.PreviousNode.extend(puzzle.StartNode)
        block=0
        for b in blocks:
            b['block']=str(puzzle.StartNode[block])
            block+=1
            
            if b['block']=='0':
                b['color']=BLACK
            else:
                b['color']=GREEN         
            pygame.draw.rect(windowSurface, b['color'], b['rect'])
            textSurf = BASICFONT.render(b['block'], True,Text)
            textRect = textSurf.get_rect()
            textRect.center = b['rect'].left+50,b['rect'].top+50
            windowSurface.blit(textSurf, textRect)
        pygame.display.update()
        time.sleep(0.04)
        numShufles-=1
        
        
    if evt==True:
            puzzle.sucessor(puzzle.StartNode)
            nxNode=puzzle.getNextNode()
            
            block=0
            for b in blocks:
                b['block']=str(nxNode[block])
                block+=1
                
                if b['block']=='0':
                    b['color']=BLACK
                else:
                    b['color']=GREEN         
                pygame.draw.rect(windowSurface, b['color'], b['rect'])
                textSurf = BASICFONT.render(b['block'], True,Text)
                textRect = textSurf.get_rect()
                textRect.center = b['rect'].left+50,b['rect'].top+50
                windowSurface.blit(textSurf, textRect)
            pygame.display.update()
            time.sleep(0.3)
            count=1
            
            while nxNode!=puzzle.GoalNode:
                #print(self.fronts)
                
                count+=1
                puzzle.sucessor(nxNode)
                nxNode=puzzle.getNextNode()
                block=0
                for b in blocks:
                    b['block']=str(nxNode[block])
                    block+=1
                    
                    if b['block']=='0':
                        b['color']=BLACK
                    else:
                        b['color']=GREEN         
                    pygame.draw.rect(windowSurface, b['color'], b['rect'])
                    textSurf = BASICFONT.render(b['block'], True,Text)
                    textRect = textSurf.get_rect()
                    textRect.center = b['rect'].left+50,b['rect'].top+50
                    windowSurface.blit(textSurf, textRect)
                pygame.display.update()
                time.sleep(0.03)
            break
                  
            
while True:
    # check for the QUIT event
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()