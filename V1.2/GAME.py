import pygame
from pygame.locals import *
import random as rd
import MOB
import SETTING
import ML

# La classe Game initialise une fenêtre de jeu, gère les entités, gère les entrées utilisateur, met à
# jour les entités, vérifie les collisions et dessine l'écran de jeu.
class Game:

    def __init__(self):
        """
        La fonction initialise un écran de jeu, configure des entités telles que le joueur, l'ennemi,
        l'arme, la balle et la pièce, et démarre une boucle de jeu.
        """

        # L'extrait de code initialise la bibliothèque Pygame, configure la fenêtre de jeu, définit la
        # légende de la fenêtre, active l'économiseur d'écran et crée un objet horloge pour contrôler
        # la fréquence d'images du jeu.
        pygame.init()

        self.screen = pygame.display.set_mode(SETTING.SCREEN_SIZE)

        pygame.display.set_caption("ML_GAME")
        pygame.display.set_allow_screensaver(True)

        self.clock = pygame.time.Clock()
        
        # Le code crée des instances de différentes entités (joueur, ennemi, arme, balle, pièce) et
        # les ajoute au gestionnaire d'entités. Le gestionnaire d'entités est responsable de la
        # gestion et de la mise à jour de toutes les entités du jeu. Chaque entité a son propre
        # comportement et ses propres propriétés, et en les ajoutant au gestionnaire d'entités, elles
        # peuvent interagir entre elles et être mises à jour dans la boucle du jeu.
        self.entity_manager = MOB.Entity()

        player = MOB.Player(self.entity_manager)
        self.entity_manager.add_entity(player)
        
        for x in range(5):
            enemy = MOB.Ennemy(self.entity_manager)
            self.entity_manager.add_entity(enemy)

        for x in range(50):
            bullet = MOB.Bullet(self.entity_manager)
            self.entity_manager.add_entity(bullet)

        for x in range(5):
            weapon = MOB.Weapon(self.entity_manager)
            self.entity_manager.add_entity(weapon)

            coin = MOB.Coin(self.entity_manager)
            self.entity_manager.add_entity(coin)

        self.loop()

    def reset(self):
        """
        La fonction réinitialise l'objet entité en le supprimant et en créant une nouvelle instance avec
        les attributs de joueur, d'ennemi et de pièce.
        """

        del self.entity_manager

        self.entity_manager = MOB.Entity()

        player = MOB.Player(self.entity_manager)
        self.entity_manager.add_entity(player)
        
        for x in range(self.nb_ennemis):
            enemy = MOB.Ennemy(self.entity_manager)
            self.entity_manager.add_entity(enemy)

        for x in range(50):
            bullet = MOB.Bullet(self.entity_manager)
            self.entity_manager.add_entity(bullet)

        for x in range(self.nb_ennemis - 1):
            weapon = MOB.Weapon(self.entity_manager)
            self.entity_manager.add_entity(weapon)

            coin = MOB.Coin(self.entity_manager)
            self.entity_manager.add_entity(coin)

        self.loop()

    def loop(self):
        """
        La fonction de boucle met continuellement à jour les entités, vérifie les collisions et dessine
        le jeu.
        """
        while True:
            self.key()
            self.entity_manager.update()
            self.entity_manager.check_collisions()
            self.draw()
            if not self.entity_manager.if_in("Ennemie"):
                break
        self.reset()
    
    def key(self):
        """
        La fonction « clé » gère la saisie au clavier pour contrôler le mouvement et les actions d'une
        entité dans un jeu.
        """

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            
            self.entity_manager.entities[0].move[1] -= 0.2 if self.entity_manager.entities[0].move[1] > -4 else 0
        if keys[pygame.K_DOWN]:
            self.entity_manager.entities[0].move[1] += 0.2 if self.entity_manager.entities[0].move[1] < 4 else 0
        if keys[pygame.K_RIGHT]:
            self.entity_manager.entities[0].move[0] += 0.2 if self.entity_manager.entities[0].move[0] < 4 else 0
        if keys[pygame.K_LEFT]:
            self.entity_manager.entities[0].move[0] -= 0.2 if self.entity_manager.entities[0].move[0] > -4 else 0
        if keys[pygame.K_SPACE]:
            self.entity_manager.entities[0].action_1_bool = True
        else:
            self.entity_manager.entities[0].action_1_bool = False

        if keys[pygame.K_1]:
            self.entity_manager.entities[0].inventory.set_active_item(0)
        if keys[pygame.K_2]:
            self.entity_manager.entities[0].inventory.set_active_item(1)
        if keys[pygame.K_3]:
            self.entity_manager.entities[0].inventory.set_active_item(2)
        if keys[pygame.K_4]:
            self.entity_manager.entities[0].inventory.set_active_item(3)
        if keys[pygame.K_5]:
            self.entity_manager.entities[0].inventory.set_active_item(4)
        if keys[pygame.K_6]:
            self.entity_manager.entities[0].inventory.set_active_item(5)
        if keys[pygame.K_7]:
            self.entity_manager.entities[0].inventory.set_active_item(6)
        if keys[pygame.K_8]:
            self.entity_manager.entities[0].inventory.set_active_item(7)
        if keys[pygame.K_9]:
            self.entity_manager.entities[0].inventory.set_active_item(8)
        if keys[pygame.K_0]:
            self.entity_manager.entities[0].inventory.set_active_item(9)
    
    def draw(self):
        """
        La fonction de dessin remplit l'écran d'une couleur noire, dessine des entités sur l'écran et met
        à jour l'affichage.
        """

        self.screen.fill((0,0,0))
        self.entity_manager.draw(self.screen)
        #IA[0].Draw_ML(pygame, self.screen,(0,0), (self.size[0],self.size[1]))
        self.clock.tick_busy_loop(SETTING.FPS)
        pygame.display.update()

g = Game()
