import pygame
from pygame.locals import *
import random as rd
import MOB
import SETTING

class Game:

    def __init__(self):

        pygame.init()

        self.screen = pygame.display.set_mode(SETTING.SCREEN_SIZE)

        pygame.display.set_caption("ML_GAME")
        pygame.display.set_allow_screensaver(True)

        self.clock = pygame.time.Clock()

        self.entity = Entity()
        self.entity.player()
        for x in range(2):
            self.entity.ennemie()
        self.entity.coin()
        self.entity.weapon()
        self.entity.bullet()

        self.loop()

    def reset(self):

        del self.entity 
        self.entity = Entity()
        self.entity.player()
        self.entity.ennemie()
        self.entity.coin()

    def loop(self):
        
        while True:
            self.key()
            self.entity.update()
            self.entity.collidrect()
            self.draw()
    
    def key(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.entity.entities[1].move[1] -= 0.2 if self.entity.entities[1].move[1] > -4 else 0
        if keys[pygame.K_DOWN]:
            self.entity.entities[1].move[1] += 0.2 if self.entity.entities[1].move[1] < 4 else 0
        if keys[pygame.K_RIGHT]:
            self.entity.entities[1].move[0] += 0.2 if self.entity.entities[1].move[0] < 4 else 0
        if keys[pygame.K_LEFT]:
            self.entity.entities[1].move[0] -= 0.2 if self.entity.entities[1].move[0] > -4 else 0
    
    def draw(self):

        self.screen.fill((0,0,0))
        self.entity.draw(self.screen)
        #IA[0].Draw_ML(pygame, self.screen,(0,0), (self.size[0],self.size[1]))
        pygame.display.update()
        self.clock.tick_busy_loop(60)

class Entity:

    # ID_TYPE : Mob, Item, Particle

    def __init__(self):

        self.id = 0x0 # id d'initialisation
        self.entities = {} # initialisation dictionaire des entitées

    def player(self):

        self.id = self.id + 0x1
        self.entities[self.id] = MOB.Player(self.id) # Add new entity Player

    def ennemie(self):

        self.id = self.id + 0x1
        self.entities[self.id] = MOB.Ennemie(self.id) # Add new entity Ennemie

    def coin(self):

        self.id = self.id + 0x1
        self.entities[self.id] = MOB.Coin(self.id) # Add new entity Coin

    def weapon(self):

        self.id = self.id + 0x1
        self.entities[self.id] = MOB.Weapon(self.id) # Add new entity Coin

    def bullet(self):

        self.id = self.id + 0x1
        self.entities[self.id] = MOB.Bullet(self.id) # Add new entity Coin

    def update(self):

        Del = [] # Dictionnaire des entité suprimé

        for entity in self.entities.values():
            if not entity.update(): # Update entity
                Del.append(entity.id) # Add death entity to Del list

        for id in Del:
            del self.entities[id] # Supression entité 

    def collidrect(self):

        for entity_1 in self.entities.values():
            for entity_2 in self.entities.values():
                if entity_1.rect.colliderect(entity_2.rect):
                    collide_action(entity_1, entity_2)

    def draw(self, screen):

        for entity in self.entities.values():

            entity.draw(screen)

def collide_action(entity_1, entity_2):
    
    ID_TYPE_1 = entity_1.ID_TYPE
    ID_TYPE_2 = entity_2.ID_TYPE

    ID_NUMBER_1 = entity_1.ID_NUMBER
    ID_NUMBER_2 = entity_2.ID_NUMBER

    # MOB Collide MOB
    if ID_TYPE_1 == 0x0 and ID_TYPE_2 == 0x0 :
        # Ennemie Collide Player
        if ID_NUMBER_1 == 0x1 and ID_NUMBER_2 == 0x0 :
            # Player Lose Life
            entity_2.health -= entity_1.DOMMAGE
            # Player Lose Score
            entity_2.score -= 1
        
    # MOB Collide ITEM
    if ID_TYPE_1 == 0x0 and ID_TYPE_2 == 0x1 :
        # Player Collide Coin
        if ID_NUMBER_1 == 0x0 and ID_NUMBER_2 == 0x0 :
            # Coin Lose Life
            entity_2.health -= 1
            # Player Earn Score 
            entity_1.score += entity_2.VALUE
        # Player Collide Weapon
        if ID_NUMBER_1 == 0x0 and ID_NUMBER_2 == 0x1 :
            # Player Earn Weapon
            entity_1.inventory.add(entity_2)
            entity_2.in_inventory = True


g = Game()
