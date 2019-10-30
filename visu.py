import pygame
import os
import sys 

window = pygame.display.set_mode((800, 800))
pygame.display.set_caption("gomoku")
fps = pygame.time.Clock()
score = 0
image = pygame.image.load("joueur-blanc.png").convert_alpha()

"""
TODO : 
    * Ne pas permettre l'ajout de joueur sur le bord de la map
    * Rajouter une class qui dis si le joueur peut placer son pion a cet endroit
"""

def in_inter(pos, inters):
    """
    Check if the position is inside rectangle of intersection
    """
    for tup in inters:
        if (pos[0] >= tup[0] and pos[0] <= tup[2])\
            and (pos[1] >= tup[1] and pos[1] <= tup[3]):
            return tup[0] + 10, tup[1] + 10
    return 0, 0


pos_player = []

while True:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            try:
                # if in_inter return positions x_player and y_player are the
                # position where the user wants to put his player
                x_player, y_player = in_inter(pos, inters)
                if x_player != 0 and y_player != 0:
                    pos_player.append(((x_player,) + (y_player,)))
            except NameError:
                pass
    # background
    window.fill(pygame.Color(243, 210, 132))
    pygame.draw.rect(window, (0, 0, 0), (30, 30, 730, 730), 2)
    L = 700
    # 14 carrés par colonnes et par lignes
    nb_square = range(14)
    size_square = int(L / 14) + 6
    square = range(size_square)
    for i in nb_square:
        cube_pos = size_square * i
        pygame.draw.line(window, (0, 0, 0), (30, 30 + cube_pos), (730 + 30, 30 + cube_pos), 1) # largeur
        pygame.draw.line(window, (0, 0, 0), (30 + cube_pos, 30), (30 + cube_pos, 730 + 30), 1) # longueur
    
    # methode qui permet de recuperer la postition x,y de chaque intersection
    y = 30
    inters = []
    for i in range(14):
        x = 30
        for l in range(14):
            square_inter_start = (x - 30, y - 30)
            square_inter_end = (x + 30, y + 30)
            square_inter = square_inter_start + square_inter_end
            inters.append(square_inter)
            x += 56
        y += 56
    
    # Affiche les pions
    for elem in pos_player:
        window.blit(image, (elem[0], elem[1]))
    pygame.display.flip()
