from variables import alignement, score, dir
import random

r_conv = lambda x, y : (x * 40 + 30, y * 40 + 30)
conv = lambda x, y: (int((x - 30)/40), int((y - 30)/40))

def ai_play(gomoku):
    if not gomoku.j1.win:
        if gomoku.nb_turn < 2:
            opening_books(gomoku)
        else:
            minimax(gomoku)

def minimax(gomoku):
    """
    call max for each position in list_pos to find the best option, max
    simulate depht(3) numbers of turn before returning a value
    """
    list_pos = check_board(gomoku)
    print(list_pos, "list_pos")
    list_score = [-9000000, 9000000, -9000000]
    tmp = -9000000
    tmp_pos = None
    svg_j1, svg_j2 = gomoku.j1.last_pos, gomoku.j2.last_pos

    for x in list_pos:
        value = max_ai(gomoku, [x], 0, [], -9000000, list_score)
        list_score = [-9000000, 9000000, -9000000]
        gomoku.j1.last_pos, gomoku.j2.last_pos = svg_j1, svg_j2
        print(value, x, "value and potential move")
        if value > tmp:
            tmp = value
            tmp_pos = x
        print("END OF SIMULATION FOR {}".format(x))

    #value = max_ai(gomoku, value, 3)
    coord = tmp_pos
    gomoku.time_clock.tick()
    print(tmp, "score of move", coord, "coordonates of move")
    aftermath(gomoku, coord)

def aftermath(gomoku, pos):
    """
    do all the necessary update of all the variable after minimax
    bug : sometimes checkmate doesn't trigger
    """
    r_coord = r_conv(pos[0], pos[1])
    gomoku.pos_player.append((r_coord[0], r_coord[1], 1))
    gomoku.j1.last_pos = pos
    gomoku.coordinate[gomoku.j1.last_pos] = 1
    gomoku.map_players(gomoku.j1.last_pos[0], gomoku.j1.last_pos[1])
    gomoku.check_hor_capture(gomoku.j1.last_pos[0], gomoku.j1.last_pos[1])
    gomoku.inc_turn()
    for each in dir:
        gomoku.j1.align = check_align(gomoku, gomoku.j1.last_pos, 1, each, gomoku.j1.align)
    print(gomoku.j1.align, gomoku.j1.last_pos)
    if gomoku.nb_turn >= 4:
        gomoku.checkmate(gomoku.j2.check, gomoku.j2.last_pos, 2, gomoku.j2.align)
    gomoku.change_player()

def evaluate(gomoku, pos, player, depth, list_score):
    """
    for a coordinate(pos) return the value of the position
     by adding or substracting score of every direction alignement + capture
    """
    total = 0
    r_pos = r_conv(pos[0], pos[1])
    if gomoku.can_place(r_pos[0], r_pos[1]): #needed to check if position is valid
        for each in dir:
            player.align = check_align(gomoku, pos, player.id, each, player.align)
        val_list = list(player.align.values()) #get list of value of each direction formatted as (int, True/False, True/False)
        for each in val_list:
            if player.id == 1:
                total += score[alignement[tuple(each)]]
                 #check score and alignement in variable.py
            else:
                total -= score[alignement[tuple(each)]]
        """
        gomoku.map_players(pos[0], pos[1]) #for checking capture
        gomoku.check_hor_capture(pos[0], pos[1], False)
        total += player.score
        player.score = 0
        """
        if player.id == 1:
            if depth != 0:
                total += list_score[depth - 1]
            print(total, "total score of move (j1)", pos)
            if total > list_score[depth]:
                list_score[depth] = total # - depth * 10
                gomoku.j1.last_pos = pos
            return(list_score[depth])
        else:
            total += list_score[depth - 1]
            print(total, "total score of move (j2)", pos)
            if total < list_score[depth]:
                list_score[depth] = total # - depht * 10
                gomoku.j2.last_pos = pos
            return(list_score[depth])
    else:
        return (None)

def max_ai(gomoku, pos, depth, to_reset, value, list_score):
    """
    recursive function which end when value or depht is reached
    max represent IA move , min the player, max seek the best move for IA
    from a list of position obtained from check_board function (only heuristic for now)
    It will evaluate each pos then call min to simulate the player move until
    a move endgame has been reached or the depht is == 0
    return a score

    TO_DO
        *need some heuristics when min return a potential ending move (ex: four free)
        *need heuristic to counter the min move
        *for now max and min follow the same heurisitic but I think white
        will needs to play capture to win
        *need to implement alpha beta pruning
        -bug: when min return an ending move max will return a position already occupied
        -bug: sometimes max return a position not from the starting list
        (may need to change list_pos to a dict)
    """

    #condition to end recursive
    if value >= 10000:
        for x in to_reset:
            gomoku.coordinate[x] = -1
        del to_reset[:]
        return(value)
    elif value <= -10000 and value != -9000000:
        for x in to_reset:
            gomoku.coordinate[x] = -1
        del to_reset[:]
        return(value)
    elif depth == 3:
        for x in to_reset:
            gomoku.coordinate[x] = -1
        del to_reset[:]
        return(value)

    for nb in pos:
        value = evaluate(gomoku, nb, gomoku.j1, depth, list_score)
    print("*** play {} best possible move for j1(AI) with {} points *** #simulation".format(gomoku.j1.last_pos, value))
    gomoku.coordinate[gomoku.j1.last_pos] = 1
    to_reset.append(gomoku.j1.last_pos)
    list_pos = check_board(gomoku)
    print("///////     MIN TURN        //////")
    value = min_ai(gomoku, list_pos, depth + 1, to_reset, value, list_score)
    #end of recursion
    #print(max, "return value of max_ai")
    return(value)

def min_ai(gomoku, pos, depth, to_reset, value, list_score):
    """see max_ai only difference is min seek minimum value
    the difference of sign is in function evaluate
    """
    if value >= 10000:
        for x in to_reset:
            gomoku.coordinate[x] = -1
        del to_reset[:]
        return(value)
    elif value <= -10000 and value != -9000000:
        for x in to_reset:
            gomoku.coordinate[x] = -1
        del to_reset[:]
        return(value)
    elif depth == 3:
        for x in to_reset:
            gomoku.coordinate[x] = -1
        del to_reset[:]
        return(value)

    for nb in pos:
        value = evaluate(gomoku, nb, gomoku.j2, depth, list_score)
    print("*** play on {} best possible move for j2 with {} points *** #simulation".format(gomoku.j2.last_pos, value))
    gomoku.coordinate[gomoku.j2.last_pos] = 2
    to_reset.append(gomoku.j2.last_pos)
    list_pos = check_board(gomoku)
    print("///////     MAX TURN        ///////")
    value = max_ai(gomoku, list_pos, depth + 1, to_reset, value, list_score)
    #end of recursion

    #print(min, "return value of min_ai")
    return(value)

def check_board(gomoku):
    """
    heuristic function wich evaluate the board with check_threat and return
    a list of coordinate to evaluate them
    use last alignement check from check_align
    """
    pos = list()
    for dir, value in gomoku.j2.align.items():
        if value == 5:
            continue
        for i in range(4, 0, -1):
            pos = check_threat(gomoku, dir, value, i, pos, gomoku.j2.last_pos)
    for dir, value in gomoku.j1.align.items():
        if value == 5:
            continue
        for i in range(4, 0, -1):
            pos = check_threat(gomoku, dir, value, i, pos, gomoku.j1.last_pos)
    listpos = list(dict.fromkeys(pos))
    return(listpos)

def check_threat(gomoku, dir, value, i, pos, last_pos):
    """
        for each direction add coordinates that are the end of each alignement for each player
        ex : if ver = (3, True, True) in self.align with the coordinate (9,9)
        check_threat will add (9,12), (9,11), (9,10), (9,8), (9,7), (9,6)
        and remove at the end coordinate that are out of map or occupied
    """
    if value[0] == i:
        while i > 0:
            if dir == "hor":
                pos.append((last_pos[0] + i , last_pos[1]))
                pos.append((last_pos[0] - i , last_pos[1]))
            elif dir == "ver":
                pos.append((last_pos[0], last_pos[1] + i))
                pos.append((last_pos[0], last_pos[1] - i))
            elif dir == "dia_r":
                pos.append((last_pos[0] + i , last_pos[1] - i))
                pos.append((last_pos[0] - i , last_pos[1] + i))
            elif dir == "dia_l":
                pos.append((last_pos[0] + i , last_pos[1] + i))
                pos.append((last_pos[0] - i , last_pos[1] - i))
            i -= 1
    for each in gomoku.coordinate:
        for coor in pos:
            if coor in gomoku.coordinate.keys() and gomoku.coordinate[coor] != -1:
                pos.remove(coor)
    return(pos)

def opening_books(gomoku):
    """
    called for the first turns to gain time execution may need a check
    when further heuristic are implemented
    """
    if not gomoku.pos_player:
        pos = r_conv(9,9)
        gomoku.pos_player.append((pos[0], pos[1], 1))
        gomoku.coordinate[(9,9)] = 1
        gomoku.inc_turn()
        gomoku.change_player()
    else:
        x = random.randint(-1,1)
        l_play = conv(gomoku.pos_player[-1][0] + x, gomoku.pos_player[-1][1] + x)
        r_play = r_conv(l_play[0],l_play[1])
        while not gomoku.can_place(r_play[0], r_play[1]):
            r_play = r_conv(l_play[0] + random.randint(-1,1), l_play[1] + random.randint(-1,1))
        gomoku.pos_player.append((r_play[0], r_play[1], 1))
        print(gomoku.pos_player)
        l_play = conv(r_play[0], r_play[1])
        gomoku.j1.last_pos = l_play
        gomoku.coordinate[l_play] = 1
        gomoku.change_player()
        gomoku.inc_turn()
    gomoku.time_clock.tick()

def check_align(gomoku, coor, player, dir, n):
    """return each len of alignement for each direction for current coordinate"""
    n[dir] = [1]
    pn = [1,1]
    for x in range (1, 5):
        pn = calc(gomoku, n, dir, x, coor, pn, player)
        if pn[0]:
            n[dir][0] += 1
        if pn[1]:
            n[dir][0] += 1
    if n[dir][0] > 5:
        n[dir][0] = 5
    return(n)

def calc(gomoku, n , dir, x, coor, pn, player):
    """check each neighboor of coor for each direction"""
    if dir == "hor":
        coord = ((coor[0] + x, coor[1]), (coor[0] - x, coor[1]))
    elif dir == "ver":
        coord = ((coor[0], coor[1] + x), (coor[0], coor[1] - x))
    elif dir == "dia_r":
        coord = ((coor[0] +x , coor[1] -x), (coor[0] -x , coor[1] +x))
    elif dir == "dia_l":
        coord = ((coor[0] +x , coor[1] +x), (coor[0] -x , coor[1] -x))
    pn = not_player(gomoku, coord, pn, player, n[dir])
    return(pn)

def not_player(gomoku, coord, pn, player, ndir):
    """check if coordinate neighboor aren't out of the map or the enemy pawn"""
    pn = out_of_map(gomoku, coord, pn, ndir)
    for i in range(2):
        if pn[i] and gomoku.coordinate[coord[i]] == -1:
            ndir.append(True)
            pn[i] = 0
        elif pn[i] and gomoku.coordinate[coord[i]] != player:
            ndir.append(False)
            pn[i] = 0
    return(pn)

def out_of_map(gomoku, coor, pn, ndir):
    for i in range(2):
        if pn[i] and (coor[i] not in gomoku.coordinate):
            pn[i] = 0
            ndir.append(False)
    return(pn)
