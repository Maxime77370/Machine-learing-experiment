import random as rd

class Ml:

    def __init__(self):

        # Initialisation des paramètres du réseau de neurones
        self.score_best = 0
        self.score_best_last = 1
        self.connection = {}    # Matrice de connexion entre les neurones
        self.neron_weight = {}  # Poids des neurones
        self.neron_value = {}   # Valeurs des neurones
        self.neron_couche = [4,3]   # Nombre de neurones par couche

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
        # Calcul des valeurs des neurones

        # Recupération des entrées
        for i, input in enumerate(inputs):
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
        # Mettre à jour les connexions et les poids des neurones avec un certain pas
        # Utiliser les meilleures connexions globales comme point de départ

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
        
        if score > self.score_best:  # Si le score est supérieur au meilleur score alors :
            self.best_connection_local = dict(self.connection)  # On change les meilleures connexions locales par les nouvelles meilleures
            self.score_best = int(score)  # On met à jour le meilleur score.
            self.score_best_last = 0  # On réinitialise le compteur du score_best_last
        else:
            self.score_best_last += 1  # On incrémente le compteur si le score n'est pas meilleur

        if global_best:
            self.best_connection_global = dict(self.best_connection_local)
    
    def neron_draw(self, pygame, screen, pos, size):
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