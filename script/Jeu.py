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
            "unrevealed": (50, 50, 50),  # Dark gray
            "revealed_safe": (200, 200, 200),  # Light gray
            "revealed_mine": (255, 0, 0),  # Red
            "marked": (255, 215, 0),  # Gold
            "black": (0, 0, 0),
            "banner_bg": (70, 70, 70),  # Dark banner background
            "button_bg": (150, 150, 150),  # Button background
            "button_hover": (180, 180, 180),  # Button hover background
            "text_color": (255, 255, 255)  # White text
        }
        # Couleurs pour les chiffres des mines adjacentes
        self.adjacent_colors = {
            1: (0, 0, 255),       # 1 - Bleu
            2: (0, 128, 0),       # 2 - Vert
            3: (255, 0, 0),       # 3 - Rouge
            4: (0, 0, 128),       # 4 - Bleu foncé
            5: (128, 0, 0),       # 5 - Marron
            6: (64, 224, 208),    # 6 - Turquoise
            7: (0, 0, 0),         # 7 - Noir
            8: (128, 128, 128)    # 8 - Gris
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
                        text_color = self.adjacent_colors.get(case.minesAdjacentes, self.colors["black"])
                        text = self.font.render(str(case.minesAdjacentes), True, text_color)
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
        # Dessiner les boutons
        pygame.draw.rect(self.screen, self.colors["button_bg"], self.reset_button_rect)
        reset_text = self.font.render("Reinitialiser", True, self.colors["text_color"])
        self.screen.blit(reset_text, (self.reset_button_rect.x + 10, self.reset_button_rect.y + 5))

        pygame.draw.rect(self.screen, self.colors["button_bg"], self.change_difficulty_button_rect)
        change_difficulty_text = self.font.render("Ch. Difficulte", True, self.colors["text_color"])
        self.screen.blit(change_difficulty_text, (self.change_difficulty_button_rect.x + 10, self.change_difficulty_button_rect.y + 5))

    def handle_left_click(self, pos):
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
        x, y = pos
        x //= CASE_SIZE
        y = (y - BANNER_HEIGHT) // CASE_SIZE  # Soustraire la hauteur du bandeau

        if 0 <= x < self.largeur and 0 <= y < self.longueur:
            self.clic_droit(x, y)

    def clic_gauche(self, x, y):
        if self.grille.grille[y][x].marquee:
            return
        self.grille.devoiler(x, y)
        
        if self.grille.grille[y][x].mine:
            self.reveal_all_mines()
            self.game_over()
        elif self.grille.verifier_gagne():  # Vérifier si le joueur a gagné
            self.reveal_all_mines(victory=True)  # Révéler toutes les mines avec le flag de victoire
        self.draw_board()  # Redessiner la grille après un clic

    def clic_droit(self, x, y):
        self.grille.marquer(x, y)
        self.flags_remaining = self.grille.drapeaux_restants
        self.draw_board()  # Redessiner après avoir marqué/démarquée

    def reveal_all_mines(self, victory=False):
        # Révéler toutes les mines
        for y in range(self.grille.longueur):
            for x in range(self.grille.largeur):
                if self.grille.grille[y][x].mine:
                    self.grille.grille[y][x].devoilee = True  # Révéler la mine
        
        # Redessiner la grille pour afficher les mines
        self.draw_board()
        pygame.display.flip()  # Mettre à jour l'affichage avant d'afficher le pop-up
    
        # Afficher le message de fin de partie
        if victory:
            self.show_popup("Félicitations", "Vous avez gagné !")  # Afficher le pop-up de victoire
        else:
            self.show_popup("Fin de Partie", "Vous avez perdu !")
        
        # Désactiver le jeu pour empêcher toute autre interaction
        self.game_active = False


    def game_over(self):
        self.game_active = False  # Désactiver les clics sur la grille
        self.show_popup("Fin de Partie", "Vous avez perdu !")  # Afficher un pop-up à la fin de la partie

    def show_popup(self, title, message):
        # Créer une nouvelle fenêtre pour le pop-up
        popup_surface = pygame.Surface((400, 200))
        popup_surface.fill((200, 200, 200))
        pygame.draw.rect(popup_surface, (0, 0, 0), (0, 0, 400, 200), 2)

        title_text = self.font.render(title, True, (0, 0, 0))
        message_text = self.font.render(message, True, (0, 0, 0))
        popup_surface.blit(title_text, (50, 20))
        popup_surface.blit(message_text, (50, 80))

        self.screen.blit(popup_surface, (self.largeur * CASE_SIZE // 2 - 200, self.longueur * CASE_SIZE // 2 - 100))
        pygame.display.flip()

        # Attendre que l'utilisateur clique pour fermer le pop-up
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    waiting = False

    def reset(self):
        self.grille = Grille(self.difficulties[self.selected_difficulty])  # Réinitialiser la grille
        self.flags_remaining = self.grille.drapeaux_restants  # Réinitialiser le nombre de drapeaux
        self.game_active = True  # Réactiver le jeu

    def changer_difficulte(self):
        self.selected_difficulty = (self.selected_difficulty + 1) % len(self.difficulties)
        self.largeur, self.longueur = DIFFICULTY_SETTINGS[self.difficulties[self.selected_difficulty]]
        self.grille = Grille(self.difficulties[self.selected_difficulty])  # Réinitialiser la grille
        self.flags_remaining = self.grille.drapeaux_restants  # Réinitialiser le nombre de drapeaux
        self.draw_board()  # Redessiner la grille

    def main_loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    # Toujours vérifier les clics sur les boutons
                    if event.button == 1:  # Clic gauche
                        if self.reset_button_rect.collidepoint(event.pos):
                            self.reset()
                        elif self.change_difficulty_button_rect.collidepoint(event.pos):
                            self.changer_difficulte()
                            self.reset()
                        else:
                            if self.game_active:
                                self.handle_left_click(event.pos)
                    elif event.button == 3:  # Clic droit
                        if self.game_active:
                            self.handle_right_click(event.pos)
    
            # Redessiner la grille seulement si le jeu est actif
            if self.game_active:
                self.draw_board()  # Redessiner la grille si le jeu est actif
    
            # Toujours redessiner le bandeau, y compris les boutons
            self.draw_board()  # Cela inclut le bandeau, donc pas besoin de l'appeler à chaque fois
    
            pygame.display.flip()

if __name__ == "__main__":
    JeuDemineur()
