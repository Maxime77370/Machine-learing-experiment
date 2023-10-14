import pygame
import random as rd
import SETTING
import ML
from math import *

GRAVITY = 4 / SETTING.FPS

# Le code ci-dessus définit un dictionnaire appelé COLOR qui mappe les constantes de couleur à leurs
# valeurs RVB correspondantes. Les constantes de couleur sont définies sous forme d'entiers et chaque
# entier est mappé à un tuple de trois entiers représentant les valeurs rouge, verte et bleue de la
# couleur.

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

# La classe Player représente un joueur dans un jeu, avec des attributs tels que la position, la
# santé, l'inventaire et les méthodes de mise à jour et de dessin du joueur.
class Player:

    # La classe Paramètres contient divers paramètres et identifiants pour un joueur, notamment les
    # paramètres de santé, de dégâts, de vitesse et de dessin.
    class Settings:

        # Le code ci-dessus définit diverses constantes et paramètres pour un personnage joueur dans
        # un jeu.
        
        # Identifiants
        ID_TYPE = 0x0
        ID_NUMBER = 0x0
        ID_NAME = "Player"
        # Paramètres
        HEALTH_MAX = 100
        HEALTH_SPEED = 0.1
        DAMAGE = 2
        SPEED_MAX = 5
        # Paramètres de dessin
        MAPWIDTH = 4
        MAPHEIGHT = 3
        TILESIZE = 10
        SIZE = (MAPHEIGHT * TILESIZE, MAPWIDTH * TILESIZE)
        FORM = [[0, 3, 0],
                [4, 6, 4],
                [4, 6, 4],
                [6, 0, 6]]

    def __init__(self, entity_manager):
        """
        Cette fonction initialise les attributs d'une entité joueur.
        
        :param entity_manager: Le paramètre `entity_manager` est une instance d'une classe qui gère les
        entités du jeu. Il est utilisé pour créer d’autres entités et leur attribuer des identifiants
        uniques
        """
        # Liaison au gestionnaire d'entités pour créer d'autres entités
        self.entity_manager = entity_manager

        # Attributs du joueur
        self.id = self.entity_manager.id
        self.pos = [rd.randint(0, 249), 250]
        self.move = [0, 0]
        self.action_1_bool = False
        self.action_2_bool = False
        self.jump = False
        self.score = 0
        self.health = self.Settings.HEALTH_MAX
        self.image = surface(self.Settings)     # Création de l'image
        self.inventory = Inventory(20)           # Création de l'inventaire

    def update(self):
        """
        La fonction met à jour l'inventaire, la position et la santé du joueur, effectue des actions en
        fonction des entrées du joueur, vérifie si le joueur est dans les limites de la fenêtre et
        renvoie True si la santé du joueur est supérieure à 0.
        :return: une valeur booléenne. Si la santé du joueur est inférieure ou égale à 0, il renvoie
        False. Sinon, il renvoie True.
        """
        # Le code ci-dessus met à jour la position d'un objet. Il ajoute la valeur de `self.move[0]` à
        # la coordonnée x (`self.pos[0]`) et la valeur de `self.move[1]` à la coordonnée y (`self.pos
        # [1]`).
        self.pos[0] += self.move[0]
        self.pos[1] += self.move[1]

        # Le code ci-dessus met à jour l'inventaire, puis vérifie si « action_1_bool » est vrai. Si
        # c'est le cas, il récupère l'élément actif de l'inventaire et appelle « action_1 » dessus, en
        # passant « self » comme argument. Il vérifie ensuite si « action_2_bool » est vrai et si
        # c'est le cas, récupère à nouveau l'élément actif et appelle « action_2 » dessus, en passant
        # « self » comme argument.
        self.inventory.update(self)

        if self.action_1_bool: 
            item = self.inventory.get_active_item()
            if item != None:
                item.action_1(self)
        if self.action_2_bool : 
            item = self.inventory.get_active_item()
            if item != None:
                item.action_2(self)

        # Vérification de la position dans la fenêtre
        in_window(self)

        # Régénération de la santé avec un maximum défini
        self.health = min(self.health + self.Settings.HEALTH_SPEED, self.Settings.HEALTH_MAX)

        # Création du rectangle de collision
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.Settings.SIZE[0], self.Settings.SIZE[1])

        # Vérification de la santé pour la survie
        if self.health <= 0:
            self.health = 0
            return False
        
        return True

    def draw(self, screen):
        # Affichage de l'image du joueur et de l'inventaire
        screen.blit(self.image, self.pos)
        self.inventory.draw(screen)

# La classe ci-dessus représente un ennemi dans un jeu avec divers paramètres et attributs.
class Ennemy:

    # La classe Paramètres définit diverses constantes et paramètres pour un personnage ennemi dans un
    # jeu.
    class Settings:
        ID_TYPE = 0x0
        ID_NUMBER = 0x1
        ID_NAME = "Ennemie"
        HEALTH_MAX = 100
        HEALTH_SPEED = 0
        DAMAGE = 1
        SPEED_MAX = 4
        MAPWIDTH = 4
        MAPHEIGHT = 3
        TILESIZE = 10
        SIZE = (MAPHEIGHT * TILESIZE, MAPWIDTH * TILESIZE)
        FORM = [[0, 1, 0],
                [4, 6, 4],
                [4, 6, 4],
                [6, 0, 6]]

    def __init__(self, entity_manager):
        """
        La fonction initialise un objet avec divers attributs et leur attribue des valeurs.
        
        :param entity_manager: Le paramètre `entity_manager` est une instance d'une classe qui gère les
        entités du jeu. Il dispose probablement de méthodes pour créer, mettre à jour et supprimer des
        entités, ainsi que pour suivre leurs identifiants
        """

        self.entity_manager = entity_manager
        self.id = self.entity_manager.id
        self.pos = [rd.randint(0, SETTING.SCREEN_SIZE[0] - self.Settings.SIZE[0]),
                    rd.randint(0, SETTING.SCREEN_SIZE[1] - self.Settings.SIZE[1])]
        self.move = [1, 0]
        self.action_1_bool = False
        self.action_2_bool = False
        self.jump = False
        self.health = self.Settings.HEALTH_MAX
        self.score = 0
        self.image = surface(self.Settings)
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.Settings.SIZE[0], self.Settings.SIZE[1])

        self.inventory = Inventory(5)   

    def update(self, data = None):


        # Le code ci-dessus met à jour la position d'un objet. Il ajoute la valeur de `self.move[0]` à
        # la coordonnée x (`self.pos[0]`) et la valeur de `self.move[1]` à la coordonnée y (`self.pos
        # [1]`).

        self.pos[0] += self.move[0]
        self.pos[1] += self.move[1]

        # Le code ci-dessus met à jour l'inventaire, puis vérifie si « action_1_bool » est vrai. Si
        # c'est le cas, il récupère l'élément actif de l'inventaire et appelle « action_1 » dessus, en
        # passant « self » comme argument. Il vérifie ensuite si « action_2_bool » est vrai et si
        # c'est le cas, récupère à nouveau l'élément actif et appelle « action_2 » dessus, en passant
        # « self » comme argument.
        self.inventory.update(self)

        if self.action_1_bool: 
            item = self.inventory.get_active_item()
            if item != None:
                item.action_1(self)
        if self.action_2_bool : 
            item = self.inventory.get_active_item()
            if item != None:
                item.action_2(self)

        # Vérification de la position dans la fenêtre
        in_window(self)

        # Régénération de la santé avec un maximum défini
        self.health = min(self.health + self.Settings.HEALTH_SPEED, self.Settings.HEALTH_MAX)

        # Création du rectangle de collision
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.Settings.SIZE[0], self.Settings.SIZE[1])

        # Vérification de la santé pour la survie
        if self.health <= 0:
            self.health = 0
            return False
        
        return True

    def draw(self, screen):
        """
        La fonction de dessin est utilisée pour afficher une image sur l'écran à une position spécifiée.
        
        :param screen: Le paramètre screen est l'objet de surface représentant la fenêtre ou l'écran de
        jeu où l'image sera dessinée
        """
        screen.blit(self.image, self.pos)

# Type Item
# Number Item : Coin, Weapon, Bullet

# La classe Coin représente un objet pièce dans le jeu, avec divers paramètres et méthodes pour mettre
# à jour et dessiner la pièce.
class Coin:
    class Settings:
        
        ID_TYPE = 0x1
        ID_NUMBER = 0x0
        ID_NAME = "Coin"
        HEALTH_MAX = 1
        HEALTH_SPEED = 0
        VALUE = 100
        MAPWIDTH = 3
        MAPHEIGHT = 3
        TILESIZE = 5
        SIZE = (MAPHEIGHT * TILESIZE, MAPWIDTH * TILESIZE)
        FORM = [[0, 7, 0],
                [7, 7, 7],
                [0, 7, 0]]

    def __init__(self, entity_manager):
        """
        La fonction initialise un objet avec des propriétés telles que le gestionnaire d'entités,
        l'identifiant, l'image, la position, la santé et le score.
        
        :param entity_manager: Le paramètre `entity_manager` est une instance d'une classe qui gère les
        entités du jeu. Il est utilisé pour accéder à l'ID unique de l'entité en cours d'initialisation
        """
        self.entity_manager = entity_manager
        self.id = self.entity_manager.id
        self.image = surface(self.Settings)
        self.pos = [rd.randint(0, SETTING.SCREEN_SIZE[0] - self.Settings.SIZE[0]),
                    rd.randint(0, SETTING.SCREEN_SIZE[1] - self.Settings.SIZE[1])]
        self.health = self.Settings.HEALTH_MAX
        self.score = 0

    def update(self):
        """
        La fonction de mise à jour augmente la santé d'un objet, met à jour sa position et vérifie si la
        santé est nulle ou inférieure.
        :return: une valeur booléenne. Si la santé est supérieure à 0, elle renvoie True. Si la santé
        est inférieure ou égale à 0, elle renvoie False.
        """
        self.health = min(self.health + self.Settings.HEALTH_SPEED, self.Settings.HEALTH_MAX)
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.Settings.SIZE[0], self.Settings.SIZE[1])

        if self.health <= 0:
            self.health = 0
            return False
        return True

    def draw(self, screen):
        """
        La fonction de dessin est utilisée pour afficher une image sur l'écran à une position spécifiée.
        
        :param screen: Le paramètre screen est l'objet surface représentant la fenêtre ou l'écran de jeu
        sur lequel l'image sera dessinée
        """
        screen.blit(self.image, self.pos)

# La classe ci-dessus représente une arme dans le jeu, avec des attributs tels que la position, le
# mouvement, les actions, la santé et le score.
class Weapon:
    
    # La classe Paramètres contient divers paramètres et identifiants pour une arme, notamment des
    # paramètres de santé, de valeur, de munitions et de dessin.
    class Settings:
        # Identifiants
        ID_TYPE = 0x1
        ID_NUMBER = 0x1
        ID_NAME = "Weapon"
        # Parametres
        HEALTH_MAX = 10
        HEALTH_SPEED = 0
        VALUE = 300 
        AMMO_MAX = 10 # Taille du chargeur
        AMMO_TIME = 0.5 # Temps en s entre chaque tire 
        # Parametres de dessin
        MAPWIDTH = 2
        MAPHEIGHT = 4
        TILESIZE = 5
        SIZE = (MAPHEIGHT * TILESIZE, MAPWIDTH * TILESIZE)
        FORM = [[6, 6, 6, 6],
                [6, 0, 0, 0]]

    def __init__(self, entity_manager):
        """
        La fonction initialise divers attributs d'une entité dans un jeu, tels que sa position, ses
        mouvements, ses actions, sa santé et son score.
        
        :param entity_manager: Le paramètre `entity_manager` est une instance d'une classe qui gère les
        entités du jeu. Il dispose probablement de méthodes pour créer, mettre à jour et supprimer des
        entités, ainsi que pour suivre leurs identifiants
        """
        self.entity_manager = entity_manager
        self.id = self.entity_manager.id
        self.pos = [rd.randint(0, SETTING.SCREEN_SIZE[0] - self.Settings.SIZE[0]),
                    rd.randint(0, SETTING.SCREEN_SIZE[1] - self.Settings.SIZE[1])]
        self.move = [0, 0]
        self.action_1_bool = False
        self.action_2_bool = False
        self.in_inventory = False
        self.health = self.Settings.HEALTH_MAX
        self.score = 0
        self.ammo_last_attack = 0
        self.image_normal = surface(self.Settings)
        self.image_flip = pygame.transform.flip(self.image_normal, True, False)
        self.image_flip_bool = False
        self.image = self.image_normal

    def update(self, data=None):
        """
        La fonction met à jour la position, la santé et l'image d'un objet en fonction de son mouvement
        et de son état d'inventaire.
        
        :param data: Le paramètre « data » est un objet qui contient des informations sur le mouvement
        et la position du joueur. Il possède les attributs suivants :
        :return: une valeur booléenne. Si la condition « if not self.in_inventory » est vraie, elle
        renvoie « True ». Si la condition « si self.in_inventory et data » est vraie, elle renvoie «
        False ».
        """

        if not self.in_inventory:
            self.health = min(self.health + self.Settings.HEALTH_SPEED, self.Settings.HEALTH_MAX)
            self.pos[0] += self.move[0]
            self.pos[1] += self.move[1]
            self.rect = pygame.Rect(self.pos[0], self.pos[1], self.Settings.SIZE[0], self.Settings.SIZE[1])
            if self.health <= 0:
                self.health = 0
                return False
            return True
        
        if self.in_inventory and data:

            if data.move[0] > 0:
                self.pos[0] = data.pos[0] + data.Settings.SIZE[0]
                if self.image_flip_bool == True:
                    self.image = self.image_normal
                    self.image_flip_bool = False
            elif data.move[0] < 0:
                self.pos[0] = data.pos[0] - self.Settings.SIZE[0]
                if self.image_flip_bool == False:
                    self.image = self.image_flip
                    self.image_flip_bool = True

            self.pos[1] = data.pos[1] + data.Settings.SIZE[1]//4

            self.ammo_last_attack += 1/SETTING.FPS

            in_window(self)

            self.rect = pygame.Rect(self.pos[0], self.pos[1], self.Settings.SIZE[0], self.Settings.SIZE[1])
            return False
        
    def action_1(self,data):
        """
        La fonction `action_1` vérifie si le joueur a suffisamment de munitions et si c'est le cas, crée
        une entité balle et l'ajoute au gestionnaire d'entités, ainsi qu'une entité explosion, à la
        position appropriée et dans la direction appropriée.
        
        :param data: Le paramètre "data" est un objet qui contient divers paramètres et informations
        nécessaires à l'action. Il inclut probablement des propriétés telles que « inventaire » (qui
        représente l'inventaire du joueur), « Paramètres » (qui contient les paramètres du jeu), «
        entity_manager » (qui gère les entités du jeu), « pos » (qui
        """

        if self.action_1:
            if self.Settings.AMMO_TIME < self.ammo_last_attack:
                if data.inventory.if_in("Bullet"):

                    self.ammo_last_attack = 0
                    bullet = data.inventory.find("Bullet")
                    data.inventory.remove(bullet)
                    self.entity_manager.add_entity(bullet)

                    if self.image_flip_bool == True:
                        bullet.pos[0] = self.pos[0] - data.move[0]
                        explosion = Explosion(self.entity_manager, [self.pos[0],self.pos[1]+self.Settings.SIZE[1]/2], dir = pi)

                    if self.image_flip_bool == False:
                        bullet.pos[0] = self.pos[0]+data.Settings.SIZE[0] - data.move[0]
                        explosion = Explosion(self.entity_manager, [self.pos[0]+data.Settings.SIZE[0],self.pos[1]+self.Settings.SIZE[1]/2], dir = 0)

                    self.entity_manager.add_entity(explosion)
                    
                    bullet.pos[1] = self.pos[1]+self.Settings.SIZE[1]/2

                    bullet.move[0] = bullet.Settings.SPEED_MAX * (-1) if self.image_flip_bool else bullet.Settings.SPEED_MAX * 1
                    print("Feu !!!")
                else : print("Plus de munition !")



    def draw(self, screen):
        """
        La fonction de dessin est utilisée pour afficher une image sur l'écran à une position spécifiée.
        
        :param screen: Le paramètre screen est l'objet de surface représentant la fenêtre ou l'écran de
        jeu où l'image sera dessinée
        """
        screen.blit(self.image, self.pos)

class Bullet:
    class Settings:
        # Identifiants
        ID_TYPE = 0x1
        ID_NUMBER = 0x2
        ID_NAME = "Bullet"
        # Parametre
        HEALTH_MAX = 10
        HEALTH_SPEED = 0
        SPEED_MAX = 30
        SPEED_DECREASE = 0.01
        DAMAGE = 50
        VALUE = 20
        # Parametre de dessin
        MAPWIDTH = 1
        MAPHEIGHT = 3
        TILESIZE = 3
        SIZE = (MAPHEIGHT * TILESIZE, MAPWIDTH * TILESIZE)
        FORM = [[7, 6, 5]]

    def __init__(self, entity_manager):

        self.entity_manager = entity_manager
        self.id = self.entity_manager.id
        self.pos = [rd.randint(0, SETTING.SCREEN_SIZE[0] - self.Settings.SIZE[0]),
                    rd.randint(0, SETTING.SCREEN_SIZE[1] - self.Settings.SIZE[1])]
        self.move = [0, 0]
        self.action_1_bool = False
        self.action_2_bool = False
        self.in_inventory = False
        self.fire = False
        self.health = self.Settings.HEALTH_MAX
        self.image = surface(self.Settings)
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.Settings.SIZE[0], self.Settings.SIZE[1])

    def update(self, data=None):

        if not self.in_inventory:
            self.health = min(self.health + self.Settings.HEALTH_SPEED, self.Settings.HEALTH_MAX)
            self.pos[0] += self.move[0]
            self.pos[1] += self.move[1]
            self.move[0] *= 1 - self.Settings.SPEED_DECREASE
            in_window(self)
            self.rect = pygame.Rect(self.pos[0], self.pos[1], self.Settings.SIZE[0], self.Settings.SIZE[1])
            if self.health <= 0:
                self.health = 0
                return False
            return True
        
        if self.in_inventory and data:
            self.pos = data.pos.copy()

            if self.action_1_bool :

                bullet = data.inventory.get_active_item()
                
                self.entity_manager.add(bullet)
                self.in_inventory = False

            self.rect = pygame.Rect(self.pos[0], self.pos[1], self.Settings.SIZE[0], self.Settings.SIZE[1])
            return False
        
    def action_1(self, data):
        pass
        


    def draw(self, screen):
        screen.blit(self.image, self.pos)

# Type Particle

# La classe Explosion représente une explosion dans un jeu, avec des particules qui se déplacent et
# s'estompent avec le temps.
class Explosion:
    class Settings:
        ID_TYPE = 0x2
        ID_NUMBER = 0x0
        ID_NAME = "Explosion"
        DURATION_MAX = 0.7 # durée en s
        PARTICLE_MAX = 20
        PARTICLE_SPEED_MAX = 5
        PARTICLE_SPEED_NOISE = 0.5
        PARTICLE_SPEED_DECREASE = 2 / SETTING.FPS
        MAPWIDTH = 1
        MAPHEIGHT = 3
        TILESIZE = 2
        SIZE = (MAPHEIGHT * TILESIZE, MAPWIDTH * TILESIZE)
        FORM = [[4, 1, 7]]

    def __init__(   self, 
        
                    entity_manager, 
                    pos = [rd.randint(0, SETTING.SCREEN_SIZE[0] - Settings.SIZE[0]),
                        rd.randint(0, SETTING.SCREEN_SIZE[1] - Settings.SIZE[1])],
                    dir = pi/2
                ):
        
        """
        La fonction initialise un objet particule avec divers attributs et paramètres.
        
        :param entity_manager: Le paramètre `entity_manager` est une instance de la classe
        `EntityManager`. Il est utilisé pour gérer et suivre toutes les entités du jeu
        :param pos: Le paramètre `pos` est une liste qui représente la position initiale de l'objet. Il
        contient deux éléments : la coordonnée x et la coordonnée y de la position. La valeur par défaut
        de « pos » est une position générée aléatoirement dans la taille de l'écran définie dans «
        SETTING.SCREEN_SIZE »
        :param dir: Le paramètre "dir" représente la direction initiale de la particule. Il est spécifié
        en radians et détermine l'angle selon lequel la particule se déplacera initialement
        """
        
        self.entity_manager = entity_manager
        self.id = self.entity_manager.id

        self.image = surface(self.Settings)
        self.images = []
        self.move = []
        self.pos = []

        for i in range(self.Settings.PARTICLE_MAX):
            angle = rd.random() * pi
            speed = (1 - rd.random() * self.Settings.PARTICLE_SPEED_NOISE) * self.Settings.PARTICLE_SPEED_MAX
            self.images.append(pygame.transform.rotate(self.image, angle*360))
            self.move.append([speed* sin(angle+dir), speed* cos(angle+dir)])
            self.pos.append(pos.copy())
        self.duration = 0

        self.rect = pygame.Rect(self.pos[0][0], self.pos[0][1], self.Settings.SIZE[0], self.Settings.SIZE[1])

    def update(self):
        """
        La fonction met à jour la position et la vitesse des particules et vérifie si la durée a dépassé
        la durée maximale.
        :return: une valeur booléenne. Si la durée est supérieure à la durée maximale, elle renvoie
        False. Sinon, il renvoie True.
        """
        
        for i in range(self.Settings.PARTICLE_MAX):

            self.pos[i][0] += self.move[i][0]
            self.pos[i][1] += self.move[i][1]

            self.move[i][0] *= 1 - self.Settings.PARTICLE_SPEED_DECREASE
            self.move[i][1] *= 1 - self.Settings.PARTICLE_SPEED_DECREASE

            self.rect = pygame.Rect(self.pos[i][0], self.pos[i][1], self.Settings.SIZE[0], self.Settings.SIZE[1])

        if self.duration > self.Settings.DURATION_MAX:
            return False
        
        self.duration += 1 / SETTING.FPS

        return True

    def draw(self, screen):
        """
        La fonction dessine des particules sur l'écran en utilisant leurs images et leurs positions.
        
        :param screen: Le paramètre "screen" est l'objet surface représentant la fenêtre de jeu ou
        l'écran sur lequel vous souhaitez dessiner les particules
        """
        for i in range(self.Settings.PARTICLE_MAX):
            screen.blit(self.images[i], self.pos[i])


# Gestionnaire d'inventaire

# La classe Inventory représente une collection d'éléments avec des méthodes pour ajouter, supprimer,
# mettre à jour, dessiner, définir un élément actif, obtenir un élément actif, vérifier si un élément
# est dans l'inventaire et rechercher un élément par son nom.
class Inventory:

    EMPTY_SLOT = None

    def __init__(self, inventory_size):
        """
        La fonction initialise un inventaire avec une taille spécifiée et définit le nombre
        d'utilisations d'articles sur 0.
        
        :param inventory_size: Le paramètre `inventory_size` est la taille ou la capacité de
        l'inventaire. Il détermine le nombre d'emplacements ou d'espaces disponibles dans l'inventaire
        """
        self.inventory = [self.EMPTY_SLOT] * inventory_size
        self.item_use = 0   

    def add(self, obj):
        """
        La fonction ajoute un objet à la liste d'inventaire s'il y a un emplacement vide disponible.
        
        :param obj: Le paramètre "obj" représente l'objet que vous souhaitez ajouter à l'inventaire
        :return: La méthode add renvoie une valeur booléenne. Il renvoie True si l'objet a été ajouté
        avec succès à l'inventaire et False s'il n'y a aucun emplacement vide disponible dans
        l'inventaire.
        """

        for index, item in enumerate(self.inventory):
            if item is self.EMPTY_SLOT:
                obj.in_inventory = True
                self.inventory[index] = obj
                return True
        return False
    
    def remove(self, obj):
        """
        La fonction supprime un objet d'une liste et met à jour son statut dans l'inventaire.
        
        :param obj: Le paramètre "obj" représente l'objet que vous souhaitez supprimer de l'inventaire
        :return: La méthode Remove renvoie une valeur booléenne. Il renvoie True si l'objet est supprimé
        avec succès de l'inventaire et False si l'objet est introuvable dans l'inventaire.
        """
        for index, item in enumerate(self.inventory):
            if item is obj:
                obj.in_inventory = False
                self.inventory[index] = self.EMPTY_SLOT
                return True
        return False
    
    def update(self, data):
        """
        La fonction met à jour l'article actuel dans l'inventaire avec les données fournies.
        
        :param data: Le paramètre « data » est une variable qui représente les informations ou les
        données transmises à la méthode « update ». Il peut s'agir de n'importe quel type de données,
        comme une chaîne, un nombre, une liste ou même un objet. Le type spécifique de données dépend du
        contexte et de la finalité de
        """
        current_item = self.inventory[self.item_use]
        if current_item is not self.EMPTY_SLOT:
            current_item.update(data)

    def draw(self, screen):
        """
        La fonction dessine l'élément actuel sur l'écran s'il ne s'agit pas d'un emplacement vide.
        
        :param screen: Le paramètre « écran » est la surface sur laquelle le jeu est affiché. Il s'agit
        généralement d'un objet Surface pygame
        """
        current_item = self.inventory[self.item_use]
        if current_item is not self.EMPTY_SLOT:
            current_item.draw(screen)

    def set_active_item(self, index):
        """
        La fonction définit l'élément actif dans l'inventaire en fonction de l'index donné.
        
        :param index: Le paramètre index représente la position de l'élément dans la liste d'inventaire
        que vous souhaitez définir comme élément actif
        """
        if 0 <= index < len(self.inventory):
            self.item_use = index

    def get_active_item(self):
        """
        La fonction renvoie l'article actif de l'inventaire.
        :return: L'élément à l'index spécifié par l'attribut "item_use" dans la liste "inventaire".
        """
        return self.inventory[self.item_use]
    
    def if_in(self, item_name):
        """
        La fonction vérifie si un article avec un nom spécifique existe dans l'inventaire.
        
        :param item_name: Le paramètre `item_name` est une chaîne qui représente le nom d'un élément
        :return: une valeur booléenne. Il renvoie True si l'élément portant le nom spécifié est trouvé
        dans l'inventaire, et False dans le cas contraire.
        """
        for item in self.inventory:
            if item is not self.EMPTY_SLOT:
                if item_name == item.Settings.ID_NAME:
                    return True
        return False
    
    def find(self, item_name):
        """
        La fonction recherche un article dans l'inventaire en fonction de son nom et renvoie l'article
        s'il est trouvé.
        
        :param item_name: Le paramètre `item_name` est une chaîne qui représente le nom de l'article que
        vous recherchez dans l'inventaire
        :return: L'élément qui correspond au nom_élément donné est renvoyé.
        """
        for item in self.inventory:
            if item is not self.EMPTY_SLOT:
                if item_name == item.Settings.ID_NAME:
                    return item

# gestionnaire d'entité
         
# La classe Entity représente une collection d'entités dans un jeu, avec des méthodes pour ajouter,
# mettre à jour, vérifier les collisions, gérer les collisions et dessiner les entités.
class Entity:

    def __init__(self):
        """
        La fonction initialise un objet avec un identifiant et un dictionnaire vide pour les entités.
        """
        self.id = 0x0
        self.entities = {}

    def add_entity(self, entity):
        """
        La fonction ajoute une entité à un dictionnaire avec un identifiant unique.
        
        :param entity: Le paramètre « entité » est un objet qui représente une entité. Il peut s'agir de
        n'importe quel type d'entité, comme une personne, une voiture ou un produit. L'attribut "id" de
        l'objet entité est utilisé comme clé pour stocker l'entité dans le dictionnaire "entités"
        """
        self.entities[entity.id] = entity
        self.id += 1

    def update(self):
        """
        La fonction met à jour les entités dans un dictionnaire et supprime les entités qui renvoient
        False lors de la mise à jour.
        """
        entities_to_remove = []

        for entity in list(self.entities.values()):
            if not entity.update():
                entities_to_remove.append(entity.id)

        for entity_id in entities_to_remove:
            del self.entities[entity_id]

    def check_collisions(self):
        """
        La fonction vérifie les collisions entre les entités et les gère si elles se produisent.
        """
        for entity_1 in self.entities.values():
            for entity_2 in self.entities.values():
                if entity_1 != entity_2 and entity_1.rect.colliderect(entity_2.rect):
                    self.handle_collision(entity_1, entity_2)

    def handle_collision(self, entity_1, entity_2):
        """
        La fonction `handle_collision` gère différents types de collisions entre entités dans un jeu,
        telles que les collisions entre les monstres et les joueurs, les monstres et les objets, et les
        balles et les monstres.
        
        :param entity_1: Le paramètre `entity_1` représente la première entité impliquée dans la
        collision. Il peut s'agir d'un joueur, d'un ennemi ou d'un objet
        :param entity_2: Le paramètre `entity_2` représente la deuxième entité impliquée dans la
        collision. Il peut s'agir d'un joueur, d'un ennemi, d'une pièce de monnaie ou d'un objet. Le type
        spécifique d'entité est déterminé par les variables `ID_TYPE_2` et `ID_NUMBER_2`
        """
        
        ID_TYPE_1 = entity_1.Settings.ID_TYPE
        ID_TYPE_2 = entity_2.Settings.ID_TYPE

        ID_NUMBER_1 = entity_1.Settings.ID_NUMBER
        ID_NUMBER_2 = entity_2.Settings.ID_NUMBER

        # MOB Collide MOB
        if ID_TYPE_1 == 0x0 and ID_TYPE_2 == 0x0 :
            # Ennemie Collide Player
            if ID_NUMBER_1 == 0x1 and ID_NUMBER_2 == 0x0 :
                # Player Lose Life
                entity_2.health -= entity_1.Settings.DAMAGE
                # Player Lose Score
                entity_2.score -= 1
            
        # MOB Collide ITEM
        if ID_TYPE_1 == 0x0 and ID_TYPE_2 == 0x1 :
            # Player Collide :
            if ID_NUMBER_1 == 0x0 :
                # Coin
                if ID_NUMBER_2 == 0x0 :
                    # Coin Lose Life
                    entity_2.health -= 1
                    # Player Earn Score 
                    entity_1.score += entity_2.Settings.VALUE
                # Item
                if ID_NUMBER_2 == 0x1 :
                    # Player Earn Weapon
                    entity_1.inventory.add(entity_2)

        # ITEM Collide MOB
        if ID_TYPE_1 == 0x1 and ID_TYPE_2 == 0x0 :
            # Bullet Collide MOB
            if ID_NUMBER_1 == 0x2:

                speed = sqrt(entity_1.move[0]**2+entity_1.move[1]**2)
                entity_1.move[0] = 0
                entity_1.move[1] = 0
                if speed > 6 :
                    entity_2.health -= entity_1.Settings.DAMAGE * speed / entity_1.Settings.SPEED_MAX
                    print(entity_2.Settings.ID_NAME + " : " + str(entity_2.health))
                elif speed < 4 :
                    entity_2.inventory.add(entity_1)

    def if_in(self, entity_name):
        """
        La fonction vérifie si un article avec un nom spécifique existe dans l'inventaire.
        
        :param item_name: Le paramètre `item_name` est une chaîne qui représente le nom d'un élément
        :return: une valeur booléenne. Il renvoie True si l'élément portant le nom spécifié est trouvé
        dans l'inventaire, et False dans le cas contraire.
        """
        for entity in list(self.entities.values()):
            if entity_name == entity.Settings.ID_NAME:
                return True
        return False
    
    def draw(self, screen):
        """
        La fonction parcourt toutes les entités d'un dictionnaire et appelle leur méthode draw avec un
        paramètre d'écran donné.
        
        :param screen: Le paramètre "écran" est la surface sur laquelle les entités seront dessinées. Il
        s'agit généralement de la surface d'affichage principale du jeu ou de l'application
        """
        for entity in self.entities.values():
            entity.draw(screen)

# Other Function
def in_window(self):
    """
    La fonction vérifie si une entité se trouve dans les limites de la fenêtre et ajuste sa position en
    conséquence.
    """
    # verifie if entity are in windows and move player on the window if is not in.
    self.move[1] += GRAVITY
    if self.pos[0] > SETTING.SCREEN_SIZE[0]:
        self.pos[0] = - self.Settings.SIZE[0]
    elif self.pos[0] < -self.Settings.SIZE[0]:
        self.pos[0] = SETTING.SCREEN_SIZE[0]
    if self.pos[1] > SETTING.SCREEN_SIZE[1] - self.Settings.SIZE[1]:
        self.pos[1] = SETTING.SCREEN_SIZE[1] - self.Settings.SIZE[1]
        self.move[1] = 0
    elif self.pos[1] < 0:
        self.pos[1] = 0
        self.move[1] = 0

def surface(Settings):
    """
    La fonction "surface" crée un objet Surface pygame et y dessine des rectangles en fonction des
    valeurs de l'objet Paramètres.
    
    :param Settings: Le paramètre "Paramètres" est un objet ou un dictionnaire qui contient différents
    paramètres pour la surface. Il comprend probablement les attributs suivants :
    :return: une surface d’image.
    """

    # Le code ci-dessus crée une image à l'aide de la bibliothèque pygame en Python. Il parcourt
    # chaque ligne et colonne de la matrice Settings.FORM et vérifie si la valeur n'est pas égale à 0.
    # Si elle n'est pas égale à 0, il dessine un rectangle sur la surface de l'image à l'aide de la
    # fonction pygame.draw.rect(). . La couleur du rectangle est déterminée par la valeur du
    # dictionnaire COLOR en fonction de la valeur de la matrice Settings.FORM. La position et la
    # taille du rectangle sont déterminées par les valeurs de ligne et de colonne multipliées par
    # Settings.TILESIZE.
    image = pygame.Surface(Settings.SIZE)
    for row in range(Settings.MAPWIDTH):
            for column in range(Settings.MAPHEIGHT):
                if Settings.FORM[row][column] != 0:
                    pygame.draw.rect(image, COLOR[Settings.FORM[row][column]], (column*Settings.TILESIZE, row*Settings.TILESIZE, Settings.TILESIZE, Settings.TILESIZE))

    # Le code ci-dessus convertit une image dans un format prenant en charge la transparence (canal
    # alpha).
    image = image.convert_alpha()

    return image

