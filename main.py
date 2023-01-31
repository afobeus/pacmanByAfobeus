import time

import pygame
from game_field import GameField
from essences import Pacman, Ghost
import directions


def process_key_pressed(event):
    if event.key == pygame.K_LEFT:
        pacman.change_direction(directions.DIR_LEFT)
    elif event.key == pygame.K_RIGHT:
        pacman.change_direction(directions.DIR_RIGHT)
    elif event.key == pygame.K_UP:
        pacman.change_direction(directions.DIR_UP)
    elif event.key == pygame.K_DOWN:
        pacman.change_direction(directions.DIR_DOWN)


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
    pacman = Pacman(directions.DIR_LEFT, (360, 640), game_field)
    essences_sprite_group.add(pacman)
    red_ghost = Ghost((360, 400), game_field)
    essences_sprite_group.add(red_ghost)
    new_ghost = Ghost((360, 400), game_field)
    essences_sprite_group.add(new_ghost)
    new_ghost_2 = Ghost((360, 400), game_field)
    essences_sprite_group.add(new_ghost_2)

    while running:
        # time.sleep(0.05)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                process_key_pressed(event)

        ticks_passed = clock.tick()
        pacman.move(ticks_passed)
        red_ghost.move(ticks_passed)
        new_ghost.move(ticks_passed)
        new_ghost_2.move(ticks_passed)

        screen.fill("black")
        game_field.render()
        essences_sprite_group.draw(screen)
        pygame.display.flip()

    pygame.quit()
