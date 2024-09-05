import pygame
from pygame.locals import *
import random as rd
from math import *

class Game:
    
    def __init__(self, generation, enfant) -> None:

        self.generation = generation
        self.enfant = enfant
        self.size = (1000,300)
        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("ML_GAME") 
        pygame.display.set_allow_screensaver(True)
        self.clock = pygame.time.Clock()
        self.speed = 100 # Plus la vitesse est faible plus l'affichage est lent 

        self.enemis_pos = [rd.randint(301, 600),250]
        self.player_pos = [rd.randint(0, 249), 250]

        self.IA = ML()   
        self.IA.update_neron_ML(0.00001)

        self.Loop()

    def Loop(self):
        for g in range(self.generation):
            for e in range(self.enfant):
                move_y = 0
                self.enemis_pos = [[rd.randint(0, 250),rd.randint(300,600)][rd.randint(0,1)],250]
                self.player_pos = [250, 250]
                score = 0
                move_y = 0
                move_enemis = 1
                jump = False
                count = 0
                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            break
                    if self.enemis_pos[0] > 1000:
                        self.enemis_pos[0] = -50
                    self.enemis_pos[0] += move_enemis
                    self.get_info()
                    move_enemis += 0.0005
                    move_x, jump_activate = self.IA.calcul(self.player_pos[0], self.player_pos[1], self.enemis_pos[0], self.enemis_pos[1], move_enemis)
                    self.player_pos[0] += move_x
                    if count%self.speed == 0:
                        self.Draw()
                    if self.player_pos[0] > 550:
                        self.player_pos[0] = 550
                    elif self.player_pos[0] < 0:
                        self.player_pos[0] = 0
                    if jump == False and jump_activate == True:
                        move_y = -5
                        jump = True
                    if jump == True:
                        move_y += 0.1
                        if self.player[1] > 250:
                            move_y = 0
                            jump = False
                            self.player_pos[1] = 250
                    self.player_pos[1] += move_y
                    rect_player = pygame.Rect(self.player_pos[0],self.player_pos[1] , 50, 50)
                    rect_enemis = pygame.Rect(self.enemis_pos[0],self.enemis_pos[1] , 50, 50)
                    if rect_player.colliderect(rect_enemis):
                        break
                    score += 1
                    count += 1
                self.IA.if_best(score)
                self.IA.update_neron_ML(0.00001)
                print(g, score)
        print(self.IA.score_best)



    def get_info(self):
        self.distance_x = self.enemis_pos[0]-self.player_pos[0]
        self.distance_y = self.enemis_pos[1]-self.player_pos[1]


    def Draw(self):
        self.screen.fill((0,0,0))
        self.enemis = pygame.draw.rect(self.screen, (255,0,0), (self.enemis_pos[0],self.enemis_pos[1] , 50, 50))
        self.player = pygame.draw.rect(self.screen, (0,255,0), (self.player_pos[0],self.player_pos[1], 50, 50))
        self.IA.draw_ML(pygame, self.screen, self.size)
        pygame.display.update()
        self.clock.tick(1000)

class ML:

    def __init__(self):
        self.score_best = 0
        self.connection = {}
        self.neron_couche = [5,3,2]
        for couche in range(len(self.neron_couche)-1):
            for enter in range(self.neron_couche[couche]):
                for output in range(self.neron_couche[couche+1]):
                    self.connection[str(couche)+str(enter)+str(output)] = 0

        self.best_connection_global = dict(self.connection)

        print(self.connection)

    def calcul(self, pos_x_player, pos_y_player, pos_x_enemie, pos_y_enemie, move_enemis):
        self.neron_value = {}
        self.neron_value["00"] = pos_x_player
        self.neron_value["10"] = pos_y_player
        self.neron_value["20"] = pos_x_enemie
        self.neron_value["30"] = pos_y_enemie
        self.neron_value["40"] = move_enemis
        self.neron_max = 0
        self.neron_min = 0

        for enter in range(self.neron_couche[0]):
            if self.neron_value[str(enter)+str(0)] > self.neron_max:
                self.neron_max = self.neron_value[str(enter)+str(0)]
            elif self.neron_value[str(enter)+str(0)] < self.neron_min:
                self.neron_min = self.neron_value[str(enter)+str(0)]

        for couche in range(len(self.neron_couche)-1):
            for output in range(self.neron_couche[couche+1]):
                self.neron_value[str(output)+str(couche+1)] = 0
                for enter in range(self.neron_couche[couche]):
                    self.neron_value[str(output)+str(couche+1)] += self.neron_value[str(enter)+str(couche)]*self.connection[str(couche)+str(enter)+str(output)]
                if self.neron_value[str(output)+str(couche+1)] > self.neron_max:
                    self.neron_max = self.neron_value[str(output)+str(couche+1)]
                elif self.neron_value[str(output)+str(couche+1)] < self.neron_min:
                    self.neron_min = self.neron_value[str(output)+str(couche+1)]

        move = 5 if self.neron_value["0"+str(len(self.neron_couche)-1)] > 0 else -5
        activate_jump = True if self.neron_value["1"+str(len(self.neron_couche)-1)] > 0 else False

        return move, activate_jump

    def update_neron_ML(self,pas):
        self.connection = dict(self.best_connection_global)
        self.connection_min = 0
        self.connection_max = 0
        for couche in range(len(self.neron_couche)-1):
            for enter in range(self.neron_couche[couche]):
                for output in range(self.neron_couche[couche+1]):
                    self.connection[str(couche)+str(enter)+str(output)] += pas*(rd.random()*2-1)
                    if self.connection[str(couche)+str(enter)+str(output)] > self.connection_max:
                        self.connection_max = self.connection[str(couche)+str(enter)+str(output)]
                    elif self.connection[str(couche)+str(enter)+str(output)] < self.connection_min:
                        self.connection_min = self.connection[str(couche)+str(enter)+str(output)]
        

    def if_best(self, score = 0, global_best = False):
        if score > self.score_best:
            self.best_connection_local = dict(self.connection)
            self.score_best = int(score)
        if global_best:
            self.best_connection_global = dict(self.best_connection_local)
    
    def draw_ML(self, pygame, screen, size):
        for couche in range(len(self.neron_couche)-1):
            for neron in range(self.neron_couche[couche]):
                pos_x = (size[0])/(len(self.neron_couche)+1)*(couche+1)
                pos_y = (size[1])/(self.neron_couche[couche]+1)*(neron+1)
                for neron_next in range(self.neron_couche[couche+1]):
                    connection_norm = (self.connection[str(couche)+str(neron)+str(neron_next)]-self.connection_min)/(self.connection_max-self.connection_min)
                    color = (connection_norm*255,0,0)
                    pos_x_next = (size[0])/(len(self.neron_couche)+1)*(couche+2)
                    pos_y_next = (size[1])/(self.neron_couche[couche+1]+1)*(neron_next+1)
                    pygame.draw.line(screen, color, (pos_x,pos_y), (pos_x_next,pos_y_next)) 
                neron_norm = (self.neron_value[str(neron)+str(couche)]-self.neron_min)/(self.neron_max-self.neron_min)
                color = (neron_norm*255,255,0)
                pygame.draw.circle(screen,color,(pos_x,pos_y), 5)
        for neron in range(self.neron_couche[-1]):
            neron_norm = (self.neron_value[str(neron)+str(couche)]-self.neron_min)/(self.neron_max-self.neron_min)
            color = (neron_norm*255,255,0)
            pos_y = (size[1])/(self.neron_couche[couche+1]+1)*(neron+1)
            pygame.draw.circle(screen,color,(pos_x_next,pos_y), 5)



game = Game(200,20)