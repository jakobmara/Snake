import pygame
from random import randint
pygame.init()

BLACK = (0,0,0)
WHITE=(255,255,255)
GREEN = (0,255,0)
YELLOW = (255,255,0)
RED = (255,0,0)

HEIGHT = 704
WIDTH = 512

GLENGTH = 44
GHEIGHT = 32



#I THINK THERES AN ISSUE IF THE FOOD SPAWNS INSIDE THE SNAKE


size = (HEIGHT, WIDTH)
gameDisplay = pygame.display.set_mode(size)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Jake the Snake                                                                                                                          Highscore: 0")
largeFont = pygame.font.Font('freesansbold.ttf',115)
smallFont = pygame.font.Font('freesansbold.ttf',20)
title = largeFont.render("Snake",True,WHITE)
playText = smallFont.render("Play",True,BLACK)


 



def drawSquare(posX, posY):
    pygame.draw.rect(gameDisplay, WHITE,(posX*16,posY*16,15,15))



def delSquare(posX,posY):
    pygame.draw.rect(gameDisplay, BLACK,(posX*16,posY*16,15,15))

#determine/draw new food position
def randSquare(body):
    foodX = randint(0,43) #had to go 1 less trhan max cuz off screen
    foodY = randint(0,31)
    foodLoc = [foodX,foodY]
    #this loop is so that the new food location doesn't spawn within the snake body
    while(body.count(foodLoc) >= 1):
        foodX = randint(0,43) #had to go 1 less trhan max cuz off screen
        foodY = randint(0,31)
        foodLoc = [foodX,foodY]

    drawSquare(foodX,foodY)
    return (foodX,foodY)

#this is where the game is ran
def gameLoop():
    mode = "Paused"

    playing = True
    screen.fill(BLACK)
    food_location = [0,0]

    oldDiff = 0

    #creating start button 
    startText = smallFont.render("Start",True,WHITE)
    startRect = startText.get_rect()
    startRect.center = ((240+(200/2), (100+(75/2))))
    gameDisplay.blit(startText,startRect)
        
    game_over= False
    player = Snake()                                #player snake
    score = player.size - 1                         #score starts at 0 
    playerScore = "Score %d" % score
    scoreText = smallFont.render(playerScore,True,RED) 
    highscore = 0

    while playing:
        mouse = pygame.mouse.get_pos()
        diff =  pygame.time.get_ticks()


        if mode != "playing" and mode != "standBy":

            if((mouse[0] > 310 and mouse[0] < (310+55)) and (mouse[1] > 125 and mouse[1] < (100+50))):
                startText = smallFont.render('Start',True,YELLOW)
            else:
                startText = smallFont.render("Start",True,WHITE)

            
            gameDisplay.blit(startText,startRect)   #updates the screen

        pygame.display.flip()                       #updates the screen
        

        if(player.pos[0][0] == food_location[0] and player.pos[0][1] == food_location[1]): #if player lands on food
            

            player.size+=1
            playerScore = "Score %d" % (player.size -1)         #updates text with new score
            
            pygame.draw.rect(gameDisplay, BLACK,(600,0,90,20)) #draws black rectangle to erase previous score
            scoreText = smallFont.render(playerScore,True,RED) #changes new score text
            gameDisplay.blit(scoreText,[600,0])                 #updates screen with new text
            player.draw_fullSnake()                             #redraws snake incase part of body is inside the score black rectangle

            food_location = randSquare(player.pos)              #new food location is setup


        for event in pygame.event.get():

            if event.type == pygame.QUIT:
               
                playing = False
            
            #if mouse button clicked
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                #if the mouse button was clicked ontop of start text, spawns the snake
                if((event.button == 1) and (event.pos[0] > 310 and event.pos[0] < 310+55) and (event.pos[1] > 125 and event.pos[1] < 100+50) and (mode != "playing")):
                    
                    scoreText = smallFont.render(playerScore,True,BLACK)    #removes old text
                    gameDisplay.blit(scoreText,[600,0])

                    playerScore = "Score 0"                                 #updates text with new score
                    
                    scoreText = smallFont.render(playerScore,True,RED)      #displays new text
                    gameDisplay.blit(scoreText,[600,0])
                    
                    
                    #sets/resets the screen and snake properties
                    mode = "standBy"
                    game_over= False
                    screen.fill(BLACK)                                      #clears screen
                    player.spawn_snake()                                    #draws snake on screen

                    food_location = randSquare(player.pos)                  #starts off new food location  
                    gameDisplay.blit(scoreText,[600,0])                     #resets score
                    pygame.display.flip()                                   #updates screen

            #if a key is pressed goes into this if
            elif(event.type == pygame.KEYDOWN):
                
                #this moves the snake anytime a button is pressed
                if(mode == "playing"): 
                    if(event.key == pygame.K_LEFT):
                        player.direction = "WEST"
                        game_over= player.moveSnake()
                        oldDiff = diff                                      #resets the timer so it doesn't do a double update for the snakes movement

                    elif(event.key == pygame.K_RIGHT):
                        player.direction = "EAST"
                        game_over= player.moveSnake()
                        oldDiff = diff                                      #resets the timer so it doesn't do a double update for the snakes movement

                    elif(event.key == pygame.K_UP):
                        player.direction = "NORTH"
                        game_over= player.moveSnake()
                        oldDiff = diff                                      #resets the timer so it doesn't do a double update for the snakes movement

                    elif(event.key == pygame.K_DOWN):
                        player.direction = "SOUTH"
                        game_over= player.moveSnake()
                        oldDiff = diff                                      #resets the timer so it doesn't do a double update for the snakes movement
                
                #this is to determine the direction the snake goes on spawn
                elif(mode == "standBy"):
                    if(event.key == pygame.K_LEFT):
                        player.direction = "WEST"

                    elif(event.key == pygame.K_RIGHT):
                        player.direction = "EAST"

                    elif(event.key == pygame.K_UP):
                        player.direction = "NORTH"

                    elif(event.key == pygame.K_DOWN):
                        player.direction = "SOUTH"

                    mode = "playing"
        #if statement to make sure the score text doesn't get overwritten by snake 
        if(player.pos[0][0] >= 37 - player.size and player.pos[0][1] < 2 + player.size):#added player size because if statement only looks at head pos
            scoreText = smallFont.render(playerScore,True,BLACK) 
            gameDisplay.blit(scoreText,[600,0])

            playerScore = "Score %d" % (player.size -1)                                 #updates text with new score
            

            scoreText = smallFont.render(playerScore,True,RED)                          #displays new text
            gameDisplay.blit(scoreText,[600,0])
            pass

        #this is the passive way of moving the snake
        if (diff >= oldDiff+64 and mode == "playing"):                                  #this is the refresh rate of the snake
            oldDiff = diff
            game_over= player.moveSnake()
        
        if game_over== True:
            mode = "dead"                                                               #need to change the mode so the rest of the code doesn't need to run
            
        if(mode == "dead"):
            player.draw_deadSnake()

            #updates highscore 
            if(player.size  - 1> highscore):
                newCaption = "Jake the Snake                                                                                                                          Highscore: %d" % (player.size - 1)
                highscore = player.size - 1
                pygame.display.set_caption(newCaption)
            pass


class Snake:

    def __init__(self):
        self.size = 1
        self.pos = [[21,16]] #coords of the snake's body
        self.direction = "NORTH"
        self.dead = False

    #erases snake (for respawn)
    def del_snake(self):
        for x in self.pos:
            delSquare(x[0],x[1])

    #redraws snake incase snake body overwritten
    def draw_fullSnake(self):
        for x in self.pos:
            drawSquare(x[0],x[1])

    #makes it clear life is over 
    def draw_deadSnake(self):
        for x in self.pos:
            pygame.draw.rect(gameDisplay, RED,(x[0]*16,x[1]*16,15,15))



    #initializes snake
    def spawn_snake(self):
        self.size = 1
        drawSquare(21,16)
        self.pos = [[21,16]]
        self.dead = False
    
    #moves the snake
    def moveSnake(self): 
        
        if self.direction == "NORTH":

            if self.pos[0][1] == 0:
                self.dead = True
                self.pos[0][1] = 0
                newCoord = [0,0]
            else:
                newCoord = [self.pos[0][0],self.pos[0][1] -1]
                if(self.pos.count(newCoord)) >= 1:
                    self.dead = True
                self.pos.insert(0,newCoord)
                
            pass

        elif self.direction == "SOUTH":
            if self.pos[0][1] == GHEIGHT - 1:

                self.dead = True

                self.pos[0][1] = GHEIGHT - 1
                newCoord = [0,0]
            else:
                newCoord = [self.pos[0][0],self.pos[0][1] +1]
                if(self.pos.count(newCoord)) >= 1:
                    self.dead = True
                self.pos.insert(0,newCoord)
                
           

        elif self.direction == "EAST":
            if self.pos[0][0] == GLENGTH - 1: #reached border 
                self.dead = True
                self.pos[0][0] = GLENGTH - 1
                newCoord = [0,0]
                
            else:
                newCoord = [self.pos[0][0] + 1,self.pos[0][1]]
                if(self.pos.count(newCoord)) >= 1:
                    self.dead = True
                self.pos.insert(0,newCoord)
                
                 
            pass

        elif self.direction == "WEST":
            if self.pos[0][0] == 0:
                self.dead = True
                self.pos[0][0] = 0
                newCoord = [0,0]
            else:
                newCoord = [self.pos[0][0] - 1,self.pos[0][1]]
                if(self.pos.count(newCoord)) >= 1:
                    self.dead = True
                self.pos.insert(0,newCoord)
                 
            
        
        self.drawSnake()
        return self.dead
    #player.pos.insert(0,coord)


    #this is meant to update the snake body array and draw it on screen
    def drawSnake(self):
        drawSquare(self.pos[0][0],self.pos[0][1])                       #draws the updated pos of the head of the snake
        lastPos = len(self.pos) -1                                      #determins last snake block in array
        if len(self.pos) > self.size:
            
            delSquare(self.pos[lastPos][0], self.pos[lastPos][1])       #removes last snake block from scrren/array
            deleted = self.pos.pop(lastPos)


        return 
        
#startup menu 
def game_Menu():
    playText = smallFont.render("Play",True,BLACK)

    menu = True
    while menu:
        mouse = pygame.mouse.get_pos()

        screen.fill(BLACK)
        
        #creating title screen
        titleRect = title.get_rect()
        titleRect.center = ((704/2),100)
        gameDisplay.blit(title,titleRect)
        pygame.draw.rect(gameDisplay,YELLOW,(240,200,200,75))
        playRect = playText.get_rect()
        playRect.center = ((240+(200/2), (200+(75/2))))
        gameDisplay.blit(playText,playRect)

        #making play button interactive
        if(mouse[0] > 240 and mouse[0] < 240+200) and (mouse[1] > 200 and mouse[1] < 200+75):
            playText = smallFont.render("Play",True,WHITE)
        else:
            playText = smallFont.render("Play",True,BLACK)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu= False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if(event.button == 1) and (event.pos[0] > 240 and event.pos[0] < 240+200) and (event.pos[1] > 200 and event.pos[1] < 200+75):
                   menu = False
                   gameLoop()
            
game_Menu()