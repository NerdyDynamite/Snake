# Snake Game

import pygame
import sys
import random
import time

check_errors = pygame.init()

# Error checking and exit if errors present

if check_errors[1] > 0:
    print("(!) Had {0} existing errors, exiting...".format(check_errors[1]))
    sys.exit(-1)
else:
    print("(+) PyGame successfully initialized!")

# set window name
pygame.display.set_caption("Snake Game")

# Play surface
surfSize = (720, 460)
playSurface = pygame.display.set_mode(surfSize)

# Colors
red = pygame.Color(255,0,0) #gameover
green = pygame.Color(0,255,0) #snake
black = pygame.Color(0,0,0) #score
white = pygame.Color(255,255,255) #background
brown = pygame.Color(165,42,42) #food

# FPS controller

fpsController = pygame.time.Clock()
FPS = 10

# Important Variables
snakePos = [100,50]
snakeBody = [[100,50],[90,50],[80,50]]

foodPos = [random.randrange(1,72)*10,random.randrange(1,46)*10]
foodSpawn = True

direction = 'RIGHT'
changeto = direction
score = 0

# Game over function
def gameOver():
    myFont = pygame.font.SysFont('monaco', 72)
    GOsurf = myFont.render('Game Over!', True, red)
    GOrect = GOsurf.get_rect()
    GOrect.midtop = (360, 15)
    playSurface.blit(GOsurf,GOrect)
    showScore(0)
    pygame.display.flip()
    time.sleep(4)
    pygame.quit()
    sys.exit()

def showScore(mode=1):
    myFont = pygame.font.SysFont('monaco', 25)
    Ssurf = myFont.render('Score: ' + str(score), True, white)
    Srect = Ssurf.get_rect()
    
    if mode == 0:
        Srect.midtop = (360, 100)
    else:
        Srect.midtop = (100, 15)
        
    playSurface.blit(Ssurf,Srect)
    pygame.display.flip()
   
# Main Logic

while True:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                changeto = 'RIGHT'
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                changeto = 'LEFT'
            if event.key == pygame.K_UP or event.key == ord('w'):
                changeto = 'UP'
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                changeto = 'DOWN'
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))
                
    # validation of direction
    
    if changeto == 'RIGHT' and not direction == 'LEFT':
        direction = 'RIGHT'
    if changeto == 'LEFT' and not direction == 'RIGHT':
        direction = 'LEFT'
    if changeto == 'UP' and not direction == 'DOWN':
        direction = 'UP'
    if changeto == 'DOWN' and not direction == 'UP':
        direction = 'DOWN'
    
    # update snake position [x,y]
    
    if direction == 'RIGHT':
        snakePos[0] += 10
    if direction == 'LEFT':
        snakePos[0] -= 10
    if direction == 'UP':
        snakePos[1] -= 10
    if direction == 'DOWN':
        snakePos[1] += 10

    # snake body mechanism
    
    snakeBody.insert(0,list(snakePos))
    
    if snakePos[0] == foodPos[0] and snakePos[1] == foodPos[1]:
        score += 1
        FPS += 2
        foodSpawn = False
    else:
        snakeBody.pop()
    
    # Respawn food if necessary
    
    if foodSpawn == False:
        foodPos = [random.randrange(1,72)*10,random.randrange(1,46)*10]
    foodSpawn = True
    
    # change the background color of the game window
    playSurface.fill(black)
    
    # update location of snake 
    for pos in snakeBody:
        pygame.draw.rect(playSurface, green, pygame.Rect(pos[0],pos[1],10,10))
    
    # update location of food
    pygame.draw.rect(playSurface, brown, pygame.Rect(foodPos[0],foodPos[1],10,10))

    # collision and out of bounds logic
    
    for i in range(1,len(snakeBody)):
        if snakeBody[0] == snakeBody[i]:
            gameOver()
            
    if snakePos[0] > surfSize[0]-10 or snakePos[1] > surfSize[1]-10 or snakePos[0] < 0 or snakePos[1] < 0:
        gameOver()
    
    showScore()
    pygame.display.flip()
    fpsController.tick(FPS)
    
    # add menus, sounds, images
    # pyinstaller to get executable