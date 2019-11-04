vert_down = [(0, 1), (0, 2), (0, 3)]
vert_up = [(0, -1), (0, -2), (0, -3)]

hor_left = [(-1, 0), (-2, 0), (-3, 0)]
hor_right = [(1, 0), (2, 0), (3, 0)]

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
        "vert_up",
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
cord["vert_up"] = vert_up
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

free_threes = {}

free_threes["up"] = [
                    "diag_right_down",
                    "hor_left",
                    "three_diag_right_down"
                    ]
free_threes["down"] = [
                    "diag_left_up",
                    "hor_right",
                    "three_diag_left_up"
                    ]
free_threes["left"] = [
                    "diag_right_up",
                    "vert_down",
                    "three_diag_right_up"
                    ]
free_threes["right"] = [
                            "diag_left_down", 
                            "vert_up", 
                            "three_diag_left_down"
                            ]
arrow_free_threes = {}
arrow_free_threes["up"] = [
                            "diag_left_down",
                            "diag_right_down"
                        ]
arrow_free_threes["down"] = [
                            "diag_left_up",
                            "diag_right_up"
                        ]
arrow_free_threes["left"] = [
                            "diag_right_down",
                            "diag_right_up"
                        ]
arrow_free_threes["right"] = [
                            "diag_left_up",
                            "diag_left_down"
                        ]
