import pygame
import os
import sys
from menu import game_intro, text_objects
from random import *
from variables import cord, index, new_rules
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
    cord = {}
    for x in range(nb_square + 1):
        for y in range(nb_square + 1):
            cord[x, y] = -1
    return cord

class Gomoku():

    def __init__(self, ai_mode, j1, j2):
        pygame.init()
        self.window = pygame.display.set_mode((800, 800))
        pygame.display.set_caption("gomoku")
        self.img_player_one = pygame.image.load("./ressources/joueur-blanc-petit.png").convert_alpha()
        self.img_player_two = pygame.image.load("./ressources/joueur-noir-petit.png").convert_alpha()
        self.pos_player = []
        self.coordinate = []
        self.ai_mode = ai_mode
        self.current_player = 1
        self.time_clock = pygame.time.Clock()

    def change_player(self):
        if self.current_player == 1:
            self.current_player = 2
        else:
            self.current_player = 1

    def can_place(self, x, y):
        if ((x,) + (y,) + (1,)) in self.pos_player or ((x,) + (y,) + (2,)) in self.pos_player:
            return False
        print(self.ally)
        print(self.enemy)
        # for key, value in free_threes.items():
        #     try:
        #         if self.ally[value[0]] >= 2 and self.ally[value[1]] >= 2:
        #             if value[0] in list(self.enemy.keys()) or \
        #                 value[1] in list(self.enemy.keys()) or \
        #                 value[2] in list(self.enemy.keys()) or \
        #                 value[3] in list(self.enemy.keys()):
        #                 return True
        #             self.change_player()
        #             return False
        #     except KeyError:
        #         pass
        # return True
        for key, value in new_rules.items():
            try:
                print("in")
                print(self.ally[key])
                print(key)
                if self.ally[key] >= 2: 
                    for pos in value:
                        try:
                            if self.ally[pos] >= 2 and ("three_"+pos+"" in list(self.enemy.keys()) or "three_"+key+"" in list(self.enemy.keys())):
                                print("return True")
                                return True
                            elif self.ally[pos] >= 2:
                                self.change_player()
                                print("return False")
                                return False
                        except KeyError:
                            pass
            except KeyError:
                print("out")
                pass
        return True
    def check_event(self, j1, j2):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and (not self.ai_mode or self.current_player == 1):
                pos = pygame.mouse.get_pos()
                x_player, y_player = in_inter(pos, self.inters)
                if x_player != 0 and y_player != 0:
                    pos = (int((x_player - 30)/38), int((y_player - 30)/38))
                    self.change_player()
                    self.map_players(pos[0], pos[1])
                    if self.can_place(x_player, y_player):
                        self.pos_player.append(((x_player,) + (y_player,) + (self.current_player,)))
                        pos = (int((x_player - 30)/38), int((y_player - 30)/38))
                        self.coordinate[pos] = self.current_player
                        self.check_hor_capture(pos[0], pos[1])
                        self.time_clock.tick()
            elif event.type == pygame.QUIT:
                pygame.quit()
                quit()

    def add_enemy(self, x, y):
        """
        Add points to the corresponding direction
        """
        for name in index:
            if (x, y) in cord[name]:
                try:
                    self.enemy[name] += 1 
                except KeyError:
                    self.enemy[name] = 1
    
    def add_ally(self, x, y):
        for name in index:
            if (x, y) in cord[name]:
                try:
                    self.ally[name] += 1 
                except KeyError:
                    self.ally[name] = 1


    def map_players(self, x, y):
        """
        Map all the neighbourgs of the given position in the 8 differents directions
        """
        self.enemy = {}
        self.ally = {}
        to_add_y = -4
        for e in range(9):
            to_add_x = -4
            for i in range(9):
                print(to_add_x, to_add_y)
                if (abs(to_add_x) == 1 and abs(to_add_y) == 2) or (abs(to_add_x) == 2 and abs(to_add_y) == 1):
                    """
                    only this coordonates
                    o    o   o
                       o o o
                    o  o x o o
                       o o o 
                    o    o   o

                    """
                    to_add_x += 1
                    continue
                try:
                    pos = self.coordinate[x + to_add_x, y + to_add_y]
                except KeyError:
                    # Outside the map
                    to_add_x += 1                    
                    continue
                if pos != -1 and pos != self.current_player:
                    self.add_enemy(to_add_x, to_add_y)
                elif pos != -1 and pos == self.current_player:
                    self.add_ally(to_add_x, to_add_y)
                to_add_x += 1
            to_add_y += 1
    
    def check_hor_capture(self, x, y):
        # Take the values where they were 2 enemys on the row
        to_capture = [key for key, value in self.enemy.items() if value == 2]
        if to_capture:
            for elem in to_capture:
                try:
                    # Take the position of the x - 3 player 
                    print("=-=-=-=-=- DEBUG =-=-=-=-=-=-=-")
                    print("elem", elem)
                    print("cord", cord)
                    print("x", x)
                    print("y", y)

                    print("cord[elem][2][0]", cord[elem][2][0])
                    print("x + cord[elem][2][0]", x + cord[elem][2][0])
                    print("y + cord[elem][2][1]", y + cord[elem][2][1])
                    print("self.coordinate[x + cord[elem][2][0], y + cord[elem][2][1]]", self.coordinate[x + cord[elem][2][0], y + cord[elem][2][1]])
                    print("=-=-=-=-=-=- END DEBUG =-=-=-=-=")
                    pos = self.coordinate[x + cord[elem][2][0], y + cord[elem][2][1]]
                except (KeyError, IndexError):
                    # Outside the map or on free threes
                    continue
                sup1 = [x + cord[elem][0][0], y + cord[elem][0][1]]
                sup2 = [x + cord[elem][1][0], y + cord[elem][1][1]]
                if pos != -1 and pos == self.current_player:
                    self.capture(sup1, sup2)

    def capture(self, pos1, pos2):
        """
        need a few change when class Player will be implemented
        """
        newpos1 = [float(i * 38 + 30)  for i in pos1]
        newpos2 = [float(i * 38 + 30) for i in pos2]
        if self.current_player == 1:
            newpos1.append(2)
            newpos2.append(2)
        if self.current_player == 2:
            newpos1.append(1)
            newpos2.append(1)
        newpos1 = tuple(newpos1)
        newpos2 = tuple(newpos2)
        self.pos_player.remove(newpos1)
        pos1 = tuple(pos1)
        self.coordinate[pos1] = -1
        self.pos_player.remove(newpos2)
        pos2 = tuple(pos2)
        self.coordinate[pos2] = -1


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
        #timer display
        pygame.draw.rect(self.window, (0,0,0),(650,760,150,50), 1)
        smallText = pygame.font.Font("freesansbold.ttf",12)
        textSurf, textRect = text_objects(str(self.time_clock.get_rawtime()/1000) + " seconds", smallText)
        textRect.center = ((650+(150/2)), (750+(50/2)))
        self.window.blit(textSurf, textRect)

    def display_player(self):
        for elem in self.pos_player:
            if elem[2] == 1:
                self.window.blit(self.img_player_one, (elem[0] - 12, elem[1] - 12))
            else:
                self.window.blit(self.img_player_two, (elem[0] - 12, elem[1] - 12))
        pygame.display.flip()

class Player():

    def __init__(self, id_player, ai=False):
        self.ai = ai
        self.capture = 0
        self.alignement = 0
        self.id_player = id_player


def start_game():

    pygame.init()
    ai_mode = game_intro(pygame.display.set_mode((800, 800)))
    pygame.quit()
    nb_square = 19
    if not ai_mode:
        j1 = Player(1)
        j2 = Player(2)
    else:
        j1 = Player(1, True) #randomize later with randint
        j2 = Player(2)
    gomoku = Gomoku(ai_mode, j1, j2)

    gomoku.coordinate = get_coordinate(nb_square)
    gomoku.inters = get_inter(nb_square, gomoku)
    while True:
        gomoku.check_event(j1,j2)
        gomoku.display_player()
        gomoku.fill_background(nb_square)

start_game()
