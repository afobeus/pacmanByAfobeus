import time

import sys
import pygame
from game_field import GameField
from essences import Pacman, Ghost
import core


def start_screen():
    intro_text = ["Pacman", "by afobeus", "",
                  "Press any key",
                  "to start"]

    width, height = screen.get_size()
    background = pygame.transform.scale(core.load_image("start_screen.png"), (width, height))
    screen.blit(background, (0, 0))
    font = pygame.font.Font(None, 50)
    current_text_y = 30
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        current_text_y += 10
        intro_rect.top = current_text_y
        intro_rect.x = width / 2 - intro_rect.width / 2
        current_text_y += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()


def process_key_pressed(event):
    if event.key == pygame.K_LEFT:
        pacman.change_direction(core.DIR_LEFT)
    elif event.key == pygame.K_RIGHT:
        pacman.change_direction(core.DIR_RIGHT)
    elif event.key == pygame.K_UP:
        pacman.change_direction(core.DIR_UP)
    elif event.key == pygame.K_DOWN:
        pacman.change_direction(core.DIR_DOWN)


def render_score() -> None:
    font = pygame.font.Font(None, 50)
    text = font.render("Score: " + str(pacman.get_score()), True, (100, 255, 100))
    text_x = 0
    text_y = (game_field.height + 1) * GameField.cell_size - 35
    screen.blit(text, (text_x, text_y))


def pacman_collides_ghost() -> bool:
    for ghost in ghosts:
        if pygame.sprite.collide_mask(pacman, ghost):
            return True
    return False


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption("Pacman")
    clock = pygame.time.Clock()
    running = True

    game_field = GameField()
    game_field.load_map_scheme("original level.txt")
    screen = pygame.display.set_mode(game_field.get_screen_size())
    game_field.set_screen(screen)
    start_screen()

    essences_sprite_group = pygame.sprite.Group()
    pacman = Pacman(core.DIR_LEFT, (360, 640), game_field)
    essences_sprite_group.add(pacman)
    ghosts = [Ghost((GameField.cell_size * col, GameField.cell_size * row), game_field)
              for row, col in game_field.get_ghosts_cells()]
    for ghost in ghosts:
        essences_sprite_group.add(ghost)

    clock.tick()
    while running:
        # time.sleep(1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                process_key_pressed(event)

        if pacman_collides_ghost():
            print("be")

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
