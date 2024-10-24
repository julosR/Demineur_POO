import random
from Case import Case

DIFFICULTE = {
    "facile": {"taille_grille": (9, 9), "nb_bombes": 10, "taille_zone_safe": (2, 4)},
    "intermediaire": {"taille_grille": (16, 16), "nb_bombes": 40, "taille_zone_safe": (5, 10)},
    "avance": {"taille_grille": (30, 16), "nb_bombes": 99, "taille_zone_safe": (10, 20)},
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
            self.taille_zone_safe_min, self.taille_zone_safe_max = config["taille_zone_safe"]
        else:
            raise ValueError(f"Difficulté {difficulte} non reconnue.")
        
        self.grille = []
        self.bombes_initialisees = False
        self.nb_cases_non_bombes = 0  
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
        self.nb_cases_non_bombes = self.largeur * self.longueur - self.nb_bombes

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
            if not case.devoilee:
                case.marquee = not case.marquee
        else:
            print("Coordonnées hors limites !")

    def devoiler(self, x, y):
        """
        Permet de dévoiler une case en fonction de ses coordonnées.
        Si la case dévoilée a 0 bombes adjacentes, les cases adjacentes sont dévoilées également.
        
        Parameters
        ----------
        x : int
            Position x de la case.
        y : int
            Position y de la case.
        """
        if (0 <= x < self.largeur and 0 <= y < self.longueur):
            case = self.grille[y][x]
            
            # Si les bombes ne sont pas encore initialisées
            if not self.bombes_initialisees:
                # Placer les bombes autour de la case initiale
                self.placerBombes(x, y)
                # Dévoiler la zone safe
                self.devoilerCasesAdjacentes(x, y)
            else:
                # Si la case n'est pas déjà dévoilée et n'est pas marquée
                if not case.devoilee and not case.marquee:
                    case.devoilee = True
                    
                    # Si la case n'a aucune mine adjacente, on dévoile les cases adjacentes
                    if case.minesAdjacentes == 0:
                        self.devoilerCasesAdjacentes(x, y)

    def devoilerCasesAdjacentes(self, x, y):
        """
        Dévoile récursivement toutes les cases adjacentes à une case donnée
        si cette case n'a aucune mine adjacente (minesAdjacentes == 0).
        
        Parameters
        ----------
        x : int
            Position x de la case.
        y : int
            Position y de la case.
        """
        pile = [(x, y)]
        deja_visitees = set()
    
        while pile:
            cx, cy = pile.pop()
    
            # Vérifiez si la case est dans les limites et pas déjà visitée
            if (cx, cy) not in deja_visitees and 0 <= cx < self.largeur and 0 <= cy < self.longueur:
                case = self.grille[cy][cx]
                deja_visitees.add((cx, cy))
    
                if not case.devoilee:
                    case.devoilee = True
    
                    # Si la case a 0 mines adjacentes, ajouter ses cases adjacentes à la pile
                    if case.minesAdjacentes == 0:
                        for dx in range(-1, 2):
                            for dy in range(-1, 2):
                                if dx == 0 and dy == 0:
                                    continue  # Ignorer la case elle-même
                                nx, ny = cx + dx, cy + dy
                                # Ajouter les coordonnées de la case adjacente à la pile si elles sont dans les limites
                                if 0 <= nx < self.largeur and 0 <= ny < self.longueur:
                                    pile.append((nx, ny))

    def placerBombes(self, x_premier, y_premier):
        positions_possibles = [(x, y) for x in range(self.largeur) for y in range(self.longueur)]
        
        zone_safe = set()
        zone_safe.add((x_premier, y_premier))
        
        # Déterminer la taille de la zone safe en fonction de la difficulté
        if self.nb_bombes == 10:  # facile
            taille_zone_safe = random.randint(1, 2)  # Plus petit pour facile
        elif self.nb_bombes == 40:  # intermédiaire
            taille_zone_safe = random.randint(3, 5)  # Moyen pour intermédiaire
        elif self.nb_bombes == 99:  # avancé
            taille_zone_safe = random.randint(6, 10)  # Plus grand pour avancé
        else:
            taille_zone_safe = 1  # Valeur par défaut, si besoin
    
        # Propagation de la zone safe à partir de la case initiale
        cases_a_traiter = [(x_premier, y_premier)]
        while len(zone_safe) < taille_zone_safe and cases_a_traiter:
            x, y = cases_a_traiter.pop(0)
            
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    if dx == 0 and dy == 0:
                        continue  # Ignorer la case elle-même
                    nx, ny = x + dx, y + dy
                    
                    if 0 <= nx < self.largeur and 0 <= ny < self.longueur:
                        case_adjacent = self.grille[ny][nx]
                        if case_adjacent.minesAdjacentes == 0 and (nx, ny) not in zone_safe:
                            zone_safe.add((nx, ny))
                            cases_a_traiter.append((nx, ny))
                            
                            if len(zone_safe) >= taille_zone_safe:
                                break
            
            if len(zone_safe) >= taille_zone_safe:
                break
    
        for position in zone_safe:
            if position in positions_possibles:
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

    def afficherGrille(self):
        """
        Affiche la grille de manière textuelle.
        """
        for ligne in self.grille:
            print(" | ".join([str(case) for case in ligne]))
