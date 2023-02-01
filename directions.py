DIR_UP, DIR_DOWN, DIR_LEFT, DIR_RIGHT = "up", "down", "left", "right"
directions_codes = {"up": (0, 1), "down": (0, -1), "left": (-1, 0), "right": (1, 0)}


def opposite(direction_1, direction_2) -> bool:
    x, y = directions_codes[direction_1][0] + directions_codes[direction_2][0],\
        directions_codes[direction_1][1] + directions_codes[direction_2][1]

    return x == y == 0
