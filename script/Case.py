class Case(object):
    def __init__(self,y,x,mine,devoilee,marquee,minesAdjacentes):
        """
        
        Constructeur de la classe jeu
        
        ----------
        x : int
            position x de la case.
        y : int
            position y de la case.
        mine : bool
            Etat permettant de savoir si la case contient une mine.
        devoilee : bool
            Permet de savoir si une case à déjà été dévoilée ou non.
        marquee : bool
            Permet de savoir si une case à déjà été marquée ou non.
        minesAdjacentes : int
            renseigne sur le nombre de bombes présentes dans les cases
            adjacentes à la case étudiée.

        -------


        """
        self.x = x
        self.y = y
        self.mine = mine
        self.devoilee = devoilee
        self.marquee = marquee
        self.minesAdjacentes = minesAdjacentes
        
        
        
    def marquer(self,case):
        case.marquee = not(case.marquee)
    
    def __str__(self):
        return f'Case(x = {self.x}, y = {self.y}, mine = {self.mine}, devoilee = {self.devoilee}, marquee = {self.marquee}, minesAdjacentes = {self.minesAdjacentes}'