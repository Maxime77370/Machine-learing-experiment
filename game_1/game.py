import pygame
from pygame.locals import *
import numpy as np

class Game:

    def __init__(self):

        pygame.init()
        self.screen = pygame.display.set_mode(pygame.display.get_desktop_sizes()[0],pygame.FULLSCREEN)
        pygame.display.set_caption("Prepa Game")

        self.clock = pygame.time.Clock()

        self.running = True
        self.run()

    def run(self):

        while self.running:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    self.running = False

            self.draw()

    def draw(self):
        self.screen.fill((0,0,0))
        pygame.display.update()
        self.clock.tick(60)


game = Game()