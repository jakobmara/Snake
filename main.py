import pygame
from random import randint
pygame.init()

BLACK = (0,0,0)
WHITE=(255,255,255)
GREEN = (0,255,0)
YELLOW = (255,255,0)


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
    pointX = randint(0,44)
    pointY = randint(0,32)
    print(f"x: {pointX} y: {pointY}")
    drawSquare(5,5)
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


    player = Snake()
    while playing:
        point_location = [0,0]
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
        
       
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if((event.button == 1) and (event.pos[0] > 310 and event.pos[0] < 310+55) and (event.pos[1] > 125 and event.pos[1] < 100+50) and (mode != "playing")):
                    print(f"Calling game loop... {mode}")
                   
                    player.spawn_snake()
                    point_location = randSquare()
                    mode = "playing"
                    screen.fill(BLACK)

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
        if (diff >= oldDiff+60 and mode == "playing"):
            oldDiff = diff
            player.moveSnake()
            #print(f"ticks: {diff}")
        if(player.pos[0] == point_location):
            print("POINT!!")
        clock.tick(60)


#how should i do this snake game? make it a board and seperate it into blocks? 
#i could use hardcoded values but I think that'd be harder when it comes to the previous block trail
class Snake:

    def __init__(self):
        self.size = 3
        self.speed = 1 #might not include speed
        self.pos = [[21,16]] #coords of the snake's head
        self.direction = "NORTH"


    def add_square(self):
        self.size += 1

    def spawn_snake(self):
        drawSquare(21,16)
        #drawSquare(22,16)
        #drawSquare(23,16)
    
    def moveSnake(self):
        if self.direction == "NORTH":
            delSquare(self.pos[0][0],self.pos[0][1])
            self.pos[0][1] = self.pos[0][1] - 1
            drawSquare(self.pos[0][0],self.pos[0][1])

        elif self.direction == "SOUTH":
            delSquare(self.pos[0][0],self.pos[0][1])
            self.pos[0][1] = self.pos[0][1] + 1
            drawSquare(self.pos[0][0],self.pos[0][1])

        elif self.direction == "EAST":
            delSquare(self.pos[0][0],self.pos[0][1])
            self.pos[0][0] = self.pos[0][0] + 1
            drawSquare(self.pos[0][0],self.pos[0][1])

        elif self.direction == "WEST":
            delSquare(self.pos[0][0],self.pos[0][1])
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


