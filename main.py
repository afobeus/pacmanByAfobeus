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


def render_score() -> None:
    font = pygame.font.Font(None, 50)
    text = font.render("Score: " + str(pacman.get_score()), True, (100, 255, 100))
    text_x = 0
    text_y = (game_field.height + 1) * GameField.cell_size - 35
    screen.blit(text, (text_x, text_y))


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
    ghosts = [Ghost((GameField.cell_size * col, GameField.cell_size * row), game_field)
              for row, col in game_field.get_ghosts_cells()]
    for ghost in ghosts:
        essences_sprite_group.add(ghost)

    while running:
        # time.sleep(1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                process_key_pressed(event)

        ticks_passed = clock.tick()
        pacman.move(ticks_passed)
        for ghost in ghosts:
            ghost.move(ticks_passed, pacman)

        screen.fill("black")
        game_field.render()
        essences_sprite_group.draw(screen)
        render_score()
        pygame.display.flip()

    pygame.quit()
