import random as rd

class Ml:

    def __init__(self):
        """
        Initialise les paramètres du réseau de neurones.
        - score_best: Meilleur score obtenu.
        - score_best_last: Dernier meilleur score obtenu.
        - connection: Matrice de connexion entre les neurones.
        - neron_weight: Poids des neurones.
        - neron_value: Valeurs des neurones.
        - neron_couche: Nombre de neurones par couche.
        Initialise les matrices de connexion et les poids.
        Initialise les meilleures connexions locales et globales.
        """

        # Initialisation des paramètres du réseau de neurones
        self.score_best = 0 # Meilleur score obtenu
        self.score_best_last = 1 # Initialisation à 1 pour éviter la division par 0
        self.connection = {}    # Matrice de connexion entre les neurones
        self.neron_weight = {}  # Poids des neurones
        self.neron_value = {}   # Valeurs des neurones
        self.neron_couche = [4,5,3]   # Nombre de neurones par couche

        # Initialisation des matrices de connexion et poids
        for couche in range(len(self.neron_couche)-1):
            for enter in range(self.neron_couche[couche]):
                for output in range(self.neron_couche[couche+1]):
                    self.connection[str(couche)+str(enter)+str(output)] = 0
                self.neron_weight[str(enter)+str(couche)] = 0

        for enter in range(self.neron_couche[-1]):
            self.neron_weight[str(enter)+str(couche+1)] = 0
                
        # Initialisation des meilleures connexions locales et globales
        self.best_connection_global = dict(self.connection)
        self.best_connection_local = dict(self.connection)

    def neron_calcul(self, inputs = []):
        """
        Calcule les valeurs des neurones du réseau de neurones.

        Args:
            inputs (list): Liste des valeurs d'entrée pour les neurones.

        Returns:
            list: Liste des valeurs des neurones de sortie.
        """

        # Recupération des entrées
        for i, input in enumerate(inputs):
            # Initialisation de la valeur du neurone d'entrée à la valeur d'entrée
            self.neron_value[str(i)+"0"] = input


        for couche in range(len(self.neron_couche)-1):
            # Parcours des couches du réseau de neurones (sauf la dernière couche)
            for output in range(self.neron_couche[couche+1]):
                # Parcours des neurones de sortie de la couche suivante (sorties)
                # Initialisation de la valeur du neurone de sortie à 0
                self.neron_value[str(output)+str(couche+1)] = 0
                for enter in range(self.neron_couche[couche]):
                    # Parcours des neurones de la couche actuelle (entrées)
                    # Calcul de la valeur du neurone de sortie en fonction des valeurs des neurones d'entrée, de la connexion et du poids
                    self.neron_value[str(output)+str(couche+1)] += self.neron_value[str(enter)+str(couche)]*self.connection[str(couche)+str(enter)+str(output)] * self.neron_weight[str(enter)+str(couche)]

        return [self.neron_value[str(i)+str(len(self.neron_couche)-1)] for i in range(self.neron_couche[-1])]

    def neron_update(self,pas):
        """
        Met à jour les connexions et les poids des neurones avec une taille de pas donnée.
        Paramètres :
        - pas (float) : La taille de pas pour mettre à jour les connexions et les poids.
        Description :
        - Cette méthode met à jour les connexions entre les neurones et les poids des neurones en utilisant une taille de pas donnée.
        - Elle commence par copier les meilleures connexions globales en tant que connexions initiales.
        - Ensuite, elle itère à travers les couches du réseau de neurones (sauf la dernière couche).
        - Pour chaque couche, elle itère à travers les neurones d'entrée de la couche actuelle.
        - Pour chaque neurone d'entrée, elle itère à travers les neurones de sortie de la couche suivante.
        - Elle met à jour la connexion entre les neurones avec un bruit aléatoire multiplié par la taille de pas.
        - Elle met également à jour les poids des neurones de la couche actuelle avec un bruit aléatoire multiplié par la taille de pas.
        - Enfin, elle itère à travers les neurones de la dernière couche et met à jour leurs poids avec un bruit aléatoire multiplié par la taille de pas.
        """

        # Mettre à jour les connexions entre les neurones
        self.connection = dict(self.best_connection_global)

        # Parcourir les couches du réseau de neurones (sauf la dernière couche)
        for couche in range(len(self.neron_couche)-1):
            # Parcourir les neurones d'entré de la couche actuelle
            for enter in range(self.neron_couche[couche]):
                # Parcourir les neurones de sortie de la couche suivante
                for output in range(self.neron_couche[couche+1]):
                    # Mettre à jour la connexion entre les neurones avec un bruit aléatoire
                    self.connection[str(couche)+str(enter)+str(output)] += pas*(rd.random()*2-1)
                # Mettre à jour les poids des neurones de la couche actuelle avec un bruit aléatoire
                self.neron_weight[str(enter)+str(couche)] += pas*(rd.random()*2-1)
        # Parcourir les neurones de la derniere couche
        for output in range(self.neron_couche[couche+1]):
            # Mettre à jour les poids des neurones de la derniere couche avec un bruit aléatoire
            self.neron_weight[str(output)+str(couche+1)] += pas*(rd.random()*2-1)

    def if_best(self, score=0, global_best=False):
        """
        Détermine si le score donné est le meilleur score et met à jour les meilleures connexions en conséquence.
        Paramètres :
        - score (int) : Le score à comparer avec le meilleur score.
        - global_best (bool) : Indicateur indiquant s'il faut mettre à jour les meilleures connexions globales.
        Renvoie :
        - bool : True si le score est le meilleur score, False sinon.
        """


        if global_best: # Si on veut mettre à jour les meilleures connexions globales
            self.best_connection_global = dict(self.best_connection_local)
            return True
        
        if score > self.score_best:  # Si le score est supérieur au meilleur score alors :
            self.best_connection_local = dict(self.connection)  # On change les meilleures connexions locales par les nouvelles meilleures
            self.score_best = int(score)  # On met à jour le meilleur score.
            self.score_best_last = 0  # On réinitialise le compteur du score_best_last
            return True
        else:
            self.score_best_last += 1  # On incrémente le compteur si le score n'est pas meilleur
            return False

    
    def neron_draw(self, pygame, screen, pos, size):
        """
        Dessine un réseau de neurones sur l'écran à l'aide de la bibliothèque Pygame.
        Args:
            pygame (module): Le module Pygame utilisé pour le dessin.
            screen (object): L'objet écran sur lequel le réseau de neurones sera dessiné.
            pos (tuple): La position de départ du réseau de neurones sur l'écran.
            size (tuple): La taille de l'écran sur lequel le réseau de neurones sera dessiné.
        Returns:
            None
        """

        for couche in range(len(self.neron_couche)-1):
            for neron in range(self.neron_couche[couche]):
                pos_x = (size[0])/(len(self.neron_couche)+1)*(couche+1)+pos[0]
                pos_y = (size[1])/(self.neron_couche[couche]+1)*(neron+1)+pos[1]
                neron_norm = abs((self.neron_value[str(neron)+str(couche)]-self.neron_min)/(self.neron_max-self.neron_min)*2-1)
                neron_weight_norm = abs((self.neron_weight[str(neron)+str(couche)]-self.neron_weight_min)/(self.neron_weight_max-self.neron_weight_min)*2-1)
                for neron_next in range(self.neron_couche[couche+1]):
                    connection_norm = (self.connection[str(couche)+str(neron)+str(neron_next)]-self.connection_min)/(self.connection_max-self.connection_min)
                    color = (neron_norm*neron_weight_norm*255,0,255)
                    pos_x_next = (size[0])/(len(self.neron_couche)+1)*(couche+2)+pos[0]
                    pos_y_next = (size[1])/(self.neron_couche[couche+1]+1)*(neron_next+1)+pos[1]
                    pygame.draw.line(screen, color, (pos_x,pos_y), (pos_x_next,pos_y_next), int((connection_norm*6)//1)) 
                color = (neron_norm*255,0,255)
                pygame.draw.circle(screen,color,(pos_x,pos_y), (neron_weight_norm*15)//1)
        for neron in range(self.neron_couche[-1]):
            neron_norm = (self.neron_value[str(neron)+str(couche)]-self.neron_min)/(self.neron_max-self.neron_min)
            color = (neron_norm*255,255,0)
            pos_y = (size[1])/(self.neron_couche[couche+1]+1)*(neron+1)+pos[1]
            pygame.draw.circle(screen,color,(pos_x_next,pos_y), 5)