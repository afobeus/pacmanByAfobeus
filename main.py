import pygame
import sys


def get_size():
    input_data = input().split()
    if len(input_data) != 2:
        raise ValueError
    number_1, number_2 = input_data
    if not (number_1.isdigit() and int(number_1) > 0):
        raise ValueError
    if not (number_2.isdigit() and int(number_2) > 0):
        raise ValueError
    return int(number_1), int(number_2)


def init_pygame():
    pygame.init()
    screen = pygame.display.set_mode(1200, 700)
    pygame.display.set_caption("Packman")

    return screen


if __name__ == '__main__':
    screen = init_pygame()
    while pygame.event.wait().type != pygame.QUIT:
        pass
    pygame.quit()
