import pygame
from game_field import GameField
from essences import Pacman


def process_key_pressed(event):
    if event.key == pygame.K_LEFT:
        pacman.change_direction("left")
    elif event.key == pygame.K_RIGHT:
        pacman.change_direction("right")
    elif event.key == pygame.K_UP:
        pacman.change_direction("up")
    elif event.key == pygame.K_DOWN:
        pacman.change_direction("down")


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption("Pacman")
    clock = pygame.time.Clock()
    running = True

    game_field = GameField()
    game_field.load_map_scheme("original level.txt")
    screen = pygame.display.set_mode(game_field.get_screen_size())
    game_field.set_screen(screen)

    essences_sprite_group = pygame.sprite.Group()
    pacman = Pacman("left", (360, 640), game_field)
    essences_sprite_group.add(pacman)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                process_key_pressed(event)

        pacman.move(clock.tick())

        screen.fill("black")
        game_field.render()
        essences_sprite_group.draw(screen)
        pygame.display.flip()

    pygame.quit()
