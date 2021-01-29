import pygame
from snake import Snake
from random import randint
pygame.init()

LARGEFONT = pygame.font.Font('freesansbold.ttf',115)
SMALLFONT = pygame.font.Font('freesansbold.ttf',20)

BLACK = (0,0,0)
WHITE=(255,255,255)
GREEN = (0,255,0)
YELLOW = (255,255,0)
RED = (255,0,0)

# Window size dimensions
HEIGHT = 704
WIDTH = 512

# Game grid dimensions
GLENGTH = 44 
GHEIGHT = 32



class Board():

    def __init__(self,display,screen,refreshRate):
        self.board = display
        self.screen = screen 
        self.player = Snake()
        self.refreshRate = refreshRate


    def drawSquare(self, posX, posY, color = WHITE):
        pygame.draw.rect(gameDisplay, color,(posX*16,posY*16,15,15))



    def delSquare(self, posX,posY):
        pygame.draw.rect(gameDisplay, BLACK,(posX*16,posY*16,15,15))

    def del_snake(self,playerCoords):
        for x in playerCoords:
            self.delSquare(x[0],x[1])
    
    #makes it clear life is over 
    def draw_deadSnake(self,playerCoords):
        for x in playerCoords:
            self.drawSquare(x[0],x[1],RED)
            #pygame.draw.rect(gameDisplay, RED,(x[0]*16,x[1]*16,15,15))

    #redraws snake incase snake body overwritten
    def draw_fullSnake(self,playerCoords):
        for x in playerCoords:
            self.drawSquare(x[0],x[1])

    

    #this is meant to update the snake body array and draw it on screen
    def drawSnake(self):
        self.drawSquare(self.player.pos[0][0],self.player.pos[0][1])                       #draws the updated pos of the head of the snake
        lastPos = len(self.player.pos) -1                                      #determins last snake block in array
        if len(self.player.pos) > self.player.size:
            
            self.delSquare(self.player.pos[lastPos][0], self.player.pos[lastPos][1])       #removes last snake block from scrren/array
            self.player.pos.pop(lastPos)


    #determine/draw new food position
    def randSquare(self, body):
        foodX = randint(0,43) #had to go 1 less trhan max cuz off screen
        foodY = randint(0,31)
        foodLoc = [foodX,foodY]
        #this loop is so that the new food location doesn't spawn within the snake body
        while(body.count(foodLoc) >= 1):
            foodX = randint(0,43) #had to go 1 less trhan max cuz off screen
            foodY = randint(0,31)
            foodLoc = [foodX,foodY]

        self.drawSquare(foodX,foodY)
        return (foodX,foodY)

    #initializes snake this is used when a player respawns could potentially change this so when a player dies snake settings default back to this
    def spawn_snake(self):
        self.player.size = 1
        self.drawSquare(21,16)
        self.player.pos = [[21,16]]
        self.player.dead = False

    #this is where the game is ran
    def gameLoop(self):
        mode = "Paused"

        playing = True
        self.screen.fill(BLACK)
        food_location = [0,0]

        oldDiff = 0

        #creating start button 
        startText = SMALLFONT.render("Start",True,WHITE)
        startRect = startText.get_rect()
        startRect.center = ((240+(200/2), (100+(75/2))))
        gameDisplay.blit(startText,startRect)
            
        game_over= False
        score = self.player.size - 1                         #score starts at 0 
        playerScore = "Score %d" % score
        scoreText = SMALLFONT.render(playerScore,True,RED) 
        highscore = 0

        while playing:
            mouse = pygame.mouse.get_pos()
            diff =  pygame.time.get_ticks()


            if mode != "playing" and mode != "standBy":

                if((mouse[0] > 310 and mouse[0] < (310+55)) and (mouse[1] > 125 and mouse[1] < (100+50))):
                    startText = SMALLFONT.render('Start',True,YELLOW)
                else:
                    startText = SMALLFONT.render("Start",True,WHITE)

                
                gameDisplay.blit(startText,startRect)   #updates the screen

            pygame.display.flip()                       #updates the screen
            

            if(self.player.pos[0][0] == food_location[0] and self.player.pos[0][1] == food_location[1]): #if player lands on food
                

                self.player.size+=1
                playerScore = "Score %d" % (self.player.size -1)         #updates text with new score
                
                pygame.draw.rect(gameDisplay, BLACK,(600,0,90,20)) #draws black rectangle to erase previous score
                scoreText = SMALLFONT.render(playerScore,True,RED) #changes new score text
                gameDisplay.blit(scoreText,[600,0])                 #updates screen with new text
                self.draw_fullSnake(self.player.pos)                             #redraws snake incase part of body is inside the score black rectangle

                food_location = self.randSquare(self.player.pos)              #new food location is setup


            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                
                    playing = False
                
                #if mouse button clicked
                if event.type == pygame.MOUSEBUTTONDOWN:
                    
                    #if the mouse button was clicked ontop of start text, spawns the snake
                    if((event.button == 1) and (event.pos[0] > 310 and event.pos[0] < 310+55) and (event.pos[1] > 125 and event.pos[1] < 100+50) and (mode != "playing")):
                        
                        scoreText = SMALLFONT.render(playerScore,True,BLACK)    #removes old text
                        gameDisplay.blit(scoreText,[600,0])

                        playerScore = "Score 0"                                 #updates text with new score
                        
                        scoreText = SMALLFONT.render(playerScore,True,RED)      #displays new text
                        gameDisplay.blit(scoreText,[600,0])
                        
                        
                        #sets/resets the screen and snake properties
                        mode = "standBy"
                        game_over= False
                        self.screen.fill(BLACK)                                      #clears screen
                        self.spawn_snake()                                          #draws snake on screen

                        food_location = self.randSquare(self.player.pos)                  #starts off new food location  
                        gameDisplay.blit(scoreText,[600,0])                     #resets score
                        pygame.display.flip()                                   #updates screen

                #if a key is pressed goes into this if
                elif(event.type == pygame.KEYDOWN):
                    
                    #this moves the snake anytime a button is pressed
                    if(mode == "playing"): 
                        if(event.key == pygame.K_LEFT):
                            self.player.direction = "WEST"
                            game_over= self.player.moveSnake()
                            oldDiff = diff                                      #resets the timer so it doesn't do a double update for the snakes movement

                        elif(event.key == pygame.K_RIGHT):
                            self.player.direction = "EAST"
                            game_over= self.player.moveSnake()
                            oldDiff = diff                                      #resets the timer so it doesn't do a double update for the snakes movement

                        elif(event.key == pygame.K_UP):
                            self.player.direction = "NORTH"
                            game_over= self.player.moveSnake()
                            oldDiff = diff                                      #resets the timer so it doesn't do a double update for the snakes movement

                        elif(event.key == pygame.K_DOWN):
                            self.player.direction = "SOUTH"
                            game_over= self.player.moveSnake()
                            oldDiff = diff                                      #resets the timer so it doesn't do a double update for the snakes movement
                    
                    #this is to determine the direction the snake goes on spawn
                    elif(mode == "standBy"):
                        if(event.key == pygame.K_LEFT):
                            self.player.direction = "WEST"

                        elif(event.key == pygame.K_RIGHT):
                            self.player.direction = "EAST"

                        elif(event.key == pygame.K_UP):
                            self.player.direction = "NORTH"

                        elif(event.key == pygame.K_DOWN):
                            self.player.direction = "SOUTH"

                        mode = "playing"
            #if statement to make sure the score text doesn't get overwritten by snake 
            if(self.player.pos[0][0] >= 37 - self.player.size and self.player.pos[0][1] < 2 + self.player.size):#added player size because if statement only looks at head pos
                scoreText = SMALLFONT.render(playerScore,True,BLACK) 
                gameDisplay.blit(scoreText,[600,0])

                playerScore = "Score %d" % (self.player.size -1)                                 #updates text with new score
                

                scoreText = SMALLFONT.render(playerScore,True,RED)                          #displays new text
                gameDisplay.blit(scoreText,[600,0])
                pass

            #this is the passive way of moving the snake
            if (diff >= oldDiff+ self.refreshRate and mode == "playing"):                                  #this is the refresh rate of the snake
                oldDiff = diff
                game_over= self.player.moveSnake()
            
            if game_over== True:
                mode = "dead"                                                               #need to change the mode so the rest of the code doesn't need to run
                
                self.draw_deadSnake(self.player.pos)

                #updates highscore 
                if(self.player.size  - 1> highscore):
                    newCaption = "Jake the Snake                                                                                                                          Highscore: %d" % (self.player.size - 1)
                    highscore = self.player.size - 1
                    pygame.display.set_caption(newCaption)
                pass
            else:
                self.drawSnake()


    
            
    #startup menu 
    def game_Menu(self):
        playText = SMALLFONT.render("Play",True,BLACK)

        menu = True
        while menu:
            mouse = pygame.mouse.get_pos()

            self.screen.fill(BLACK)
            
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
                playText = SMALLFONT.render("Play",True,WHITE)
            else:
                playText = SMALLFONT.render("Play",True,BLACK)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    menu= False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if(event.button == 1) and (event.pos[0] > 240 and event.pos[0] < 240+200) and (event.pos[1] > 200 and event.pos[1] < 200+75):
                        menu = False
                        self.gameLoop()

if __name__ == "__main__":
    
    title = LARGEFONT.render("Snake",True,WHITE)
    playText = SMALLFONT.render("Play",True,BLACK)
    
    difficulties = {"1":60, "2":44, "3":30}

    difficulty = input("Welcome to snake! Please enter 1, 2, or 3 to set the difficulty you would like to play at (1 is easiest 2 is reccomended): ")

    size = (HEIGHT, WIDTH)
    gameDisplay = pygame.display.set_mode(size)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Jake the Snake                                                                                                                          Highscore: 0")

    game = Board(gameDisplay,screen,difficulties[difficulty])
    game.game_Menu()