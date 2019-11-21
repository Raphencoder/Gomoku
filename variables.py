vert_down = [(0, 1), (0, 2), (0, 3)]
three_vert_down = [(0, 3), (0, 4)]

vert_up = [(0, -1), (0, -2), (0, -3)]
three_vert_up = [(0, -3), (0, -4)]

hor_left = [(-1, 0), (-2, 0), (-3, 0)]
three_hor_left = [(-3, 0), (-4, 0)]

hor_right = [(1, 0), (2, 0), (3, 0)]
three_hor_right = [(3, 0), (4, 0)]

diag_left_up = [(-1, -1), (-2, -2), (-3, -3)]
three_diag_left_up = [(-3, -3), (-4, -4)]

diag_left_down = [(-1, 1), (-2, 2), (-3, 3)]
three_diag_left_down = [(-3, 3), (-4, 4)]

diag_right_up = [(1, -1), (2, -2), (3, -3)]
three_diag_right_up = [(3, -3), (4, -4)]

diag_right_down = [(1, 1), (2, 2), (3, 3)]
three_diag_right_down = [(3, 3), (4, 4)]

cord = {}
index = [
        "vert_down",
        "three_vert_down",
        "vert_up",
        "three_vert_up",
        "hor_left",
        "hor_right",
        "diag_right_down",
        "three_diag_right_down",
        "diag_left_up",
        "three_diag_left_up",
        "diag_left_down",
        "three_diag_left_down",
        "diag_right_up",
        "three_diag_right_up"
 ]
cord["vert_down"] = vert_down
cord["three_vert_down"] = three_vert_down
cord["vert_up"] = vert_up
cord["three_vert_up"] = three_vert_up
cord["hor_left"] = hor_left
cord["hor_right"] = hor_right
cord["diag_right_down"] = diag_right_down
cord["three_diag_right_down"] = three_diag_right_down
cord["diag_left_up"] = diag_left_up
cord["three_diag_left_up"] = three_diag_left_up
cord["diag_left_down"] = diag_left_down
cord["three_diag_left_down"] = three_diag_left_down
cord["diag_right_up"] = diag_right_up
cord["three_diag_right_up"] = three_diag_right_up

new_rules = {}

new_rules["vert_up"] = [
                "diag_right_up",
                "hor_right",
                "diag_right_down",
                "diag_left_down",
                "hor_left",
                "diag_left_up"
]
new_rules["diag_right_up"] = [
                "vert_up",
                "hor_right",
                "diag_right_down",
                "vert_down",
                "hor_left",
                "diag_left_up"
]
new_rules["hor_right"] = [
                "vert_up",
                "diag_right_up",
                "diag_right_down",
                "vert_down",
                "diag_left_down",
                "diag_left_up"
]
new_rules["diag_right_down"] = [
                "vert_up",
                "diag_right_up",
                "hor_right",
                "vert_down",
                "diag_left_down",
                "hor_left"
]
new_rules["vert_down"] = [
                "diag_right_up",
                "hor_right",
                "diag_right_down",
                "diag_left_down",
                "hor_left",
                "diag_left_up"
]
new_rules["diag_left_down"] = [
                "vert_up",
                "hor_right",
                "diag_right_down",
                "vert_down",
                "hor_left",
                "diag_left_up"
]
new_rules["hor_left"] = [
                "vert_up",
                "diag_right_up",
                "diag_right_down",
                "vert_down",
                "diag_left_down",
                "diag_left_up"
]
new_rules["diag_left_up"] = [
                "vert_up",
                "diag_right_up",
                "hor_right",
                "vert_down",
                "diag_left_down",
                "hor_left"
]
oposite = {}
oposite["hor_left"] = "hor_right"
oposite["hor_right"] = "hor_left"
oposite["diag_right_up"] = "diag_left_down"
oposite["diag_left_down"] = "diag_right_up"
oposite["diag_right_down"] = "diag_left_up"
oposite["diag_left_up"] = "diag_right_down"
oposite["vert_up"] = "vert_down"
oposite["vert_down"] = "vert_up"
dir = ["hor", "ver", "dia_l", "dia_r"]

alignement = {
    (1, True, True): "one_free",
    (1, True, False): "one_sided",
    (1, False, True): "one_sided",
    (1, False, False): "one_block",
    (2, True, True): "two_free",
    (2, True, False): "two_sided",
    (2, False, True): "two_sided",
    (2, False, False):"two_block",
    (3, True, True):"three_free",
    (3, True, False):"three_sided",
    (3, False, True):"three_sided",
    (3, False, False):"three_block",
    (4, True, True):"four_free",
    (4, True, False):"four_sided",
    (4, False, True):"four_sided",
    (4, False, False):"four_block",
    (5):"five"
}
score = {
    "one_free" : 5,
    "one_sided" : 2,
    "one_block" : 0,
    "two_free" : 10,
    "two_sided" : -5,
    "two_block" : 0,
    "three_free" : 100,
    "three_sided" : 50,
    "three_block" : 20,
    "four_free" : 2000,
    "four_sided" : 3000,
    "four_block" : 150,
    "five" : 5000,
    }
