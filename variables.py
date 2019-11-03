vert_down = [(0, 1), (0, 2), (0, 3)]
vert_up = [(0, -1), (0, -2), (0, -3)]
hor_left = [(-1, 0), (-2, 0), (-3, 0)]
hor_right = [(1, 0), (2, 0), (3, 0)]
diag_right = [(1, 1), (2, 2), (3, 3)]
diag_left = [(-1, -1), (-2, -2), (-3, -3)]
other_diag_left = [(-1, 1), (-2, 2), (-3, 3)]
other_diag_right = [(1, -1), (2, -2), (3, -3)]

three_diag_spec = [(-3, 3), (-4, 4)]
other_three_diag_spec = [(3, -3), (4, -4)]

cord = {}
index = ["vert_down", "vert_up", "hor_left", "hor_right", "diag_right", "diag_left", "other_diag_left", "other_diag_right", "three_diag_spec", "other_three_diag_spec"]
cord["vert_down"] = vert_down
cord["three_diag_spec"] = three_diag_spec
cord["other_three_diag_spec"] = other_three_diag_spec
cord["vert_up"] = vert_up
cord["hor_left"] = hor_left
cord["hor_right"] = hor_right
cord["diag_right"] = diag_right
cord["diag_left"] = diag_left
cord["other_diag_left"] = other_diag_left
cord["other_diag_right"] = other_diag_right

free_threes = {}

free_threes["diag_down"] = ["diag_left", "hor_right", "three_diag_spec"]
free_threes["diag_up"] = ["diag_right", "hor_left", "other_three_diag_spec"]
