import os
import pygame


DIR_UP, DIR_DOWN, DIR_LEFT, DIR_RIGHT = "up", "down", "left", "right"
directions_codes = {"up": (0, 1), "down": (0, -1), "left": (-1, 0), "right": (1, 0),
                    (0, 1): "up", (0, -1): "down", (-1, 0): "left", (1, 0): "right"}


def is_opposite(direction_1: str, direction_2: str) -> bool:
    """Returns True if directions are opposite else False"""
    x, y = directions_codes[direction_1][0] + directions_codes[direction_2][0],\
        directions_codes[direction_1][1] + directions_codes[direction_2][1]

    return x == y == 0


def get_opposite(direction: str) -> str:
    """Returns opposite direction for given one"""
    code = directions_codes[direction]
    opposite_code = code[0] * -1, code[1] * -1
    return directions_codes[opposite_code]


def load_image(name: str) -> pygame.image:
    """Returns pygame image from given file name"""
    fullname = os.path.join("data", name)
    if not os.path.isfile(fullname):
        raise ValueError(f"No image with name '{fullname}' found")

    image = pygame.image.load(fullname)
    return image
