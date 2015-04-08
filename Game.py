import pygame, math, sys, os
from Entity import Entity
from Player import Player
from MainMenu import Button
#from BackGround import BackGround
#from Level import Level
#from Block import Block
pygame.init()

clock = pygame.time.Clock()

width = 800 
height = 600
size = width, height

bgColor = r,g,b = 0, 0, 10

screen = pygame.display.set_mode(size)

bgImage = pygame.image.load("RSC/Background Images/basichallway.png").convert()
bgImage = pygame.transform.scale(bgImage, size)
bgRect = bgImage.get_rect()

entities = pygame.sprite.Group()
players = pygame.sprite.Group()
hudItems = pygame.sprite.Group()
backgrounds = pygame.sprite.Group()
blocks = pygame.sprite.Group()
all = pygame.sprite.OrderedUpdates()

Entity.containers = (all, entities)
Player.containers = (all, players)

#BackGround.containers = (all, backgrounds)
#Block.containers = (all, blocks)

run = False


startButton = Button([width/2, height-300], 
				 "RSC/Enemy Images/yee.png", 
				 "RSC/Enemy Images/sh.png")

while True:
    while not run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    run = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                startButton.click(event.pos)
            if event.type == pygame.MOUSEBUTTONUP:
                if startButton.release(event.pos):
                    run = True
                
    bgColor = r,g,b
    screen.fill(bgColor)
    screen.blit(bgImage, bgRect)
    screen.blit(startButton.image, startButton.rect)
    pygame.display.flip()
    clock.tick(60)
    
    bgImage = pygame.image.load("images/Screens/Main Screen.png").convert()
    bgRect = bgImage.get_rect()
    BackGround("images/Screens/Main Screen.png")
    
    player = PlayerBall([width/2, height/2])
    
    
    level = Level(size, 50)
    level.loadLevel("1")

    timer = Score([80, height - 25], "Time: ", 36)
    timerWait = 0
    timerWaitMax = 6

    score = Score([width-80, height-25], "Score: ", 36)
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                player.go("up")
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                player.go("right")
            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                player.go("down")
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                player.go("left")
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                player.go("stop up")
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                player.go("stop right")
            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                player.go("stop down")
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                player.go("stop left")
        
    if len(balls) < 10:
        if random.randint(0, 1*60) == 0:
                Ball("images/Ball/ball.png",
                      [random.randint(0,10), random.randint(0,10)],
                      [random.randint(100, width-100), random.randint(100, height-100)])
                          
    for block in level.hardBlocks:
            player.collideBlock(block)
            for Entity in Entity:
                Entity.collideBlock(block)
                      
    if timerWait < timerWaitMax:
        timerWait += 1
    else:
        timerWait = 0
        timer.increaseScore(.1)
        
        playersHitBalls = pygame.sprite.groupcollide(players, balls, False, True)
        ballsHitBalls = pygame.sprite.groupcollide(balls, balls, False, False)
        
        for player in playersHitBalls:
            for ball in playersHitBalls[player]:
                score.increaseScore(1)
                
        for bully in ballsHitBalls:
            for victem in ballsHitBalls[bully]:
                    bully.collideBall(victem)
                    
        for block in level.blocks:
            screen.blit(block.image, block.rect)
    
        all.update(width, height)

        dirty = all.draw(screen)
        pygame.display.update(dirty)
    pygame.display.flip()
    clock.tick(60)
