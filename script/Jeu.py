# -*- coding: utf-8 -*-
import pygame
import sys
from pygame.locals import *
from Case import Case
from Grille import Grille

# Définition des dimensions pour chaque difficulté
DIFFICULTY_SETTINGS = {
    "facile": (9, 9),         # facile
    "intermediaire": (16, 16),  # 16x16
    "avance": (30, 16)       # 30x16
}

# Dimensions de la case
CASE_SIZE = 40
BANNER_HEIGHT = 120  # Hauteur du bandeau

class JeuDemineur:
    def __init__(self, difficulte="avance"):
        """
        Initialise une nouvelle partie du démineur avec la difficulté spécifiée.
        
        Paramètres
        ----------
        difficulte : str
            La difficulté du jeu, qui peut être "facile", "intermediaire" ou "avance".
        """
        pygame.init()
        self.difficulties = list(DIFFICULTY_SETTINGS.keys())
        self.selected_difficulty = self.difficulties.index(difficulte)
        
        # Dimensions de la grille
        self.largeur, self.longueur = DIFFICULTY_SETTINGS[difficulte]
        self.grille = Grille(difficulte)
        
        # Initialiser la fenêtre
        self.screen = pygame.display.set_mode((self.largeur * CASE_SIZE, self.longueur * CASE_SIZE + BANNER_HEIGHT))
        pygame.display.set_caption("Demineur")
        
        # Initialiser les couleurs
        self.colors = {
            "unrevealed": (50, 50, 50),  # Gris foncé
            "revealed_safe": (200, 200, 200),  # Gris clair
            "revealed_mine": (255, 0, 0),  # Rouge
            "marked": (255, 215, 0),  # Or
            "black": (0, 0, 0),
            "banner_bg": (70, 70, 70),  # Fond du bandeau
            "button_bg": (150, 150, 150),  # Fond des boutons
            "button_hover": (180, 180, 180),  # Fond des boutons au survol
            "text_color": (255, 255, 255)  # Texte blanc
        }
        
        self.font = pygame.font.SysFont("Helvetica", 24)
        
        # Charger l'image du drapeau
        self.flag_image = pygame.image.load("../images/drapeau.png")
        self.flag_image = pygame.transform.scale(self.flag_image, (30, 30))  # Redimensionner si nécessaire
        
        self.mine_image = pygame.image.load("../images/mine.png")
        self.mine_image = pygame.transform.scale(self.mine_image, (30, 30))  # Redimensionner si nécessaire
        
        self.flags_remaining = self.grille.drapeaux_restants
        
        # État du jeu
        self.game_active = True
        
        # Boutons
        self.reset_button_rect = pygame.Rect(10, 10, 120, 30)
        self.change_difficulty_button_rect = pygame.Rect(140, 10, 150, 30)

        # Boucle principale
        self.main_loop()

    def draw_board(self):
        """
        Dessine la grille de jeu sur l'écran.
        
        Affiche les cases, le bandeau et les boutons sur la fenêtre.
        """
        # Dessiner le fond de l'écran
        self.screen.fill((255, 255, 255))  # Remplir l'écran de blanc
    
        # Dessiner le bandeau
        self.draw_banner()
    
        # Afficher les cases
        for y in range(self.grille.longueur):
            for x in range(self.grille.largeur):
                case = self.grille.grille[y][x]
                rect = (x * CASE_SIZE, y * CASE_SIZE + BANNER_HEIGHT, CASE_SIZE, CASE_SIZE)
    
                if case.devoilee:
                    # Utiliser le fond des cases dévoilées
                    pygame.draw.rect(self.screen, self.colors["revealed_safe"], rect)
                    
                    if case.mine:
                        # Afficher l'image de la mine
                        self.screen.blit(self.mine_image, (x * CASE_SIZE + 5, y * CASE_SIZE + BANNER_HEIGHT + 5))
                    elif case.minesAdjacentes > 0:
                        # Afficher le nombre de mines adjacentes si non-mine
                        text = self.font.render(str(case.minesAdjacentes), True, self.colors["black"])
                        self.screen.blit(text, (x * CASE_SIZE + 10, y * CASE_SIZE + BANNER_HEIGHT + 5))
                elif case.marquee:
                    # Dessiner une case non dévoilée avec le drapeau
                    pygame.draw.rect(self.screen, self.colors["unrevealed"], rect)
                    self.screen.blit(self.flag_image, (x * CASE_SIZE + 5, y * CASE_SIZE + BANNER_HEIGHT + 5))
                else:
                    # Dessiner les cases non dévoilées en gris foncé
                    pygame.draw.rect(self.screen, self.colors["unrevealed"], rect)
    
                pygame.draw.rect(self.screen, self.colors["black"], rect, 1)

    def draw_banner(self):
        """
        Dessine le bandeau en haut de l'écran.
        
        Affiche les boutons et les informations de jeu telles que le mode de jeu et le nombre de drapeaux restants.
        """
        # Dessiner le bandeau
        pygame.draw.rect(self.screen, self.colors["banner_bg"], (0, 0, self.largeur * CASE_SIZE, BANNER_HEIGHT))
        
        # Afficher les boutons
        self.draw_buttons()

        # Afficher le mode de jeu et le nombre de drapeaux restants sous les boutons
        mode_text = self.font.render(f"Mode: {self.difficulties[self.selected_difficulty].capitalize()}", True, self.colors["text_color"])
        flags_text = self.font.render(f"Drapeaux: {self.flags_remaining}", True, self.colors["text_color"])
        
        # Positionner le texte sous les boutons
        self.screen.blit(mode_text, (10, 50))  # Position du texte du mode de jeu
        self.screen.blit(flags_text, (10, 80))  # Position du texte du nombre de drapeaux

    def draw_buttons(self):
        """
        Dessine les boutons sur le bandeau.
        
        Affiche les boutons de réinitialisation et de changement de difficulté.
        """
        # Dessiner les boutons
        pygame.draw.rect(self.screen, self.colors["button_bg"], self.reset_button_rect)
        reset_text = self.font.render("Reinitialiser", True, self.colors["text_color"])
        self.screen.blit(reset_text, (self.reset_button_rect.x + 10, self.reset_button_rect.y + 5))

        pygame.draw.rect(self.screen, self.colors["button_bg"], self.change_difficulty_button_rect)
        change_difficulty_text = self.font.render("Ch. Difficulte", True, self.colors["text_color"])
        self.screen.blit(change_difficulty_text, (self.change_difficulty_button_rect.x + 10, self.change_difficulty_button_rect.y + 5))

    def handle_left_click(self, pos):
        """
        Gère le clic gauche de la souris.
        
        Vérifie si le clic est sur un bouton ou sur une case de la grille, et effectue l'action appropriée.
        
        Paramètres
        ----------
        pos : tuple
            La position du clic sous forme de tuple (x, y).
        """
        x, y = pos
        if y < BANNER_HEIGHT:  # Vérifier si le clic est dans la zone des boutons
            if self.reset_button_rect.collidepoint(pos):
                self.reset()
            elif self.change_difficulty_button_rect.collidepoint(pos):
                self.changer_difficulte()
                self.reset()
        else:
            x //= CASE_SIZE
            y = (y - BANNER_HEIGHT) // CASE_SIZE  # Soustraire la hauteur du bandeau

            if 0 <= x < self.largeur and 0 <= y < self.longueur:
                self.clic_gauche(x, y)

    def handle_right_click(self, pos):
        """
        Gère le clic droit de la souris.
        
        Marque ou démarque une case en fonction de la position du clic.
        
        Paramètres
        ----------
        pos : tuple
            La position du clic sous forme de tuple (x, y).
        """
        x, y = pos
        x //= CASE_SIZE
        y = (y - BANNER_HEIGHT) // CASE_SIZE  # Soustraire la hauteur du bandeau

        if 0 <= x < self.largeur and 0 <= y < self.longueur:
            self.clic_droit(x, y)

    def clic_gauche(self, x, y):
        """
        Traite le clic gauche sur une case.
        
        Dévoile la case, révèle toutes les mines si c'est une mine, et vérifie si le joueur a gagné.
        
        Paramètres
        ----------
        x : int
            La position x de la case cliquée.
        y : int
            La position y de la case cliquée.
        """
        if self.grille.grille[y][x].marquee:
            return
        self.grille.devoiler_case(x, y)
        
        if self.grille.grille[y][x].mine:
            self.game_active = False
            self.grille.reveler_mines()  # Révéler toutes les mines
        elif self.grille.est_gagne():
            self.game_active = False  # Joueur a gagné
            self.grille.reveler_mines()

    def clic_droit(self, x, y):
        """
        Traite le clic droit sur une case.
        
        Marque ou démarque une case avec un drapeau.
        
        Paramètres
        ----------
        x : int
            La position x de la case cliquée.
        y : int
            La position y de la case cliquée.
        """
        case = self.grille.grille[y][x]
        if not case.devoilee:
            case.marquee = not case.marquee
            self.flags_remaining += -1 if case.marquee else 1

    def reset(self):
        """
        Réinitialise le jeu en créant une nouvelle grille avec la difficulté actuelle.
        """
        self.grille = Grille(self.difficulties[self.selected_difficulty])
        self.flags_remaining = self.grille.drapeaux_restants
        self.game_active = True

    def changer_difficulte(self):
        """
        Change la difficulté du jeu.
        
        Passe à la prochaine difficulté dans la liste définie.
        """
        self.selected_difficulty = (self.selected_difficulty + 1) % len(self.difficulties)

    def main_loop(self):
        """
        Boucle principale du jeu.
        
        Gère les événements et dessine l'état du jeu à chaque itération.
        """
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:  # Clic gauche
                        self.handle_left_click(event.pos)
                    elif event.button == 3:  # Clic droit
                        self.handle_right_click(event.pos)

            if self.game_active:
                self.draw_board()
            else:
                self.draw_board()  # Redessiner une dernière fois pour montrer la grille révélée
                pygame.display.update()  # Mettre à jour l'affichage
            
            pygame.display.update()

if __name__ == "__main__":
    JeuDemineur()
