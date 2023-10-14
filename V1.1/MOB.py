import pygame
import random as rd
import SETTING
import ML

GRAVITY = 0.1

RED = 1
GREEN = 2
BLEU = 3
WHITE = 4
BLACK = 5
GREY = 6
YELLOW = 7

COLOR = {
            RED : (255,0,0),
            GREEN : (0,255,0),
            BLEU : (0,0,255),
            WHITE : (255,255, 255),
            BLACK : (255,255,255),
            GREY : (90,90,90),
            YELLOW : (255,255,0)
     }

# Type Mob
# Number Mob : Player, Ennemie
 
class Player:

    # Player ID
    ID_TYPE = 0x0
    ID_NUMBER = 0x0
    ID_NAME = "Player"

    # Player Setting
    HEALTH_MAX = 100        # PV maximum
    HEALTH_SPEED = 0.1      # PV regenerate per frame
    DOMMAGE = 2             # DOMMAGE per frame
    SPEED_MAX = 5           # Px per frame

    # Draw Setting:
    MAPWIDTH = 4            # hauteur
    MAPHEIGHT = 3           # longeur
    TILESIZE = 10           # taille px
    SIZE = (MAPHEIGHT * TILESIZE, MAPWIDTH * TILESIZE) # taille de l'image
    FORM = [[0,3,0],
            [4,6,4],
            [4,6,4],
            [6,0,6],]


    def __init__(self, id):

        self.id = id

        self.pos = [rd.randint(0, 249), 250] # Position

        self.move = [0,0] # Vitesse
        self.jump = False
        self.score = 0
        self.health = self.HEALTH_MAX

        self.image = surface(self)

        self.inventory = Inventory(5)

    def update(self):

        self.inventory.update(self)

        self.pos[0] += self.move[0]
        self.pos[1] += self.move[1]

        in_window(self)

        self.health = self.health + self.HEALTH_SPEED if self.health < self.HEALTH_MAX+self.HEALTH_SPEED else self.HEALTH_MAX # régéneration de la vie

        self.rect = pygame.Rect(self.pos[0],self.pos[1] , self.SIZE[0], self.SIZE[1])

        # test si encore en vie
        if self.health <= 0:
            self.health = 0
            return False 
        
        return True # True si entité vivante sinon False
    
    def draw(self, screen):

        screen.blit(self.image, self.pos)

        self.inventory.draw(screen)

class Ennemie:

    # Ennemie ID
    ID_TYPE = 0x0
    ID_NUMBER = 0x1
    ID_NAME = "Ennemie"

    # Ennemie Setting
    HEALTH_MAX = 100    # PV maximum
    HEALTH_SPEED = 0    # PV regenerate per frame
    DOMMAGE = 1         # DOMMAGE per frame
    SPEED_MAX = 4       # PX per frame

    # Draw Setting:
    MAPWIDTH = 4
    MAPHEIGHT = 3
    TILESIZE = 10
    SIZE = (MAPHEIGHT * TILESIZE, MAPWIDTH * TILESIZE)
    FORM = [[0,1,0],
            [4,6,4],
            [4,6,4],
            [6,0,6],]

    def __init__(self, id):

        self.id = id
        self.pos = [rd.randint(0, SETTING.SCREEN_SIZE[0]-self.SIZE[0]),rd.randint(0, SETTING.SCREEN_SIZE[1]-self.SIZE[1])]
        self.move = [1,0]
        self.jump = False
        self.health = self.HEALTH_MAX
        self.score = 0

        self.image = surface(self)

    def update(self):

        self.move[1] += 0.01 

        self.pos[0] += self.move[0]
        self.pos[1] += self.move[1]

        in_window(self)

        self.health = self.health + self.HEALTH_SPEED if self.health < self.HEALTH_MAX+self.HEALTH_SPEED else self.HEALTH_MAX # régéneration de la vie

        self.rect = pygame.Rect(self.pos[0],self.pos[1] , self.SIZE[0], self.SIZE[1])

        if self.health <= 0: 
            self.health = 0
            return False

        return True
    
    def draw(self, screen):

        screen.blit(self.image, self.pos)

# Type Item
# Number Item : Coin
class Coin:

    # Coin ID
    ID_TYPE = 0x1
    ID_NUMBER = 0x0
    ID_NAME = "Coin"

    # Coin Setting
    HEALTH_MAX = 1
    HEALTH_SPEED = 0
    VALUE = 100 

    # Draw Setting:
    MAPWIDTH = 3
    MAPHEIGHT = 3
    TILESIZE = 5
    SIZE = (MAPHEIGHT * TILESIZE, MAPWIDTH * TILESIZE)
    FORM = [[0,7,0],
            [7,7,7],
            [0,7,0]]
    

    def __init__(self, id):

        self.image = surface(self)

        self.id = id
        self.pos = [rd.randint(0, SETTING.SCREEN_SIZE[0] - self.SIZE[0]), rd.randint(0, SETTING.SCREEN_SIZE[1] - self.SIZE[1])]

        self.health = self.HEALTH_MAX
        self.score = 0

    def update(self):

        self.health = self.health + self.HEALTH_SPEED if self.health < self.HEALTH_MAX+self.HEALTH_SPEED else self.HEALTH_MAX # régéneration de la vie

        self.rect = pygame.Rect(self.pos[0],self.pos[1] , self.SIZE[0], self.SIZE[1])

        if self.health <= 0: 
            self.health = 0
            return False

        return True
    
    def draw(self, screen):

        screen.blit(self.image, self.pos)

class Weapon:

    # Weapon ID
    ID_TYPE = 0x1
    ID_NUMBER = 0x1
    ID_NAME = "Weapon"

    # Weapon Setting
    HEALTH_MAX = 100
    HEALTH_SPEED = 0
    VALUE = 300 

    # Draw Setting:
    MAPWIDTH = 2
    MAPHEIGHT = 4
    TILESIZE = 5
    SIZE = (MAPHEIGHT * TILESIZE, MAPWIDTH * TILESIZE)
    FORM = [[6,6,6,6],
            [6,0,0,0]]

    def __init__(self, id):

        self.id = id
        self.pos = [rd.randint(0, SETTING.SCREEN_SIZE[0] - self.SIZE[0]), rd.randint(0, SETTING.SCREEN_SIZE[1] - self.SIZE[1])]
        self.move = [0,0]

        self.in_inventory = False
        self.health = self.HEALTH_MAX
        self.score = 0

        self.image = surface(self)

    def update(self, data=None):

        if not self.in_inventory: # when the weapon are in the floor

            self.health = self.health + self.HEALTH_SPEED if self.health < self.HEALTH_MAX+self.HEALTH_SPEED else self.HEALTH_MAX # régéneration de la vie

            self.pos[0] += self.move[0]
            self.pos[1] += self.move[1]

            in_window(self)

            self.rect = pygame.Rect(self.pos[0],self.pos[1] , self.SIZE[0], self.SIZE[1])

            if self.health <= 0: 
                self.health = 0
                return False

            return True
    
        if self.in_inventory and data != None:

            self.pos = data.pos_hand

            if self.move[0] > 0:
                self.pos[0] += data.SIZE[0]
            if self.move[0] < 0:
                self.pos[0] -= data.SIZE[0]
                self.image = pygame.transform.flip(self.image, True)

            self.rect = pygame.Rect(self.pos[0],self.pos[1] , self.SIZE[0], self.SIZE[1])

            return False 
        

    def draw(self, screen):

        screen.blit(self.image, self.pos)

class Bullet:
    # Bullet ID
    ID_TYPE = 0x1
    ID_NUMBER = 0x2
    ID_NAME = "Bullet"

    # Bullet Setting
    HEALTH_MAX = 10
    HEALTH_SPEED = 0
    VALUE = 25

    # Draw Setting:
    MAPWIDTH = 1
    MAPHEIGHT = 3
    TILESIZE = 3
    SIZE = (MAPHEIGHT * TILESIZE, MAPWIDTH * TILESIZE)
    FORM = [[7,6,5]]

    def __init__(self, id):

        self.id = id
        self.pos = [rd.randint(0, SETTING.SCREEN_SIZE[0] - self.SIZE[0]), rd.randint(0, SETTING.SCREEN_SIZE[1] - self.SIZE[1])]
        self.move = [0,0]

        self.in_inventory = False
        self.health = self.HEALTH_MAX

        self.image = surface(self)

    def update(self, data=None):

        if not self.in_inventory: # when the weapon are in the floor

            self.health = self.health + self.HEALTH_SPEED if self.health < self.HEALTH_MAX+self.HEALTH_SPEED else self.HEALTH_MAX # régéneration de la vie

            self.pos[0] += self.move[0]
            self.pos[1] += self.move[1]

            in_window(self)

            self.rect = pygame.Rect(self.pos[0],self.pos[1] , self.SIZE[0], self.SIZE[1])

            if self.health <= 0: 
                self.health = 0
                return False

            return True
    
        if self.in_inventory and data != None:

            self.pos = data.pos

            self.rect = pygame.Rect(self.pos[0],self.pos[1] , self.SIZE[0], self.SIZE[1])

            return False   

    def draw(self, screen):

        screen.blit(self.image, self.pos)

# Type Particle

# Other Function
def in_window(self):
    # verifie if entity are in windows and move player on the window if is not in.
    self.move[1] += GRAVITY
    if self.pos[0] > SETTING.SCREEN_SIZE[0]:
        self.pos[0] = - self.SIZE[0]
    elif self.pos[0] < -self.SIZE[0]:
        self.pos[0] = SETTING.SCREEN_SIZE[0]
    if self.pos[1] > SETTING.SCREEN_SIZE[1] - self.SIZE[1]:
        self.pos[1] = SETTING.SCREEN_SIZE[1] - self.SIZE[1]
        self.move[1] = 0
    elif self.pos[1] < 0:
        self.pos[1] = 0
        self.move[1] = 0

def surface(self):

    image = pygame.Surface(self.SIZE)
    for row in range(self.MAPWIDTH):
            for column in range(self.MAPHEIGHT):
                if self.FORM[row][column] != 0:
                    pygame.draw.rect(image, COLOR[self.FORM[row][column]], (column*self.TILESIZE, row*self.TILESIZE, self.TILESIZE, self.TILESIZE))

    image = image.convert_alpha()

    return image

class Inventory:

    def __init__(self, inventory_size):

        self.inventory = {x : None for x in range(inventory_size)}
        self.item_use = 0

    def add(self, Object):

        for item in range(len(self.inventory)):
            if self.inventory[item] == None:
                self.inventory[item] = Object
                return True
        
        return False

    def remove(self, Object):
    
        for item in range(len(self.inventory)):
            if self.inventory[item] == Object:
                self.inventory[item] = None
                return True
            
        return False
    
    def update(self, data):

        if self.inventory[self.item_use] != None:
            self.inventory[self.item_use].update(data)
    
    def draw(self, screen):

        if self.inventory[self.item_use] != None:
            self.inventory[self.item_use].draw(screen)