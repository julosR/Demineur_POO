import random
from Case import Case

DIFFICULTE = {
    "facile": {"taille_grille": (9, 9), "nb_bombes": 10},
    "intermediaire": {"taille_grille": (16, 16), "nb_bombes": 40},
    "avance": {"taille_grille": (30, 16), "nb_bombes": 99},
    "surhomme": {"taille_grille": (50, 50), "nb_bombes": 500},
    "extraterrestre": {"taille_grille": (100, 100), "nb_bombes": 1000}
}

class Grille(object):
    def __init__(self, difficulte="facile"):
        """
        Constructeur de la classe Grille selon le mode de difficulté.

        Parameters
        ----------
        difficulte : str
            Mode de difficulté pour initialiser la taille de la grille et le nombre de bombes.
            Doit être une clé valide du dictionnaire DIFFICULTE.
        """
        if difficulte in DIFFICULTE:
            config = DIFFICULTE[difficulte]
            self.largeur, self.longueur = config["taille_grille"]
            self.nb_bombes = config["nb_bombes"]
        else:
            raise ValueError(f"Difficulté {difficulte} non reconnue.")
        
        self.grille = []
        self.bombes_initialisees = False
        self.initialiserGrille()

    def initialiserGrille(self):
        """
        Créer une grille remplie de cases.
        """
        self.grille = [
            [Case(x=x, y=y, mine=False, devoilee=False, marquee=False, minesAdjacentes=0)
             for x in range(self.largeur)]
            for y in range(self.longueur)
        ]

    def marquer(self, x, y):
        """
        Permet de marquer ou dé-marquer une case en fonction de ses coordonnées.

        Parameters
        ----------
        x : int
            Position x de la case.
        y : int
            Position y de la case.
        """
        if 0 <= x < self.largeur and 0 <= y < self.longueur:
            case = self.grille[y][x]
            case.marquee = not case.marquee
        else:
            print("Coordonnées hors limites !")
            
    def devoiler(self, x, y):
        """
        Permet de dévoiler une case en fonction de ses coordonnées.

        Parameters
        ----------
        x : int
            Position x de la case.
        y : int
            Position y de la case.
        """
        if 0 <= x < self.largeur and 0 <= y < self.longueur:
            case = self.grille[y][x]
            if not self.bombes_initialisees:
                case.devoilee = not case.devoilee
                self.placerBombes(x, y)
            else:
                case.devoilee = not case.devoilee
        else:
            print("Coordonnées hors limites !")
            
    def placerBombes(self, x_premier, y_premier):
        """
        Place aléatoirement des bombes dans la grille, en évitant la case initiale.
        """     
        positions_possibles = [(x, y) for x in range(self.largeur) for y in range(self.longueur)]
        positions_possibles.remove((x_premier, y_premier))  # Éviter la case initiale
        bombes = random.sample(positions_possibles, self.nb_bombes)

        for x, y in bombes:
            self.grille[y][x].mine = True

        # Calculer les mines adjacentes après avoir placé les bombes
        for ligne in self.grille:
            for case in ligne:
                case.calculerMinesAdjacentes(self.grille)    
                
        self.bombes_initialisees = True

    def afficherGrille(self):
        for ligne in self.grille:
            print(" | ".join([str(case) for case in ligne]))
