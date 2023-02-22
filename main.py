import sys
import pygame

from game_field import GameField
from essences import Pacman, Ghost
import core


LEVELS_FILES = ["original level.txt", "level 2.txt"]


def info_screen(text: list, screen: pygame.Surface) -> int:
    width, height = screen.get_size()
    background = pygame.transform.scale(core.load_image("start_screen.png"), (width, height))
    screen.blit(background, (0, 0))
    text_font = pygame.font.Font(None, 50)
    current_text_y = 30  # 30 is start height for intro text
    for line in text:
        string_rendered = text_font.render(line, True, pygame.Color('white'))
        text_rect = string_rendered.get_rect()
        current_text_y += 10
        text_rect.top = current_text_y
        text_rect.x = width // 2 - text_rect.width // 2
        current_text_y += text_rect.height
        screen.blit(string_rendered, text_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 1
                elif event.key == pygame.K_2:
                    return 2
        pygame.display.flip()


def process_key_pressed(event, pacman: Pacman):
    if event.key == pygame.K_LEFT:
        pacman.change_direction(core.DIR_LEFT)
    elif event.key == pygame.K_RIGHT:
        pacman.change_direction(core.DIR_RIGHT)
    elif event.key == pygame.K_UP:
        pacman.change_direction(core.DIR_UP)
    elif event.key == pygame.K_DOWN:
        pacman.change_direction(core.DIR_DOWN)


def render_score(screen: pygame.Surface, pacman: Pacman) -> None:
    font = pygame.font.Font(None, 50)
    text = font.render("Score: " + str(pacman.get_score()), True, (100, 255, 100))
    screen.blit(text, (0, 0))


def start_game(show_start_screen=True, level_index=0):
    screen = pygame.display.set_mode((800, 800))
    if show_start_screen:
        level_index = info_screen(["Pacman", "by afobeus", "", "press 1 or 2", "to chose level"], screen)
    clock = pygame.time.Clock()
    game_field = GameField()
    game_field.load_map_scheme(LEVELS_FILES[level_index - 1])
    screen = pygame.display.set_mode(game_field.get_screen_size())
    game_field.set_screen(screen)

    essences_sprite_group = pygame.sprite.Group()
    pacman = Pacman(core.DIR_LEFT, game_field.get_pacman_cords(), game_field, "pacman_sprite_sheet.png")
    game_field.set_pacman(pacman)
    essences_sprite_group.add(pacman)
    ghosts = [Ghost([GameField.cell_size * col, GameField.cell_size * row], game_field)
              for row, col in game_field.get_ghosts_cells()]
    game_field.set_ghosts(ghosts)
    for ghost in ghosts:
        essences_sprite_group.add(ghost)

    clock.tick()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0
            elif event.type == pygame.KEYDOWN:
                process_key_pressed(event, pacman)

        if game_field.get_pellets_left() == 0:
            level_choice = info_screen(["You win!", f"Your score: {pacman.get_score()}" "",
                                       "press 1 or 2", "to chose level"], screen)
            return level_choice

        for ghost in ghosts:
            if pygame.sprite.collide_mask(pacman, ghost):
                if ghost.is_in_magic_state():
                    ghost.reset_position()
                else:
                    level_choice = info_screen(["You lose", f"Your score: {pacman.get_score()}", "",
                                               "press 1 or 2", "to chose level"], screen)
                    return level_choice

        ticks_passed = clock.tick()

        pacman.move(ticks_passed)
        for ghost in ghosts:
            ghost.move(ticks_passed, pacman)
            ghost.update_magic_state(ticks_passed)

        screen.fill("black")
        game_field.render()
        essences_sprite_group.draw(screen)
        render_score(screen, pacman)
        pygame.display.flip()


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption("Pacman")
    game_exit_code = start_game(True)
    while game_exit_code in (1, 2):
        game_exit_code = start_game(False, game_exit_code)

    pygame.quit()
