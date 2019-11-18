import pygame
import os
import sys
from menu import game_intro, text_objects, button, quit_game
from random import *
from variables import cord, index, new_rules, oposite, dir
import time


"""
TODO :
    *minimax algo with alphabeta pruning
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
        self.nb_turn = 0
        self.turn = 0
        self.end = 0
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
        print(to_add_x, to_add_y, coordonates)
        pos_x = x
        pos_y = y
        count = 0
        try:
            while self.coordinate[pos_x, pos_y] == -1:
                pos_x += to_add_x
                pos_y += to_add_y
        except KeyError:
            return False        
        try:
            while self.coordinate[pos_x, pos_y] == self.current_player:
                pos_x += to_add_x
                pos_y += to_add_y
                count += 1
                if count >= 3:
                    return False
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
                    if (key in self.ally and self.ally[key] >= 3) or (oposite[key] in self.ally and\
                        key in self.ally and self.ally[key] + self.ally[oposite[key]] >= 3):
                        print("More than three")
                        return True 
                    if (pos in self.ally and self.ally[pos] >= 3) or (oposite[pos] in self.ally and\
                        pos in self.ally and self.ally[pos] + self.ally[oposite[pos]] >= 3):
                        print("More than three")
                        return True 
                    print("SP For this key {}".format(pos))
                    if pos in self.ally and self.ally[pos] >= 2 and self.is_free(position[0], position[1], cord[pos])\
                        and self.is_free(position[0], position[1], cord[oposite[pos]])\
                        and self.is_free(position[0], position[1], cord[oposite[key]]):
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
                        if self.current_player == 1:
                            for each in dir:
                                self.j1.align = self.check_align(pos, 1, each, self.j1.align)
                            print(self.j1.align)
                            if self.nb_turn >= 4:
                                self.checkmate(self.j2.check, self.j2.last_pos, 2, self.j2.align)
                            self.j1.last_pos = pos
                        else:
                            for each in dir:
                                self.j2.align = self.check_align(pos, 2, each, self.j2.align)
                            print(self.j2.align)
                            if self.nb_turn >= 4:
                                self.checkmate(self.j1.check, self.j1.last_pos, 1, self.j1.align)
                            self.j2.last_pos = pos
                        self.turn += 1
                        if self.turn == 2:
                            self.turn = 0
                            self.nb_turn += 1
                        self.change_player()
            elif event.type == pygame.QUIT:
                pygame.quit()
                quit()

    def check_align(self, coor, player, dir, n):
        """return each alignement direction for current coordinate"""
        n[dir] = 1
        pn = [1,1]
        for x in range (1, 5):
            pn = self.calc(dir, x, coor, pn, player)
            if pn[0]:
                n[dir] += 1
            if pn[1]:
                n[dir] += 1
        return(n)

    def calc(self, dir, x, coor, pn, player):
        """check each neighboor of coor for each direction"""
        if dir == "hor":
            coord = ((coor[0] + x, coor[1]), (coor[0] - x, coor[1]))
            pn = self.not_player(coord, pn, player)
        elif dir == "ver":
            coord = ((coor[0], coor[1] + x), (coor[0], coor[1] - x))
            pn = self.not_player(coord, pn, player)
        elif dir == "dia_r":
            coord = ((coor[0] +x , coor[1] -x), (coor[0] -x , coor[1] +x))
            pn = self.not_player(coord, pn, player)
        elif dir == "dia_l":
            coord = ((coor[0] +x , coor[1] +x), (coor[0] -x , coor[1] -x))
            pn = self.not_player(coord, pn, player)
        return(pn)

    def not_player(self, coord, pn, player):
        """check if coordinate neighboor aren't out of the map or the enemy pawn"""
        pn = self.out_of_map(coord, pn)
        if pn[0] and self.coordinate[coord[0]] != player:
            pn[0] = 0
        if pn[1] and self.coordinate[coord[1]] != player:
            pn[1] = 0
        return(pn)

    def out_of_map(self, coor, pn):
        if coor[0] not in self.coordinate:
            pn[0] = 0
        if coor[1] not in self.coordinate:
            pn[1] = 0
        return(pn)

    def checkmate(self, check, pos, p, align):
        """trigger the end of the game if check not countered"""
        for each in dir:
            align = self.check_align(pos, p, each, align)
        if check == 1 and 5 in align.values():
            self.end = 1
        else:
            check = 0

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
        to_erase = []
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
                    self.capture(sup1, sup2, to_erase)
        for each in to_erase:
            self.pos_player.remove(each)
        del to_erase[:]

    def capture(self, pos1, pos2, to_erase):
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
            if self.pos_player[-1] in self.j1.captured:
                self.j1.captured[self.pos_player[-1]].append((newpos1, i))
                self.j1.captured[self.pos_player[-1]].append((newpos2, j))
                self.j1.capture += 1
            else:
                self.j1.captured[self.pos_player[-1]] = [(newpos1, i), (newpos2, j)]
                self.j1.capture += 1
        else:
            if self.pos_player[-1] in self.j2.captured:
                self.j2.captured[self.pos_player[-1]].append((newpos1, i))
                self.j2.captured[self.pos_player[-1]].append((newpos2, j))
                self.j2.capture += 1
            else:
                self.j2.captured[self.pos_player[-1]] = [(newpos1, i), (newpos2, j)]
                self.j2.capture += 1
        to_erase.append(newpos1)
        to_erase.append(newpos2)

    def check_win(self):
        """check if a condition for winning is fulfilled"""
        if self.j1.capture >= 5 or self.j2.capture >= 5:
            return(1)
        elif self.end == 1:
            return(1)
        elif 5 in self.j1.align.values():
            self.j1.check = 1
            return(0)
        elif 5 in self.j2.align.values():
            self.j2.check = 1
            return(0)

    def d_win(self):
        """display winner and message need refactoring and more polish"""
        if self.j2.capture >= 5:
            self.message("J2 win by Capture")
        elif self.j1.capture >= 5:
            self.message("J1 Win By Capture")
        elif 5 in self.j2.align.values():
            self.message("J2 Win By Alignement")
        elif 5 in self.j1.align.values():
            self.message("J1 Win By Alignement")

    def message(self, msg):
        smallText = pygame.font.Font("freesansbold.ttf",24)
        textSurf, textRect = text_objects(msg, smallText)
        textRect.center = (400, 770)
        button(0, 760, 150, 50, "Exit", self.window, quit_game)
        self.window.blit(textSurf, textRect)

    def erase(self):
        """undo function TODO check when ai_mode implemeted"""
        if self.ai_mode:
            try:
                r = self.pos_player.pop()
                self.coordinate[(int((r[0] - 30)/38), int((r[0] - 30)/38))] = -1
                self.restore(r)
                r1 = self.pos_player.pop()
                self.coordinate[(int((r1[0] - 30)/38), int((r1[1] - 30)/38))] = -1
                self.restore(r1)
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
                print("can't undo anymore")
                pass

    def restore(self, pos):
        """restore captured pieces when undo"""
        i = 0
        if self.current_player == 2:
            for key, coor in self.j1.captured.items():
                if key == pos:
                    order = sorted(coor, key=lambda i: i[1])
                    print(order)
                    for each in coor:
                        self.coordinate[(int((each[0][0] - 30)/38), int(each[0][1] - 30)/38)] = each[0][2]
                    for each in order:
                        self.pos_player.insert(each[1], each[0])
                        i += 1
                    self.j1.capture -= i/2
            if i > 0:
                self.j1.captured.pop(pos)
        else:
            for key, coor in self.j2.captured.items():
                if key == pos:
                    order = sorted(coor, key=lambda i: i[1])
                    print(order)
                    for each in coor:
                        self.coordinate[(int((each[0][0] - 30)/38), int(each[0][1] - 30)/38)] = each[0][2]
                    for each in order:
                        self.pos_player.insert(each[1], each[0])
                        i += 1
                    self.j2.capture -= i/2
            if i > 0:
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
        if not self.end:
            button(0, 760, 150, 50, "Undo", self.window, self.erase)

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
        self.align = {}
        self.id = id
        self.check = 0
        self.last_pos = None


def start_game():

    pygame.init()
    ai_mode = game_intro(pygame.display.set_mode((800, 800)))
    pygame.quit()
    nb_square = 19
    gomoku = Gomoku(ai_mode)

    gomoku.coordinate = get_coordinate(nb_square)
    gomoku.inters = get_inter(nb_square, gomoku)
    while True:
        if gomoku.check_win():
            gomoku.d_win()
            event = pygame.event.wait()
        gomoku.check_event()
        gomoku.display_player()
        gomoku.fill_background(nb_square)
    pygame.quit()

start_game()
