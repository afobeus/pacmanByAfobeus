import pygame


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
