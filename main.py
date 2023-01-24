import pygame
from game_field import load_image


def init_pygame():
    pygame.init()
    screen = pygame.display.set_mode((1200, 700))
    pygame.display.set_caption("Packman")

    return screen


if __name__ == '__main__':
    screen = init_pygame()
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip()
        clock.tick(10)
    pygame.quit()
