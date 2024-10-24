# -*- coding: utf-8 -*-
import random
from Case import Case

DIFFICULTE = {
    "facile": {"taille_grille": (9, 9), "nb_bombes": 10, "taille_zone_safe": (2, 4)},
    "intermediaire": {"taille_grille": (16, 16), "nb_bombes": 40, "taille_zone_safe": (5, 10)},
    "avance": {"taille_grille": (30, 16), "nb_bombes": 75, "taille_zone_safe": (10, 20)},
}

class Grille(object):
    def __init__(self, difficulte="facile"):
        if difficulte in DIFFICULTE:
            config = DIFFICULTE[difficulte]
            self.largeur, self.longueur = config["taille_grille"]
            self.nb_bombes = config["nb_bombes"]
            self.taille_zone_safe_min, self.taille_zone_safe_max = config["taille_zone_safe"]
        else:
            raise ValueError(f"Difficulté {difficulte} non reconnue.")
        
        self.grille = []
        self.bombes_initialisees = False
        self.nb_cases_non_bombes = 0  
        self.initialiserGrille()
        self.drapeaux_restants = self.nb_bombes  # Compteur de drapeaux posés

    def initialiserGrille(self):
        # Crée une grille remplie de cases
        self.grille = [
            [Case(x=x, y=y, mine=False, devoilee=False, marquee=False, minesAdjacentes=0)
             for x in range(self.largeur)]
            for y in range(self.longueur)
        ]
        self.nb_cases_non_bombes = self.largeur * self.longueur - self.nb_bombes

    def creer_zone_safe(self, x_initial, y_initial):
        """
        Créer une zone sûre autour de la case initiale.
        
        Parameters
        ----------
        x_initial : int
            Position x de la case initiale.
        y_initial : int
            Position y de la case initiale.
        """
        zone_safe = set()
        zone_safe.add((x_initial, y_initial))

        # Déterminer la taille de la zone safe
        taille_zone_safe = random.randint(self.taille_zone_safe_min, self.taille_zone_safe_max)

        # Propagation de la zone safe à partir de la case initiale
        cases_a_traiter = [(x_initial, y_initial)]
        while len(zone_safe) < taille_zone_safe and cases_a_traiter:
            x, y = cases_a_traiter.pop(0)

            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    if dx == 0 and dy == 0:
                        continue  # Ignorer la case elle-même
                    nx, ny = x + dx, y + dy

                    if 0 <= nx < self.largeur and 0 <= ny < self.longueur:
                        if (nx, ny) not in zone_safe:
                            zone_safe.add((nx, ny))
                            cases_a_traiter.append((nx, ny))

        for position in zone_safe:
            # Assurez-vous que toutes les cases dans la zone sûre ne contiennent pas de mines
            self.grille[position[1]][position[0]].devoilee = True

        return zone_safe

    def placerBombes(self, x_initial, y_initial):
        """
        Placer les bombes sur la grille après avoir créé la zone sûre.

        Parameters
        ----------
        x_initial : int
            Position x de la case initiale (premier clic).
        y_initial : int
            Position y de la case initiale (premier clic).
        """
        # Récupérer les positions possibles pour placer les bombes
        positions_possibles = [(x, y) for x in range(self.largeur) for y in range(self.longueur)]

        # Créer la zone sûre autour de la case initiale
        zone_safe = self.creer_zone_safe(x_initial, y_initial)

        # Éliminer les positions dans la zone sûre de la liste des positions possibles
        for position in zone_safe:
            positions_possibles.remove(position)

        # Placer les bombes
        bombes = random.sample(positions_possibles, self.nb_bombes)

        for x, y in bombes:
            self.grille[y][x].mine = True

        # Calculer les mines adjacentes pour chaque case
        for ligne in self.grille:
            for case in ligne:
                case.calculerMinesAdjacentes(self.grille)

        self.bombes_initialisees = True

    def marquer(self, x, y):
        if 0 <= x < self.largeur and 0 <= y < self.longueur:
            case = self.grille[y][x]
            if not case.devoilee:
                case.marquee = not case.marquee
                if case.marquee:
                    self.drapeaux_restants -= 1  # Décrémente le compteur de drapeaux restants
                else:
                    self.drapeaux_restants += 1  # Incrémente le compteur de drapeaux restants si le drapeau est retiré
        else:
            print("Coordonnées hors limites !")

    def devoiler(self, x, y):
        if (0 <= x < self.largeur and 0 <= y < self.longueur):
            case = self.grille[y][x]
            
            # Si les bombes ne sont pas encore initialisées
            if not self.bombes_initialisees:
                # Placer les bombes après la création de la zone sûre
                self.placerBombes(x, y)
                self.devoilee = True
                self.devoilerCasesAdjacentes(x, y)
            else:
                if not case.devoilee and not case.marquee:
                    case.devoilee = True

                    if case.minesAdjacentes == 0:
                        self.devoilerCasesAdjacentes(x, y)
            
            # Vérifier si le joueur a gagné après avoir dévoilé une case
            if self.verifier_gagne():
                print("Vous avez gagné !")
                return True  # Indiquer que le jeu est gagné

        return False  # Indiquer que le jeu continue
    
    def devoilerCasesAdjacentes(self, x, y):
        """
        Révèle les cases adjacentes qui n'ont pas de mines adjacentes.
        
        Parameters
        ----------
        x : int
            Position x de la case actuelle.
        y : int
            Position y de la case actuelle.
        """
        # Créer une pile ou une file d'attente pour les cases à dévoiler
        cases_a_devoiler = [(x, y)]
        deja_devoilees = set()  # Pour éviter de reprocesser des cases
    
        while cases_a_devoiler:
            cx, cy = cases_a_devoiler.pop(0)  # Récupère la prochaine case à traiter
    
            if (cx, cy) in deja_devoilees:
                continue  # Évite de traiter plusieurs fois la même case
    
            deja_devoilees.add((cx, cy))  # Marquer la case comme traitée
            case = self.grille[cy][cx]
    
            if not case.devoilee:
                case.devoilee = True  # Révéler la case
    
            # Si la case a 0 mines adjacentes, propager la révélation aux voisines
            if case.minesAdjacentes == 0:
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        nx, ny = cx + dx, cy + dy
    
                        # Vérifier que la case voisine est dans la grille
                        if 0 <= nx < self.largeur and 0 <= ny < self.longueur:
                            # Si la case n'est pas encore dévoilée et pas déjà dans la liste
                            if (nx, ny) not in deja_devoilees:
                                cases_a_devoiler.append((nx, ny))




    def verifier_gagne(self):
        """
        Vérifie si le joueur a gagné.
        
        Returns
        -------
        bool
            True si le joueur a gagné, sinon False.
        """
        for ligne in self.grille:
            for case in ligne:
                # Si la case n'est pas une mine et n'est pas dévoilée
                if not case.mine and not case.devoilee:
                    return False  # Le jeu continue
        
        return True  # Toutes les cases non-bombes sont dévoilées

    def afficherGrille(self):
        for ligne in self.grille:
            print(" | ".join([str(case) for case in ligne]))
