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

free_threes = {}

free_threes["up"] = [
                    "diag_right_down",
                    "hor_left",
                    "three_diag_right_down",
                    "three_hor_left"
                    ]
free_threes["down"] = [
                    "diag_left_up",
                    "hor_right",
                    "three_diag_left_up",
                    "three_hor_right",
                    ]
free_threes["left"] = [
                    "diag_right_up",
                    "vert_down",
                    "three_diag_right_up",
                    "three_vert_down"
                    ]
free_threes["right"] = [
                            "diag_left_down", 
                            "vert_up", 
                            "three_diag_left_down",
                            "three_vert_up" 
                            ]


free_threes["up-square"] = [
                            "diag_left_down",
                            "diag_right_down",
                            "three_diag_right_down",
                            "three_diag_left_down"
                        ]
free_threes["down-square"] = [
                            "diag_left_up",
                            "diag_right_up",
                            "three_diag_right_up",
                            "three_diag_left_up"
                        ]
free_threes["left-square"] = [
                            "diag_right_down",
                            "diag_right_up",
                            "three_diag_right_up",
                            "three_diag_right_down"
                        ]
free_threes["right-square"] = [
                            "diag_left_up",
                            "diag_left_down",
                            "three_diag_left_down",
                            "three_diag_left_up"
                        ]
free_threes["up_square"] = [
                            "hor_left",
                            "vert_down",
                            "three_vert_down",
                            "three_hor_left"
                        ]
free_threes["down_square"] = [
                            "hor_right",
                            "vert_up",
                            "three_vert_up",
                            "three_hor_right"
                        ]
free_threes["left_square"] = [
                            "vert_down",
                            "hor_right",
                            "three_hot_right",
                            "three_vert_down"
                        ]
free_threes["right_square"] = [
                            "vert_up",
                            "hor_left",
                            "three_hor_left",
                            "three_vert_up"
                        ]

free_threes["up_mi_square"] = [
                            "hor_left",
                            "diag_right_down",
                            "three_diag_right_down",
                            "three_hor_left"
                        ]
free_threes["down_mi_square"] = [
                            "hor_right",
                            "diag_left_up",
                            "three_diag_left_up",
                            "three_hor_right"
                        ]
free_threes["left_mi_square"] = [
                            "vert_down",
                            "diag_right_down",
                            "three_diag_right_down",
                            "three_vert_down"
                        ]
free_threes["right_mi_square"] = [
                            "vert_up",
                            "diag_left_up",
                            "three_diag_left_up",
                            "three_vert_up"
                        ]

free_threes["up_mi"] = [
                            "vert_down",
                            "diag_right_down",
                            "three_diag_right_down",
                            "three_vert_down"
                        ]

free_threes["left_mi"] = [
                            "hor_right",
                            "diag_right_up",
                            "three_diag_right_up",
                            "three_hor_right"
                        ]
free_threes["right_mi"] = [
                            "hor_left",
                            "diag_left_up",
                            "three_diag_left_up",
                            "three_hor_left"
                        ]
free_threes["down_mi"] = [
                            "vert_up",
                            "diag_right_up",
                            "three_diag_right_up",
                            "three_vert_up"
                        ]
