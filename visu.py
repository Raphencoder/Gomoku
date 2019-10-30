import pygame
import os
import sys
from menu import game_intro
from variables import inters
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
            return tup[0] + 10, tup[1] + 10
    return 0, 0


def get_inter():
    y = 30
    inters = []
    for i in range(14):
        x = 30
        for l in range(14):
            square_inter_start = (x - 30, y - 30)
            square_inter_end = (x + 30, y + 30)
            square_inter = square_inter_start + square_inter_end
            inters.append(square_inter)
            x += 52
        y += 52
    return inters




class Gomoku():

    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((800, 800))
        pygame.display.set_caption("gomoku")
        self.img_player_one = pygame.image.load("joueur-blanc.png").convert_alpha()
        self.img_player_two = pygame.image.load("joueur-noir.png").convert_alpha()
        self.inters = inters
        self.pos_player = []
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
                x_player, y_player = in_inter(pos, inters)
                if x_player != 0 and y_player != 0:
                    if self.can_place(x_player, y_player):
                        self.pos_player.append(((x_player,) + (y_player,) + (self.current_player,)))

    def fill_background(self):
        self.window.fill(yellow)
        pygame.draw.rect(self.window, (0, 0, 0), (30, 30, 730, 730), 2)
        L = 700
        nb_square = range(15)
        size_square = int(L / max(nb_square) + 2)
        square = range(size_square)
        for i in nb_square:
            cube_pos = size_square * i
            pygame.draw.line(self.window, (0, 0, 0), (30, 30 + cube_pos), (730 + 30, 30 + cube_pos), 1) # largeur
            pygame.draw.line(self.window, (0, 0, 0), (30 + cube_pos, 30), (30 + cube_pos, 730 + 30), 1) # longueur

    def display_player(self):
        for elem in self.pos_player:
            if elem[2] == 1:
                self.window.blit(self.img_player_one, (elem[0], elem[1]))
            else:
                self.window.blit(self.img_player_two, (elem[0], elem[1]))
        pygame.display.flip()


def start_game():
    gomoku = Gomoku()
    gomoku.init = True
    while True:
        if gomoku.init:
            gomoku.ai_mode = game_intro(gomoku.window)
            gomoku.init = False
        gomoku.check_event()
        gomoku.fill_background()
        gomoku.display_player()

start_game()