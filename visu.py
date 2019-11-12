import pygame
import os
import sys
from menu import game_intro, text_objects, button
from random import *
from variables import cord, index, new_rules, oposite
import time


"""
TODO :
    * Victory rules
    * Free three bug
"""

yellow = (243, 210, 132)

notcur_p = lambda x, y , z : y if x != y else z

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
        self.current_player = 2
        self.time_clock = pygame.time.Clock()
        if ai_mode:
            self.j1, self.j2 = Player(1, True), Player(2)
        else:
            self.j1, self.j2 = Player(1), Player(2)

    def change_player(self):
        if self.current_player == 1:
            self.current_player = 2
        else:
            self.current_player = 1

    def is_free(self, x, y, coordonates):
        to_add_x = coordonates[1][0] - coordonates[0][0]
        to_add_y = coordonates[1][1] - coordonates[0][1]
        pos_x = x
        pos_y = y
        while self.coordinate[pos_x, pos_y] == -1:
            pos_x += to_add_x
            pos_y += to_add_y        
        try:
            while self.coordinate[pos_x, pos_y] == self.current_player:
                pos_x += to_add_x
                pos_y += to_add_y
        except KeyError:
            print("outside map")
            print(pos_x, pos_y)
            return False
        if self.coordinate[pos_x, pos_y] == -1:
            print("this is free")
            return True
        print("This is occupied")
        return False


    def can_place(self, x, y):
        if ((x,) + (y,) + (1,)) in self.pos_player or ((x,) + (y,) + (2,)) in self.pos_player:
            return False
        position = (int((x - 30)/38), int((y - 30)/38))
        for key, value in new_rules.items():
            if (key in self.ally and self.ally[key] >= 2 and self.is_free(position[0], position[1], cord[key]))\
                 or (key in self.ally and oposite[key] in self.ally and\
                        self.is_free(position[0], position[1], cord[key]) and\
                        self.is_free(position[0], position[1], cord[oposite[key]])):
                print("-----------FP For this key {} it is true and free".format(key))
                for pos in value:
                    print("SP For this key {}".format(pos))                    
                    if pos in self.ally and self.ally[pos] >= 2 and self.is_free(position[0], position[1], cord[pos]):
                        print("Can't place")
                        return False
                    if pos in self.ally and oposite[pos] in self.ally and\
                        self.is_free(position[0], position[1], cord[pos]) and\
                        self.is_free(position[0], position[1], cord[oposite[pos]]):
                            print("Catn place too")
                            return False
        self.coordinate[position[0], position[1]] = self.current_player
        print("ok to place")
        return True


    def check_event(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and (not self.ai_mode or self.current_player == 1):
                pos = pygame.mouse.get_pos()
                x_player, y_player = in_inter(pos, self.inters)
                if x_player != 0 and y_player != 0:
                    pos = (int((x_player - 30)/38), int((y_player - 30)/38))
                    self.map_players(pos[0], pos[1])
                    if self.can_place(x_player, y_player):
                        self.pos_player.append(((x_player,) + (y_player,) + (self.current_player,)))
                        pos = (int((x_player - 30)/38), int((y_player - 30)/38))
                        self.coordinate[pos] = self.current_player
                        self.check_hor_capture(pos[0], pos[1])
                        self.time_clock.tick()
                        self.change_player()
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

    def add_outside(self, x, y):
        for name in index:
            if (x, y) in cord[name]:
                try:
                    self.outside[name] += 1
                except KeyError:
                    self.outside[name] = 1

    def map_players(self, x, y):
        """
        Map all the neighbourgs of the given position in the 8 differents directions
        """
        self.enemy = {}
        self.ally = {}
        self.outside = {}
        to_add_y = -4
        for e in range(9):
            to_add_x = -4
            for i in range(9):
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
                    self.add_outside(to_add_x, to_add_y)
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
        ncur = notcur_p(self.current_player, self.j1.id, self.j2.id)
        newpos1.append(ncur)
        newpos2.append(ncur)
        newpos1 = tuple(newpos1)
        newpos2 = tuple(newpos2)
        pos1 = tuple(pos1)
        pos2 = tuple(pos2)
        self.coordinate[pos1] = -1
        self.coordinate[pos2] = -1
        i = self.pos_player.index(newpos1)
        j = self.pos_player.index(newpos2)


        if self.current_player == 1:
            self.j1.captured[self.pos_player[-1]] = [(newpos1, i), (newpos2, j)]
            self.j1.capture += 1
            print(self.j1.captured)
        else:
            self.j2.captured[self.pos_player[-1]] = [(newpos1, i), (newpos2, j)]
            self.j2.capture += 1
            print(self.j2.captured)

        self.pos_player.remove(newpos1)
        self.pos_player.remove(newpos2)


    def erase(self):
        "undo function, TODO restore captured piece"
        if self.ai_mode:
            try:
                r = self.pos_player.pop()
                r1 = self.pos_player.pop()
                self.coordinate[(int((r1[0] - 30)/38), int((r1[1] - 30)/38))] = -1

                self.coordinate[(int((r[0] - 30)/38), int((r[0] - 30)/38))] = -1
                time.sleep(0.2)
            except IndexError:
                pass
        else:
            try:
                r = self.pos_player.pop()
                self.coordinate[(int((r[0] - 30)/38), int((r[1] - 30)/38))] = -1
                self.restore(r)
                if self.current_player == 1:
                    self.current_player = 2
                else:
                    self.current_player = 1
                time.sleep(0.2)
            except IndexError:
                pass

    def restore(self, pos):
        """restore captured pieces when undo"""
        i = 0
        if self.current_player == 1:
            for key, coor in self.j1.captured.items():
                if key == pos:
                    for each in coor:
                        self.pos_player.insert(each[1], each[0])
                        self.coordinate[(int((each[0][0] - 30)/38), int(each[0][1] - 30)/38)] = each[0][2]
                    self.j1.capture -= 1
                    i = 1
            if i == 1:
                self.j1.captured.pop(pos)
        else:
            for key, coor in self.j2.captured.items():
                if key == pos:
                    for each in coor:
                        self.pos_player.insert(each[1], each[0])
                        self.coordinate[(int((each[0][0] - 30)/38), int(each[0][1] - 30)/38)] = each[0][2]
                    self.j1.capture -= 1
                    i = 1
            if i == 1:
                self.j2.captured.pop(pos)

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
        button(0, 760, 150, 50, "undo", self.window, self.erase)

    def display_player(self):
        for elem in self.pos_player:
            if elem[2] == 1:
                self.window.blit(self.img_player_one, (elem[0] - 12, elem[1] - 12))
            else:
                self.window.blit(self.img_player_two, (elem[0] - 12, elem[1] - 12))
        pygame.display.flip()

class Player():

    def __init__(self, id, ai=False):
        self.ai = ai
        self.capture = 0
        self.captured = {}
        self.alignement = 0
        self.id = id


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
    gomoku = Gomoku(ai_mode)

    gomoku.coordinate = get_coordinate(nb_square)
    gomoku.inters = get_inter(nb_square, gomoku)
    while True:
        gomoku.check_event()
        gomoku.display_player()
        gomoku.fill_background(nb_square)

start_game()
