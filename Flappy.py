import pygame as pg
import sys
import math
import random


pg.init()
pts = 0
gravity = 1.5


#Define global variabes 
def Variables():
    global run
    run = True
    global dead
    dead = False
    global Default
    Default = True
    global Up
    Up = False
    global Pause
    Pause = True
    global Collision
    Collision = False
    global score
    score = 0

    
#Define screen and captions
screen = pg.display.set_mode((800,600))
pg.display.set_caption('FlappyBird')
#Load sprites
bird = pg.image.load('Sprites/Bird.png')
bird_up = pg.image.load('Sprites/Bird_Up.png')
pipe_Up = pg.image.load('Sprites/PipeUp.png')
pipe_Down = pg.image.load('Sprites/PipeDown.png')
ground = pg.image.load('Sprites/Ground.png')
background = pg.image.load('Sprites/Background.png')


#That is the Bird Class
class Bird():
    X = 250
    Y = 250
    speed = 1
    
    #This Function makes our bird fly 
    def Flying():
        global Default,Up
        #This makes gravity's action on our game possible
        Bird.Y += gravity
        
        #The following 2 if blocks check if the bird is standing idle or is actually jumping/flying up and it changes it's
        #Animation accordingly 
        if Default:
            screen.blit(bird,(Bird.X,Bird.Y))
        elif not Default and Up==True:
            screen.blit(bird_up,(Bird.X,Bird.Y))
            Default = True
            Up = False
        #This if block checks if the game is paused and if it is it also makes our bird fly in a small sine wave. The code also
        #shows us the starting text that reads "Press space to begin"
        if Pause:
            Bird.Y = 250+ math.sin(pts/10)*15
            Bird.StartingText()
        
        
        
    #Losing Conditions
        if Bird.Y >= 525:
            Bird.die()
        if Bird.Y <= 0:
            Bird.Y += 25
        
         
    
            
    def die():
        global dead, run
        screen.blit(gameOverText,(200,50))
        Collision = True
        dead = True
        run = False
        
    

class Pipes():
    #Set X and Y coordinates for the Pipes 
    X = random.randint(250,750)
    Y = random.randint(250, 300) 
    
    def ShowPipes():
        #What this function does is it checks if the game has started(space has been pressed) and it starts moving
        #the pipes around, then it also checks if the bird has collided with the pipes themselves, and it blits the score on the
        #screen
        if not Pause:
            screen.blit(pipe_Up, (Pipes.X,Pipes.Y))
            screen.blit(pipe_Down, (Pipes.X,-Pipes.Y))
            Pipes.X -= 5
            if Pipes.X <= 0:
                Pipes.X = random.randint(300,700)
                Pipes.Y = random.randint(250, 500) 
        if Bird.Y > Pipes.Y and Bird.X > Pipes.X:
            Bird.die()
        if Bird.Y < -Pipes.Y and Bird.X > Pipes.X:
            Bird.die()
        screen.blit(scoreText,(0,0))


def MovingGround():
    #What this function does is it shows us the ground sprite and it makes it seem as if it is moving, depending on how much pts
    #one has(not score)
    x = 0
    x = pts-800
    screen.blit(ground,(x,550))
   
#Here we call the Variables function which contains all the global variables, we'll use later on
Variables()
#That is the main game loop
while run:  
    #Here are all the fonts I'd use later on
    font = pg.font.Font('PixelFJVerdana12pt.ttf', 25)
    text=font.render('Press space to begin', True,(0,0,0))
    gameOverText = font.render('Game Over', True,(0,0,0))
    scoreText = font.render('Score: ' + str(score), True,(0,0,0))
    
    #That is an event handler
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
        #The if block below checks if a mouse button is pressed and if it is, then the bird moves by 25 pixels upwards on the Y scale
        elif event.type == pg.MOUSEBUTTONDOWN:
            Bird.Y-=25
            Default=False
            Up=True
        #What this if block does is it checks for a pressed key and if that key is space then the game starts
        elif event.type == pg.KEYDOWN:
            if event.key ==pg.K_SPACE:
                Pause = False
        
    #This if block checks if the bird is still alive         
    if not dead:
        pts+=1
        #This if block checks if the maximum amount of pts(not score) has been reached and if it has then it is reset back to 1
        if pts >= 400:
            pts = 1
        #This if block checks if the bird has made it through the Pipes and gives us a point in doing so 
        if Collision==False and Pipes.X <= 5:
            score+=1


    screen.blit(background,(0,0))
    Bird.Flying()
    Pipes.ShowPipes()
    MovingGround()
    pg.display.flip()