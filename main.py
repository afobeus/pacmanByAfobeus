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


def init_pygame(size):
    pygame.init()
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Крест")

    draw_cross(screen)
    pygame.display.flip()
    while pygame.event.wait().type != pygame.QUIT:
        pass
    pygame.quit()

    return screen


def draw_cross(screen):
    screen_width, screen_height = screen.get_size()
    pygame.draw.line(screen, "white", (0, 0), (screen_width, screen_height), width=5)
    pygame.draw.line(screen, "white", (0, screen_height), (screen_width, 0), width=5)


if __name__ == '__main__':
    try:
        size = width, height = get_size()
        screen = init_pygame(size)
    except ValueError:
        print("Неправильный формат ввода")
