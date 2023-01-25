import pygame
from game_field import GameField


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption("Packman")
    clock = pygame.time.Clock()
    running = True

    game_field = GameField()
    game_field.load_map_scheme("vasa.txt")
    screen = pygame.display.set_mode(game_field.get_screen_size())
    game_field.set_screen(screen)
    game_field.render()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip()
        clock.tick(10)

    pygame.quit()
