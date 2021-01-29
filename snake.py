
GLENGTH = 44
GHEIGHT = 32
class Snake:

    def __init__(self):
        self.size = 1
        self.pos = [[21,16]] #coords of the snake's body
        self.direction = "NORTH"
        self.dead = False

    

    
    
    #moves the snake
    # can modify this so that it just takes a direction as an input
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
                 
            
        
        #self.drawSnake()
        return self.dead
    #player.pos.insert(0,coord)
