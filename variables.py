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
                "hor_left"
                "diag_left_up"
]
new_rules["diag_right_up"] = [
                "vert_up",
                "hor_right",
                "diag_right_down",
                "vert_down",
                "hor_left"
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
                "vert_up"
                "hor_right",
                "diag_right_down",
                "vert_down"    
                "hor_left",
                "diag_left_up"
]
new_rules["hor_left"] = [
                "vert_up"
                "diag_right_up",
                "diag_right_down",
                "vert_down"    
                "diag_left_down",
                "diag_left_up"
]
new_rules["diag_left_up"] = [
                "vert_up"
                "diag_right_up",
                "hor_right"
                "vert_down"    
                "diag_left_down",
                "hor_left"
]