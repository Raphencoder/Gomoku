import pygame
import os
import sys
from menu import game_intro
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
                        pos = (int((x_player - 30)/38), int((y_player - 30)/38))
                        self.coordinate[pos] = self.current_player
                        self.check_hor_capture(pos[0], pos[1], 3)
                        # self.check_hor_capture(pos[0], pos[1], -3)
            
            elif event.type == pygame.QUIT:
                pygame.quit()
                quit()

    def check_hor_capture(self, x, y, i):
        # if x - i < 0 or x - i > 19:  #need to replace 20 by xmax
        #     return
        # elif self.coordinate[x - i, y] != self.current_player:
        #     return
        vert_min = [(0, 1), (0, 2)]
        vert_max = [(0, -1), (0, -2)]
        hor_min = [(0, 1), (0, 2)]
        hor_max = [(0, -1), (0, -2)]
        diag_min = [(1, 1), (2, 2)]
        diag_max = [(-1, -1), (-2, -2)]
        other_diag_min = [(-1, 1), (-2, 2)]
        other_diag_max = [(1, -1), (2, -2)]
        cord = {}
        index = ["vert_min", "vert_max", "hor_min", "hor_max", "diag_min", "diag_max", "other_diag_min", "other_diag_max"]
        cord["vert_min"] = vert_min
        cord["vert_max"] = vert_max
        cord["hor_min"] = hor_min
        cord["hor_max"] = hor_max
        cord["diag_min"] = diag_min
        cord["diag_max"] = diag_max
        cord["other_diag_min"] = other_diag_min
        cord["other_diag_max"] = other_diag_max
        points = {}
        to_add_y = -2
        for e in range(5):
            to_add_x = -2
            for i in range(5):
                if (abs(to_add_x) == 1 and abs(to_add_y) == 2) or (abs(to_add_x) == 2 and abs(to_add_y) == 1):
                    to_add_x += 1
                    continue
                des_x = float((x + to_add_x) * 38 + 30)
                des_y = float((y + to_add_y) * 38 + 30)
                pygame.draw.rect(self.window, (0, 0, 0), (des_x - 10, des_y - 10, 20, 20), 2) # largeur
                pos = self.coordinate[x + to_add_x, y + to_add_y]
                if pos != -1 and pos != self.current_player:
                    for name in index:
                        if (to_add_x, to_add_y) in cord[name]:
                            try:
                                points[name] += 1 
                            except KeyError:
                                points[name] = 1
                to_add_x += 1
            to_add_y += 1
        pygame.display.flip()
        print(points)
        if i > 0:
            pos1 =  self.coordinate[x - i + 1, y]
            pos2 = self.coordinate[x - i + 2, y]
            sup1 = [x - i + 1, y]
            sup2 = [x - i + 2, y]
        else:
            pos1 =  self.coordinate[x - i - 1, y]
            pos2 = self.coordinate[x - i - 2, y]
            sup1 = [x - i - 1, y]
            sup2 = [x - i - 2, y]
        if pos1 != -1 and pos2 != -1 and pos1 != self.current_player and pos2 != self.current_player:
            self.capture(sup1, sup2)
        else:
            return

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
        self.pos_player.remove(newpos2)


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
