import pygame
import os
import sys
from menu import game_intro
# from variables import inters
import time


"""
TODO :
    * Ne pas permettre l'ajout de joueur sur le bord de la map
    * timer
"""

yellow = (243, 210, 132)

def in_inter(pos, inters):
    """
    Check if the position is inside rectangle of intersection
    """
    for tup in inters:
        if (pos[0] >= tup[0] and pos[0] <= tup[2])\
            and (pos[1] >= tup[1] and pos[1] <= tup[3]):
            return (tup[0] + 10), (tup[1] + 10)
    return 0, 0


def get_inter(nb_square, gomoku):
    inters = []
    size = 700 + nb_square
    while size % nb_square != 0:
        size += 1
    size_square = (size / nb_square)
    y = 30
    for i in range(nb_square + 1):
        x = 30
        for l in range(nb_square + 1):
            square_inter_start = (x - 10, y - 10)
            square_inter_end = (x + 10, y + 10)
            square_inter = square_inter_start + square_inter_end
            # allow to see the click point
            # pygame.draw.rect(gomoku.window, (0, 0, 0), (x - 10, y - 10, 20, 20), 2) # largeur
            inters.append(square_inter)
            x += size_square 
        y += size_square 
    return inters

def get_coordinate(nb_square):
    cord = []
    for x in range(nb_square + 1):
        for y in range(nb_square + 1):
            cord.append([x, y, -1])
    return cord



class Gomoku():

    def __init__(self, ai_mode):
        pygame.init()
        self.window = pygame.display.set_mode((800, 800))
        pygame.display.set_caption("gomoku")
        self.img_player_one = pygame.image.load("./ressources/joueur-blanc-petit.png").convert_alpha()
        self.img_player_two = pygame.image.load("./ressources/joueur-noir-petit.png").convert_alpha()
        self.pos_player = []
        self.coordinate = []
        self.ai_mode = ai_mode
        self.current_player = 1

    def can_place(self, x, y):
        if ((x,) + (y,) + (1,)) in self.pos_player or ((x,) + (y,) + (2,)) in self.pos_player:
            return False
        # need to add rule of the game if can be place or no
        else:
            if self.current_player == 1:
                self.current_player = 2
            else:
                self.current_player = 1
            return True

    def check_event(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and (not self.ai_mode or self.current_player == 1):
                pos = pygame.mouse.get_pos()
                x_player, y_player = in_inter(pos, self.inters)
                if x_player != 0 and y_player != 0:
                    if self.can_place(x_player, y_player):
                        self.pos_player.append(((x_player,) + (y_player,) + (self.current_player,)))
                        pos = [int((x_player - 10)/38), int((y_player - 10)/38), -1]
                        i = self.coordinate.index(pos)
                        self.coordinate[i][2] = self.current_player
                        print (self.coordinate[i])


            elif event.type == pygame.QUIT:
                pygame.quit()
                quit()


    def fill_background(self, nb_square):
        self.window.fill(yellow)
        size = 700 + nb_square
        while size % nb_square != 0:
            size += 1
        pygame.draw.rect(self.window, (0, 0, 0), (30, 30, size, size), 2)
        size_square = size / nb_square
        for i in range(nb_square):
            cube_pos = (size_square * i)
            pygame.draw.line(self.window, (0, 0, 0), (30, 30 + cube_pos), (size + 30, 30 + cube_pos), 1) # largeur
            pygame.draw.line(self.window, (0, 0, 0), (30 + cube_pos, 30), (30 + cube_pos, size + 30), 1) # longueur

    def display_player(self):
        for elem in self.pos_player:
            if elem[2] == 1:
                self.window.blit(self.img_player_one, (elem[0] - 12, elem[1] - 12))
            else:
                self.window.blit(self.img_player_two, (elem[0] - 12, elem[1] - 12))
        pygame.display.flip()



def start_game():
    
    pygame.init()
    ai_mode = game_intro(pygame.display.set_mode((800, 800)))
    pygame.quit()
    nb_square = 19
    gomoku = Gomoku(ai_mode)

    gomoku.coordinate = get_coordinate(nb_square)
    gomoku.inters = get_inter(nb_square, gomoku)
    while True:
        gomoku.check_event()
        gomoku.display_player()
        gomoku.fill_background(nb_square)



start_game()
