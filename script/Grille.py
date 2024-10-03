from Case import Case

class Grille(object):
    def __init__(self, largeur, longueur):
        """
        Constructeur de la classe Grille.

        ----------
        largeur : int
            Largeur de la grille (nombre de colonnes).
        longueur : int
            Longueur de la grille (nombre de lignes).
        """
        self.largeur = largeur
        self.longueur = longueur
        self.grille = []
        self.initialiserGrille()

    def initialiserGrille(self):
        """
        Créer une grille remplie de case
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


    def afficherGrille(self):
        for ligne in self.grille:
            print(" | ".join([str(case) for case in ligne]))
    
    
    