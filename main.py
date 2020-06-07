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



size = (HEIGHT, WIDTH)
gameDisplay = pygame.display.set_mode(size)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("My First Game")
largeFont = pygame.font.Font('freesansbold.ttf',115)
smallFont = pygame.font.Font('freesansbold.ttf',20)
title = largeFont.render("Snake",True,WHITE)
playText = smallFont.render("Play",True,BLACK)



# The loop will carry on until the user exit the game (e.g. clicks the close button).
carryOn = True
 
# The clock will be used to control how fast the screen updates
clock = pygame.time.Clock()


def drawSquare(posX, posY):
    pygame.draw.rect(gameDisplay, WHITE,(posX*16,posY*16,15,15))

def delSquare(posX,posY):
    pygame.draw.rect(gameDisplay, BLACK,(posX*16,posY*16,15,15))

def randSquare():
    pointX = randint(0,43) #had to go 1 less trhan max cuz off screen
    pointY = randint(0,31)
    print(f"x: {pointX} y: {pointY}")
    drawSquare(pointX,pointY)
    return (pointX,pointY)

def gameLoop():
    mode = "Paused"
    #creates a 32x44 map (32 = y, 44 = x)
    map = [[0 for x in range(GLENGTH)] for y in range(GHEIGHT)]
    
    print(f"map: {len(map)}")

    playing = True
    screen.fill(BLACK)

    oldDiff = 0

    startText = smallFont.render("Start",True,WHITE)
    startRect = startText.get_rect()
    startRect.center = ((240+(200/2), (100+(75/2))))
    gameDisplay.blit(startText,startRect)


    #pygame.draw.rect(gameDisplay,WHITE,(100,100,16,16))
    point_location = [0,0]


    player = Snake()
    score = player.size - 1 #cuz size starts at 1
    playerScore = "Score %d" % score
    scoreText = smallFont.render(playerScore,True,RED)
    while playing:
        #updates screen
        mouse = pygame.mouse.get_pos()
        diff =  pygame.time.get_ticks()


        if mode != "playing":

            if((mouse[0] > 310 and mouse[0] < (310+55)) and (mouse[1] > 125 and mouse[1] < (100+50))):
                startText = smallFont.render('Start',True,YELLOW)
            else:
                startText = smallFont.render("Start",True,WHITE)

            
            gameDisplay.blit(startText,startRect)

        pygame.display.flip()
        
        print(f"player: {player.pos[0]} point: {point_location}")

        if(player.pos[0][0] == point_location[0] and player.pos[0][1] == point_location[1]): #if player lands on point
            point_location = randSquare() #new point location is setup
            player.add_square()
            #player.size += 1
            
            scoreText = smallFont.render(playerScore,True,BLACK) #removes old text
            gameDisplay.blit(scoreText,[600,0])

            playerScore = "Score %d" % (player.size -1) #updates text with new score
            

            scoreText = smallFont.render(playerScore,True,RED) #displays new text
            gameDisplay.blit(scoreText,[600,0])

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                playing = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if((event.button == 1) and (event.pos[0] > 310 and event.pos[0] < 310+55) and (event.pos[1] > 125 and event.pos[1] < 100+50) and (mode != "playing")):
                    print(f"Calling game loop... {mode}")
                   
                    player.spawn_snake()
                    mode = "playing"
                    screen.fill(BLACK)
                    point_location = randSquare()
                    gameDisplay.blit(scoreText,[600,0])
                    pygame.display.flip()

                   #calls the actual game play
            elif(event.type == pygame.KEYDOWN):
                if(event.key == pygame.K_LEFT):
                    player.direction = "WEST"
                elif(event.key == pygame.K_RIGHT):
                    player.direction = "EAST"
                elif(event.key == pygame.K_UP):
                    player.direction = "NORTH"
                elif(event.key == pygame.K_DOWN):
                    player.direction = "SOUTH"
        
        if (diff >= oldDiff+60 and mode == "playing"): #this is the refresh rate
            oldDiff = diff
            player.moveSnake()
            #print(f"ticks: {diff}")
    
    clock.tick(60)


#how should i do this snake game? make it a board and seperate it into blocks? 
#i could use hardcoded values but I think that'd be harder when it comes to the previous block trail
class Snake:

    def __init__(self):
        self.size = 1
        self.speed = 1 #might not include speed
        self.pos = [[21,16]] #coords of the snake's head
        self.direction = "NORTH"


    def add_square(self):
        newCoords = [self.pos[self.size-1][0] - 1, self.pos[self.size-1][1] - 1] #finding position of new square
        print(f"ADDED: {self.pos}")
        self.pos.append(newCoords) #adding it to the list of square positions
        drawSquare(newCoords[0],newCoords[1]) #drawing it on screen
        self.size += 1 #incrementing score/size
        pass


    def spawn_snake(self):
        drawSquare(21,16)
        #drawSquare(22,16)
        #drawSquare(23,16)
    
    def moveSnake(self): #make a for loop that goes through the list of positions and updates all of them depending on direction
        if self.direction == "NORTH":
            delSquare(self.pos[self.size-1][0],self.pos[self.size-1][1]) #delsquare removes the last square on the snake
            if self.pos[0][1] == 0: #reached border
                self.pos[0][1] = 0
            else:
                self.pos[0][1] = self.pos[0][1] - 1
            drawSquare(self.pos[0][0],self.pos[0][1])

        elif self.direction == "SOUTH":
            delSquare(self.pos[self.size-1][0],self.pos[self.size-1][1])
            if self.pos[0][1] == GHEIGHT - 1: #reached border
                self.pos[0][1] = GHEIGHT - 1
            else:
                self.pos[0][1] = self.pos[0][1] + 1
            drawSquare(self.pos[0][0],self.pos[0][1])

        elif self.direction == "EAST":
            delSquare(self.pos[self.size-1][0],self.pos[self.size-1][1]) #can proll move this to the else
            if self.pos[0][0] == GLENGTH - 1:
                self.pos[0][0] = GLENGTH - 1
            else:
                self.pos[0][0] = self.pos[0][0] + 1
            drawSquare(self.pos[0][0],self.pos[0][1])

        elif self.direction == "WEST":
            delSquare(self.pos[self.size-1][0],self.pos[self.size-1][1])
            if self.pos[0][0] == 0:
                self.pos[0][0] = 0
            else:
                self.pos[0][0] = self.pos[0][0] - 1
            drawSquare(self.pos[0][0],self.pos[0][1])
        
        pass

def game_Menu():
    playText = smallFont.render("Play",True,BLACK)

    menu = True
    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu= False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if(event.button == 1) and (event.pos[0] > 240 and event.pos[0] < 240+200) and (event.pos[1] > 200 and event.pos[1] < 200+75):
                   print("Calling game loop2...")
                   menu = False
                   gameLoop()
                   
                
        #had to add this part cuz after the loop switched it'd default back to this screen before finally closing
        if menu == True:

            mouse = pygame.mouse.get_pos()

            screen.fill(BLACK)
            #this is my putting title and play button on menu screen
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

            # --- Go ahead and update the screen with what we've drawn.
            pygame.display.flip()
            
            # --- Limit to 60 frames per second
            clock.tick(60)
game_Menu()

print("QUOT")
pygame.quit()


