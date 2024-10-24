from Case import Case
from Grille import Grille
import tkinter as tk
from tkinter import messagebox

class SelectionDifficulte:
    def __init__(self, root):
        self.root = root
        self.root.title("Choisissez la difficulté")
        
        self.difficulties = ["facile", "intermediaire", "avance"]
        self.selected_difficulty = tk.StringVar(value=self.difficulties[0])  # Difficulté par défaut
        
        self.creerInterface()

    def creerInterface(self):
        tk.Label(self.root, text="Choisissez la difficulté :").pack(pady=10)

        for difficulte in self.difficulties:
            tk.Radiobutton(self.root, text=difficulte.capitalize(), variable=self.selected_difficulty,
                           value=difficulte).pack(anchor=tk.W)

        tk.Button(self.root, text="Démarrer le jeu", command=self.lancerJeu).pack(pady=20)

    def lancerJeu(self):
        self.root.destroy()  # Fermer la fenêtre de sélection de difficulté
        root = tk.Tk()
        jeu = JeuDemineur(root, self.selected_difficulty.get())
        root.mainloop()

class JeuDemineur:
    def __init__(self, root, difficulte="facile"):
        self.grille = Grille(difficulte)  # Votre classe Grille
        self.root = root
        self.root.title("Démineur")
        self.boutons = [[None for _ in range(self.grille.largeur)] for _ in range(self.grille.longueur)]
        self.creerInterface()

    def creerInterface(self):
        for y in range(self.grille.longueur):
            for x in range(self.grille.largeur):
                bouton = tk.Button(self.root, width=3, height=1,
                                   command=lambda x=x, y=y: self.clicGauche(x, y))
                bouton.bind("<Button-3>", lambda event, x=x, y=y: self.clicDroit(event, x, y))
                bouton.grid(row=y, column=x)
                self.boutons[y][x] = bouton

    def clicGauche(self, x, y):
        # Vérifiez si la case est marquée
        if self.grille.grille[y][x].marquee:
            return  # Ne pas dévoiler la case si elle est marquée
        
        # Dévoiler la case
        self.grille.devoiler(x, y)
        self.mettreAJourInterface()
        
        # Vérifiez si la partie est perdue ou gagnée
        if self.grille.grille[y][x].mine:
            messagebox.showinfo("Fin du jeu", "Vous avez perdu !")
            self.root.quit()  # Ferme l'application

    def clicDroit(self, event, x, y):
        # Marquer ou dé-marquer la case
        self.grille.marquer(x, y)
        self.mettreAJourInterface()

    def mettreAJourInterface(self):
        for y in range(self.grille.longueur):
            for x in range(self.grille.largeur):
                case = self.grille.grille[y][x]
                if case.devoilee:
                    if case.mine:
                        self.boutons[y][x].config(text="*", bg="red")
                    else:
                        self.boutons[y][x].config(text=str(case.minesAdjacentes), bg="lightgrey")
                elif case.marquee:
                    self.boutons[y][x].config(text="!", bg="yellow")
                else:
                    self.boutons[y][x].config(text="", bg="SystemButtonFace")


if __name__ == "__main__":
    root = tk.Tk()
    selection = SelectionDifficulte(root)
    root.mainloop()
