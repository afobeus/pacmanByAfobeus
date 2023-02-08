import random

import pygame

from game_field import GameField, Pellet, get_indexes_by_cords
import core


def move_essence(direction: str, distance_to_wall: int, distance: int,
                 object_rect: pygame.rect.Rect) -> pygame.rect.Rect:
    if direction == core.DIR_LEFT:
        new_rect = object_rect.move(max(-distance_to_wall, -distance), 0)
    elif direction == core.DIR_RIGHT:
        new_rect = object_rect.move(min(distance_to_wall, distance), 0)
    elif direction == core.DIR_UP:
        new_rect = object_rect.move(0, max(-distance_to_wall, -distance))
    else:
        new_rect = object_rect.move(0, min(distance_to_wall, distance))
    return new_rect


class Pacman(pygame.sprite.Sprite):
    ticks_to_move_1_px, ticks_to_update_animation = 10, 25
    direction_frames_indexes = {core.DIR_UP: 4, core.DIR_DOWN: 6, core.DIR_LEFT:0, core.DIR_RIGHT: 2}

    def __init__(self, start_direction: str, start_cords: tuple[int, int],
                 game_field: GameField, sprites_sheet: str) -> None:
        if start_direction not in [core.DIR_UP, core.DIR_DOWN, core.DIR_LEFT, core.DIR_RIGHT]:
            raise ValueError("Incorrect direction given")

        super().__init__()
        self.current_direction = start_direction
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

        distance_to_wall = self.game_field.min_distance_to_wall(self.current_direction, self.rect.x, self.rect.y)
        if distance_to_wall == 0 and self.next_direction is None:
            self.ticks_passed %= Pacman.ticks_to_move_1_px
            return

        if self.next_direction is not None:
            next_distance = self.game_field.min_distance_to_wall(self.next_direction, self.rect.x, self.rect.y)
            if next_distance > 0:
                self.current_direction = self.next_direction
                distance_to_wall = next_distance

        self.rect = move_essence(self.current_direction, distance_to_wall,
                                 self.ticks_passed // Pacman.ticks_to_move_1_px, self.rect)
        self.ticks_passed %= Pacman.ticks_to_move_1_px
        self.check_pellets()
        self.update_animation(ticks_passed)
        self.ex_cell = get_indexes_by_cords(self.rect.x, self.rect.y)

    def update_animation(self, ticks_passed: int) -> None:
        self.animation_ticks_passed += ticks_passed
        if self.animation_ticks_passed < Pacman.ticks_to_update_animation:
            return

        self.animation_state = (self.animation_state + 1) % (len(self.frames) // 4)
        self.image = self.frames[self.animation_state + Pacman.direction_frames_indexes[self.current_direction]]
        self.animation_ticks_passed %= Pacman.ticks_to_update_animation

    def check_pellets(self) -> None:
        start_row, start_col = self.ex_cell
        object_row, object_col = get_indexes_by_cords(self.rect.x, self.rect.y)

        if self.current_direction == core.DIR_UP:
            end_row = get_indexes_by_cords(self.rect.x, self.rect.y - 1)[0]
            for row in range(start_row, end_row, -1):
                pellet = self.game_field.pellets[row][object_col]
                if pellet is not None and not pellet.is_eaten():
                    self.eat_pellet(pellet)
        elif self.current_direction == core.DIR_DOWN:
            end_row = get_indexes_by_cords(self.rect.x, self.rect.y + GameField.cell_size + 1)[0]
            for row in range(start_row, end_row):
                pellet = self.game_field.pellets[row][object_col]
                if pellet is not None and not pellet.is_eaten():
                    self.eat_pellet(pellet)
        elif self.current_direction == core.DIR_LEFT:
            end_col = get_indexes_by_cords(self.rect.x - 1, self.rect.y)[1]
            for col in range(start_col, end_col, -1):
                pellet = self.game_field.pellets[object_row][col]
                if pellet is not None and not pellet.is_eaten():
                    self.eat_pellet(pellet)
        elif self.current_direction == core.DIR_RIGHT:
            end_col = get_indexes_by_cords(self.rect.x + GameField.cell_size + 1, self.rect.y)[1]
            for col in range(start_col, end_col):
                pellet = self.game_field.pellets[object_row][col]
                if pellet is not None and not pellet.is_eaten():
                    self.eat_pellet(pellet)

    def eat_pellet(self, pellet: Pellet) -> None:
        self.current_score += pellet.get_value()
        pellet.set_eaten(True)

    def get_score(self):
        return self.current_score

    def get_cords(self) -> tuple[int, int]:
        return self.rect.x, self.rect.y


class Ghost(pygame.sprite.Sprite):
    directions = [core.DIR_UP, core.DIR_DOWN, core.DIR_LEFT, core.DIR_RIGHT]
    ticks_to_move_1_px = 11

    def __init__(self, start_cords: tuple[int, int], game_field: GameField) -> None:
        super().__init__()
        self.game_field = game_field
        self.ticks_passed = 0
        self.last_cell_processed = None
        self.current_direction = core.DIR_UP
        self.image = core.load_image("ghost.png")
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = start_cords

    def get_random_way(self) -> tuple[str, int]:
        possible_ways = []
        for direction in Ghost.directions:
            distance = self.game_field.min_distance_to_wall(direction, self.rect.x, self.rect.y)
            if distance > 0:
                possible_ways.append((direction, distance))
        if len(possible_ways) == 1:
            return possible_ways[0]
        return random.choice([way for way in possible_ways if not core.opposite(way[0], self.current_direction)])

    def get_way_to_pacman(self, pacman: Pacman):
        object_x, object_y = self.rect.x, self.rect.y
        pacman_x, pacman_y = pacman.get_cords()
        for direction in Ghost.directions:
            distance_to_wall = self.game_field.min_distance_to_wall(direction, object_x, object_y)
            if direction == core.DIR_LEFT:
                distance_to_pacman = object_x - (pacman_x - GameField.cell_size)
                if object_y == pacman_y and 0 <= distance_to_pacman <= distance_to_wall:
                    return direction
            elif direction == core.DIR_RIGHT:
                distance_to_pacman = pacman_x - (object_x + GameField.cell_size)
                if object_y == pacman_y and 0 <= distance_to_pacman <= distance_to_wall:
                    return direction
            elif direction == core.DIR_UP:
                distance_to_pacman = object_y - (pacman_y + GameField.cell_size)
                if object_x == pacman_x and 0 <= distance_to_pacman <= distance_to_wall:
                    return direction
            elif direction == core.DIR_DOWN:
                distance_to_pacman = pacman_y - (object_y + GameField.cell_size)
                if object_x == pacman_x and 0 <= distance_to_pacman <= distance_to_wall:
                    return direction
        return None

    def move(self, ticks_passed: int, pacman: Pacman) -> None:
        self.ticks_passed += ticks_passed
        if self.ticks_passed < Ghost.ticks_to_move_1_px:
            return

        cur_cell = get_indexes_by_cords(self.rect.x, self.rect.y)
        way_to_pacman = self.get_way_to_pacman(pacman)
        if way_to_pacman is not None:
            direction = way_to_pacman
            distance_to_wall = self.game_field.min_distance_to_wall(direction, self.rect.x, self.rect.y)
        elif cur_cell != self.last_cell_processed:
            direction, distance_to_wall = self.get_random_way()
        else:
            direction, distance_to_wall = self.current_direction, \
                self.game_field.min_distance_to_wall(self.current_direction, self.rect.x, self.rect.y)
        if distance_to_wall == 0:
            direction, distance_to_wall = self.get_random_way()

        self.rect = move_essence(direction, distance_to_wall,
                                 self.ticks_passed // Ghost.ticks_to_move_1_px, self.rect)
        self.ticks_passed %= Ghost.ticks_to_move_1_px
        self.last_cell_processed = cur_cell
        self.current_direction = direction
