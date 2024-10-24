class Case(object):
    def __init__(self, y, x, mine, devoilee, marquee, minesAdjacentes=0):
        """
        Constructeur de la classe Case.

        Parameters
        ----------
        x : int
            Position x de la case.
        y : int
            Position y de la case.
        mine : bool
            Etat permettant de savoir si la case contient une mine.
        devoilee : bool
            Permet de savoir si une case à déjà été dévoilée ou non.
        marquee : bool
            Permet de savoir si une case à déjà été marquée ou non.
        minesAdjacentes : int
            Nombre de mines présentes dans les cases adjacentes.
        """
        self.x = x
        self.y = y
        self.mine = mine
        self.devoilee = devoilee
        self.marquee = marquee
        self.minesAdjacentes = minesAdjacentes

    def calculerMinesAdjacentes(self, grille):
        """
        Calcule et met à jour le nombre de mines adjacentes à cette case.
        """
        voisins = self.getVoisins(grille)
        self.minesAdjacentes = sum(1 for voisin in voisins if voisin.mine)

    def getVoisins(self, grille):
        """
        Retourne une liste des cases voisines de cette case.

        Parameters
        ----------
        grille : list
            La grille entière (liste de listes) de cases.

        Returns
        -------
        voisins : list
            Une liste contenant les cases voisines.
        """
        voisins = []
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for dy, dx in directions:
            nx, ny = self.x + dx, self.y + dy
            if 0 <= nx < len(grille[0]) and 0 <= ny < len(grille):
                voisins.append(grille[ny][nx])
        return voisins

    def __str__(self):
        """
        Retourne une représentation de la case selon son état.
        """
        if self.devoilee:
            return str(self.minesAdjacentes)  # Case dévoilée
        elif self.marquee:
            return 'M'  # Case marquée
        else:
            return '■'  # Case ni dévoilée ni marquée

        
