import pygame

class load_textures:

    file = 'game_1/sprite/terrain.png'

    def __init__(self, file, size=(31, 31), margin=1, spacing=1):
        self.file = file
        self.size = size
        self.margin = margin
        self.spacing = spacing
        self.image = pygame.image.load(file).convert_alpha()
        self.rect = self.image.get_rect()
        self.tiles = []
        self.load()

    def load(self):

        x0 = y0 = self.margin
        w, h = self.rect.size
        dx = self.size[0] + self.spacing
        dy = self.size[1] + self.spacing

        for y in range(x0, w, dx):
            for x in range(y0, h, dy):
                tile = pygame.Surface(self.size).convert_alpha()
                tile.blit(self.image, (0, 0), (x, y, *self.size))
                self.tiles.append(tile)

    def name(self):
        self.tree_1 = [30,31,62,63,94,95,126,127,158,159]
        self.tree_2 = [504,505,506,536,537,538,

    def __str__(self):
        return f'{self.__class__.__name__} file:{self.file} tile:{self.size}


