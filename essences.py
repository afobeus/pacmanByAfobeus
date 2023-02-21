import random

import pygame

from game_field import GameField, Pellet, get_indexes_by_cords
import core


def new_cords(cords: list[int, int], direction: str, distance_to_wall: int,
              distance: int) -> list[int, int]:
    if direction == core.DIR_LEFT:
        cords[0] -= min(distance_to_wall, distance)
    elif direction == core.DIR_RIGHT:
        cords[0] += min(distance_to_wall, distance)
    elif direction == core.DIR_UP:
        cords[1] -= min(distance_to_wall, distance)
    else:
        cords[1] += min(distance_to_wall, distance)
    return cords


class Pacman(pygame.sprite.Sprite):
    ticks_to_move_1_px, ticks_to_update_animation = 8, 30
    direction_frames_indexes = {core.DIR_UP: 4, core.DIR_DOWN: 6, core.DIR_LEFT: 0, core.DIR_RIGHT: 2}

    def __init__(self, start_direction: str, start_cords: list[int, int],
                 game_field: GameField, sprites_sheet: str) -> None:
        if start_direction not in [core.DIR_UP, core.DIR_DOWN, core.DIR_LEFT, core.DIR_RIGHT]:
            raise ValueError("Incorrect direction given")

        super().__init__()
        self.current_direction = start_direction
        self.current_cords = start_cords
        self.next_direction = None
        self.game_field = game_field
        self.ticks_passed = 0
        self.animation_ticks_passed = 0
        self.ex_cell = get_indexes_by_cords(*start_cords)
        self.current_score = 0

        self.rect = pygame.Rect((start_cords[0], start_cords[1],
                                 GameField.cell_size, GameField.cell_size))
        self.cut_sheet(core.load_image(sprites_sheet))

    def cut_sheet(self, sheet) -> None:
        self.frames = []
        columns, rows = sheet.get_width() // GameField.cell_size,\
            sheet.get_height() // GameField.cell_size

        for j in range(rows):
            for i in range(columns):
                frame_location = (GameField.cell_size * i, GameField.cell_size * j)
                self.frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))
        self.animation_state = -1
        self.image = self.frames[Pacman.direction_frames_indexes[self.current_direction]]

    def change_direction(self, direction: str) -> None:
        if direction not in [core.DIR_UP, core.DIR_DOWN, core.DIR_LEFT, core.DIR_RIGHT]:
            raise ValueError("Incorrect direction given")
        self.next_direction = direction

    def move(self, ticks_passed: int) -> None:
        self.ticks_passed += ticks_passed
        if self.ticks_passed < Pacman.ticks_to_move_1_px:
            return

        distance_to_wall = self.game_field.min_distance_to_wall(self.current_direction, *self.current_cords)
        if distance_to_wall == 0 and self.next_direction is None:
            self.ticks_passed %= Pacman.ticks_to_move_1_px
            return

        if self.next_direction is not None:
            next_distance = self.game_field.min_distance_to_wall(self.next_direction, *self.current_cords)
            if next_distance > 0:
                self.current_direction = self.next_direction
                distance_to_wall = next_distance

        self.current_cords = new_cords(self.current_cords, self.current_direction, distance_to_wall,
                                       self.ticks_passed // Pacman.ticks_to_move_1_px)
        self.rect.x, self.rect.y = self.current_cords[0] + self.game_field.shift_x,\
            self.current_cords[1] + self.game_field.shift_y
        if distance_to_wall > 0:
            self.update_animation(ticks_passed)
            self.update_game_field_shift(self.ticks_passed)
        self.ticks_passed %= Pacman.ticks_to_move_1_px
        self.check_pellets()
        self.ex_cell = get_indexes_by_cords(*self.current_cords)

    def update_animation(self, ticks_passed: int) -> None:
        self.animation_ticks_passed += ticks_passed
        if self.animation_ticks_passed < Pacman.ticks_to_update_animation:
            return

        self.animation_state = (self.animation_state + 1) % (len(self.frames) // 4)
        self.image = self.frames[self.animation_state + Pacman.direction_frames_indexes[self.current_direction]]
        self.animation_ticks_passed %= Pacman.ticks_to_update_animation

    def update_game_field_shift(self, ticks_passed: int) -> None:
        self.game_field.update_shift(self.current_direction, ticks_passed // Ghost.ticks_to_move_1_px)

    def check_pellets(self) -> None:
        start_row, start_col = self.ex_cell
        object_row, object_col = get_indexes_by_cords(*self.current_cords)

        if self.current_direction == core.DIR_UP:

            end_row = get_indexes_by_cords(self.current_cords[0], self.current_cords[1] - 1)[0]
            for row in range(start_row, end_row, -1):
                pellet = self.game_field.pellets[row][object_col]
                if pellet is not None and not pellet.is_eaten():
                    self.eat_pellet(pellet)
        elif self.current_direction == core.DIR_DOWN:
            end_row = get_indexes_by_cords(self.current_cords[0], self.current_cords[1] + GameField.cell_size + 1)[0]
            for row in range(start_row, end_row):
                pellet = self.game_field.pellets[row][object_col]
                if pellet is not None and not pellet.is_eaten():
                    self.eat_pellet(pellet)
        elif self.current_direction == core.DIR_LEFT:
            end_col = get_indexes_by_cords(self.current_cords[0] - 1, self.current_cords[1])[1]
            for col in range(start_col, end_col, -1):
                pellet = self.game_field.pellets[object_row][col]
                if pellet is not None and not pellet.is_eaten():
                    self.eat_pellet(pellet)
        elif self.current_direction == core.DIR_RIGHT:
            end_col = get_indexes_by_cords(self.current_cords[0] + GameField.cell_size + 1, self.current_cords[1])[1]
            for col in range(start_col, end_col):
                pellet = self.game_field.pellets[object_row][col]
                if pellet is not None and not pellet.is_eaten():
                    self.eat_pellet(pellet)

    def eat_pellet(self, pellet: Pellet) -> None:
        if pellet.is_eaten():
            return

        self.current_score += pellet.get_value()
        pellet.set_eaten(True)
        if pellet.is_magic():
            self.game_field.set_magic_state()

    def get_score(self):
        return self.current_score

    def get_cords(self) -> list[int, int]:
        return self.current_cords


class Ghost(pygame.sprite.Sprite):
    directions = [core.DIR_UP, core.DIR_DOWN, core.DIR_LEFT, core.DIR_RIGHT]
    ticks_to_move_1_px = 9
    ticks_to_end_magic_state = 20_000

    def __init__(self, start_cords: list[int, int], game_field: GameField) -> None:
        super().__init__()
        self.game_field = game_field
        self.ticks_passed = 0
        self.last_cell_processed = None
        self.current_direction = core.DIR_UP
        self.current_cords = start_cords.copy()
        self.regular_image = core.load_image("ghost.png")
        self.blue_image = core.load_image("ghost_blue.png")
        self.image = self.regular_image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = start_cords
        self.start_cords = start_cords
        self.magic_state = False
        self.magic_state_ticks = 0

    def get_random_way(self) -> tuple[str, int]:
        possible_ways = []
        for direction in Ghost.directions:
            distance = self.game_field.min_distance_to_wall(direction, *self.current_cords)
            if distance > 0:
                possible_ways.append((direction, distance))
        if len(possible_ways) == 1:
            return possible_ways[0]
        return random.choice([way for way in possible_ways if not core.is_opposite(way[0], self.current_direction)])

    def get_way_to_pacman(self, pacman: Pacman):
        self_x, self_y = self.current_cords
        pacman_x, pacman_y = pacman.get_cords()
        for direction in Ghost.directions:
            distance_to_wall = self.game_field.min_distance_to_wall(direction, self_x, self_y)
            if direction == core.DIR_LEFT:
                distance_to_pacman = self_x - (pacman_x + GameField.cell_size)
                if self_y == pacman_y and 0 <= distance_to_pacman <= distance_to_wall:
                    return direction
            elif direction == core.DIR_RIGHT:
                distance_to_pacman = pacman_x - (self_x + GameField.cell_size)
                if self_y == pacman_y and 0 <= distance_to_pacman <= distance_to_wall:
                    return direction
            elif direction == core.DIR_UP:
                distance_to_pacman = self_y - (pacman_y + GameField.cell_size)
                if self_x == pacman_x and 0 <= distance_to_pacman <= distance_to_wall:
                    return direction
            elif direction == core.DIR_DOWN:
                distance_to_pacman = pacman_y - (self_y + GameField.cell_size)
                if self_x == pacman_x and 0 <= distance_to_pacman <= distance_to_wall:
                    return direction
        return None

    def move(self, ticks_passed: int, pacman: Pacman) -> None:
        self.ticks_passed += ticks_passed
        if self.ticks_passed < Ghost.ticks_to_move_1_px:
            return

        cur_cell = get_indexes_by_cords(*self.current_cords)
        way_to_pacman = self.get_way_to_pacman(pacman)
        if way_to_pacman is not None:
            if self.magic_state:
                direction = core.get_opposite(way_to_pacman)
            else:
                direction = way_to_pacman
            distance_to_wall = self.game_field.min_distance_to_wall(direction, *self.current_cords)
        elif cur_cell != self.last_cell_processed:
            direction, distance_to_wall = self.get_random_way()
        else:
            direction, distance_to_wall = self.current_direction, \
                self.game_field.min_distance_to_wall(self.current_direction, *self.current_cords)
        if distance_to_wall == 0:
            direction, distance_to_wall = self.get_random_way()

        self.current_direction = direction
        self.current_cords = new_cords(self.current_cords, self.current_direction, distance_to_wall,
                                       self.ticks_passed // Ghost.ticks_to_move_1_px)
        self.rect.x, self.rect.y = self.current_cords[0] + self.game_field.shift_x,\
            self.current_cords[1] + self.game_field.shift_y
        self.update_magic_state(ticks_passed)
        self.update_animation()
        self.ticks_passed %= Ghost.ticks_to_move_1_px
        self.last_cell_processed = cur_cell

    def update_animation(self):
        if self.magic_state:
            self.image = self.blue_image
        else:
            self.image = self.regular_image

    def reset_position(self):
        self.current_cords = self.start_cords.copy()
        self.magic_state = False

    def set_magic_state(self, new_state: bool) -> None:
        self.magic_state = new_state
        self.magic_state_ticks = 0

    def update_magic_state(self, ticks_passed: int) -> None:
        self.magic_state_ticks += ticks_passed
        if self.magic_state_ticks >= Ghost.ticks_to_end_magic_state:
            self.set_magic_state(False)
            self.magic_state_ticks %= Ghost.ticks_to_end_magic_state

    def is_in_magic_state(self) -> bool:
        return self.magic_state
