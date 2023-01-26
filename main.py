import pygame
from game_field import GameField
from essences import Packman


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption("Packman")
    clock = pygame.time.Clock()
    running = True

    game_field = GameField()
    game_field.load_map_scheme("original level.txt")
    screen = pygame.display.set_mode(game_field.get_screen_size())
    game_field.set_screen(screen)

    essences_sprite_group = pygame.sprite.Group()
    packman = Packman("left", (360, 640))
    essences_sprite_group.add(packman)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        packman.move(clock.tick())

        screen.fill("black")
        game_field.render()
        essences_sprite_group.draw(screen)
        pygame.display.flip()

    pygame.quit()
