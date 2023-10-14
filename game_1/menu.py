import pygame
from pygame.locals import *
import numpy as np

class menu(object):

    def __init__(self, rect):

        self.menu = np.load('game_1/save/menu.npy')
        self.font = pygame.font.SysFont(None, 100)
        self.clock = pygame.time.Clock()
        self.items()
        self.loop()

    def loop(self):
        while True:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    return False
                elif event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()

                elif event.type == pygame.KEYDOWN and input_active:
                    if event.key == pygame.K_RETURN:
                        input_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        text =  text[:-1]
                    else:
                        text += event.unicode

    def render(self):
        pass

    def search(self, key):
        Find = []
        for item in self.Items.keys():
            if key in item:
                Find.append(self.Items[item])
        return Find

    def items(self):
        self.Items = {
        "grass_1" : (181,181),
        "grass_2" : (182,182),
        "grass_3" : (183,183),
        "grass_4" : (118,118),
        "grass_border_up_left_ext" : (85,85),
        "grass_border_up_left_int" : (22,22),
        "grass_border_up" : (86,86),
        "grass_border_up_right_ext" : (87,87),
        "grass_border_up_right_int" : (23,23),
        "grass_border_down_left_ext" : (149,149),
        "grass_border_down_left_int" : (54,54),
        "grass_border_down" : (150,150),
        "grass_border_down_right_ext" : (151,151),
        "grass_border_down_right_int" : (55,55),
        "tree_1" : (30, 159),
        "tree_2" : (504,570),
        "tree_3" : (507,605)
        }

