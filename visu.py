import pygame
import os
import sys
from menu import game_intro, text_objects, button, quit_game
from variables import cord, index, new_rules, oposite, dir
from ai_algo import ai_play, check_align
import time


"""
TODO :
    *minimax algo with alphabeta pruning
    * Free three bug
"""

yellow = (243, 210, 132)

notcur_p = lambda x, y , z : y if x != y else z
r_conv = lambda x, y : (x * 40 + 30, y * 40 + 30)
conv = lambda x, y: (int((x - 30)/40), int((y - 30)/40))

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

    def is_free_double(self, xy, coordonates):
        to_add_x = coordonates[1][0] - coordonates[0][0]
        to_add_y = coordonates[1][1] - coordonates[0][1]
        x = xy[0]
        y = xy[1]
        pos_x = x
        pos_y = y
        pos_x += to_add_x
        pos_y += to_add_y
        # print("check for this coordonates:", xy)
        # print(pos_x, pos_y)
        try:
            if self.coordinate[pos_x, pos_y] == self.current_player and\
                self.coordinate[pos_x + to_add_x, pos_y + to_add_y] == self.current_player and\
                    self.coordinate[pos_x + 2*to_add_x, pos_y + 2*to_add_y] == -1:
                # print("return True")
                return True
        except KeyError:
            # print("eror map return False")
            return False
        try:
            if self.coordinate[pos_x, pos_y] == self.current_player and\
                self.coordinate[pos_x + to_add_x, pos_y + to_add_y] == -1:
                pos_x += 2*to_add_x
                pos_y += 2*to_add_y
                # print("here we expect a current player after two bonds", pos_x, pos_y)
                if self.coordinate[pos_x, pos_y] == self.current_player and\
                    self.coordinate[pos_x + to_add_x, pos_y + to_add_y] == -1:
                    # print("return Truee")
                    return True
                else:
                    # print("return False")
                    return False
            else:
                # print("default return True")
                return False
        except KeyError:
            # print("eror map return Falsee")
            return False

    def is_free_one(self, xy, coordonates):
        # print("-- into one --")
        to_add_x = coordonates[1][0] - coordonates[0][0]
        to_add_y = coordonates[1][1] - coordonates[0][1]
        x = xy[0]
        y = xy[1]
        pos_x = x
        pos_y = y
        pos_x += 2*to_add_x
        pos_y += 2*to_add_y
        # print("check for this coordonates:", xy)
        # print("toaddx, toadd_y:", to_add_x, to_add_y)
        # print(pos_x, pos_y)
        try:
            if self.coordinate[pos_x, pos_y] == -1:
                # print("return True")
                return True
            else:
                # print("return False")
                return False
        except KeyError:
            # print("Outside map return False")
            return False


    def is_free_oposite_double(self, xy, coordonates):
        # print("-- oposite --")
        to_add_x = coordonates[1][0] - coordonates[0][0]
        to_add_y = coordonates[1][1] - coordonates[0][1]
        x = xy[0]
        y = xy[1]
        pos_x = x
        pos_y = y
        pos_x += to_add_x
        pos_y += to_add_y
        # print("check for this coordonates:", xy)
        # print("toaddx, toadd_y:", to_add_x, to_add_y)
        # print(pos_x, pos_y)
        try:
            if self.coordinate[pos_x, pos_y] == -1:
                # print("return True")
                return True
            else:
                # print("return False")
                return False
        except KeyError:
            # print("Outside map return False")
            return False

    def can_place(self, x, y):
        if ((x,) + (y,) + (1,)) in self.pos_player or ((x,) + (y,) + (2,)) in self.pos_player:
            return False
        position = conv(x, y)
        for key, value in new_rules.items():
            if key in self.ally:
                if self.ally[key] == 1 and self.is_free_one(position, cord[key]) and \
                oposite[key] in self.ally and self.ally[oposite[key]] == 1 and self.is_free_one(position, cord[oposite[key]]):
                    #print("The first one "+key+" is free check the other")
                    for pos in value:
                        if pos in self.ally:
                            print("The other is "+pos+"")
                            if self.ally[pos] == 1 and self.is_free_one(position, cord[pos]) and \
                            oposite[pos] in self.ally and self.ally[oposite[pos]] == 1 and self.is_free_one(position, cord[oposite[pos]]):
                                return False
                            if self.ally[pos] == 2 and self.is_free_double(position, cord[pos]) and\
                            oposite[pos] not in self.ally and self.is_free_oposite_double(position, cord[oposite[pos]]):
                                return False
                if self.ally[key] == 2 and self.is_free_double(position, cord[key]) and \
                oposite[key] not in self.ally and self.is_free_oposite_double(position, cord[oposite[key]]):
                    #print("The first one "+key+" is free check the other")
                    for pos in value:
                        if pos in self.ally:
                            print("The other is "+pos+"")
                            if self.ally[pos] == 1 and self.is_free_one(position, cord[pos]) and \
                            oposite[pos] in self.ally and self.ally[oposite[pos]] == 1 and self.is_free_one(position, cord[oposite[pos]]):
                                return False
                            if self.ally[pos] == 2 and self.is_free_double(position, cord[pos]) and\
                            oposite[pos] not in self.ally and self.is_free_oposite_double(position, cord[oposite[pos]]):
                                return False
        return True

    def check_event(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                x_player, y_player = in_inter(pos, self.inters)
                if x_player != 0 and y_player != 0:
                    pos = conv(x_player, y_player)
                    self.map_players(pos[0], pos[1])
                    if self.can_place(x_player, y_player):
                        self.pos_player.append(((x_player,) + (y_player,) + (self.current_player,)))
                        self.coordinate[pos] = self.current_player
                        self.check_hor_capture(pos[0], pos[1])
                        if self.current_player == 1:
                            for each in dir:
                                self.j1.align = check_align(self, pos, 1, each, self.j1.align)
                            if self.nb_turn >= 4:
                                self.checkmate(self.j2.check, self.j2.last_pos, 2, self.j2.align)
                            self.j1.last_pos = pos
                        else:
                            for each in dir:
                                self.j2.align = check_align(self, pos, 2, each, self.j2.align)
                            if self.nb_turn >= 4:
                                self.checkmate(self.j1.check, self.j1.last_pos, 1, self.j1.align)
                            self.j2.last_pos = pos
                        self.inc_turn()
                        self.change_player()
                        self.time_clock.tick()
            elif event.type == pygame.QUIT:
                pygame.quit()
                quit()


    def checkmate(self, check, pos, p, align):
        """trigger the end of the game if check not countered"""
        for each in dir:
            align = check_align(self, pos, p, each, align)
        if check == 1:
            value = list(align.values())
            fullist = [item for sublist in value for item in sublist]
            if 5 in fullist:
                self.end = 1
            if p == 1:
                self.j1.win = 1
            else:
                self.j2.win = 1
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

    def check_hor_capture(self, x, y, real=True):
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
                if real and pos != -1 and pos == self.current_player:
                    self.capture(sup1, sup2, to_erase)
                elif not real and pos != -1 and pos == self.current_player:
                    if self.current_player == 1 and self.j1.capture < 4:
                        self.j1.score += 1000
                    elif self.current_player == 1 and self.j1.capture == 4:
                        self.j1.score += 10000
                    elif self.current_player == 2 and self.j2.capture < 4:
                        self.j2.score -= 1000
                    elif self.current_player == 2 and self.j1.capture == 4:
                        self.j2.score -= 10000
        for each in to_erase:
            self.pos_player.remove(each)
        del to_erase[:]

    def capture(self, pos1, pos2, to_erase):
        """
        trigger a capture
        """
        newpos1 = [(i * 40 + 30)  for i in pos1]
        newpos2 = [(i * 40 + 30) for i in pos2]
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
        elif self.current_player == 2:
            value = list(self.j1.align.values())
            fullist = [item for sublist in value for item in sublist]
            if 5 in fullist:
                self.j1.check = 1
                return(0)
        else:
            value = list(self.j2.align.values())
            fullist = [item for sublist in value for item in sublist]
            if 5 in fullist:
                self.j2.check = 1
                return(0)

    def d_win(self):
        """display winner and message """
        if self.j2.capture >= 5:
            self.end = 1
            self.message("J2 win by Capture")
        elif self.j1.capture >= 5:
            self.end = 1
            self.message("J1 Win By Capture")
        elif self.j2.win:
            self.message("J2 Win By Alignement")
        elif self.j1.win:
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
            r = self.pos_player.pop()
            self.coordinate[conv(r[0], r[1])] = -1
            self.restore(r)
            r1 = self.pos_player.pop()
            self.coordinate[conv(r1[0], r1[1])] = -1
            self.restore(r1)
            self.nb_turn -= 1
            time.sleep(0.2)
        else:
            r = self.pos_player.pop()
            self.coordinate[conv(r[0], r[1])] = -1
            self.restore(r)
            if self.current_player == 1:
                self.current_player = 2
            else:
                self.current_player = 1
            time.sleep(0.2)

    def restore(self, pos):
        """
        restore captured pieces when undo
         *TODO restore doesn't work in ai_play since you can't undo during the AI turn
        """
        i = 0
        if self.current_player == 2:
            for key, coor in self.j1.captured.items():
                if key == pos:
                    order = sorted(coor, key=lambda i: i[1])
                    print(order)
                    for each in coor:
                        self.coordinate[conv(each[0][0], each[0][1])] = each[0][2]
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
                        self.coordinate[conv(each[0][0] , each[0][1])] = each[0][2]
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
        if not self.end and self.pos_player:
            button(0, 760, 150, 50, "Undo", self.window, self.erase)

    def display_player(self):
        for elem in self.pos_player:
            if elem[2] == 1:
                self.window.blit(self.img_player_one, (elem[0] - 12, elem[1] - 12))
            else:
                self.window.blit(self.img_player_two, (elem[0] - 12, elem[1] - 12))
        pygame.display.flip()

    def inc_turn(self):
        self.turn += 1
        if self.turn == 2:
            self.turn = 0
            self.nb_turn += 1

class Player():

    def __init__(self, id, ai=False):
        self.ai = ai
        self.capture = 0
        self.captured = {}
        self.align = {}
        self.id = id
        self.check = 0
        self.last_pos = None
        self.win = 0
        self.score = 0

def start_game():

    pygame.init()
    ai_mode = game_intro(pygame.display.set_mode((800, 800)))
    pygame.quit()
    nb_square = 18
    gomoku = Gomoku(ai_mode)

    gomoku.coordinate = get_coordinate(nb_square)
    gomoku.inters = get_inter(nb_square, gomoku)
    while True:
        if gomoku.check_win():
            gomoku.d_win()
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                quit_game()
        if ai_mode and gomoku.current_player == 1:
            ai_play(gomoku)
        gomoku.check_event()
        gomoku.display_player()
        gomoku.fill_background(nb_square)
    pygame.quit()

start_game()
