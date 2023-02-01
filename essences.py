import os
import random

import pygame

from game_field import GameField, get_indexes_by_cords
import directions


def load_image(name: str) -> pygame.image:
    fullname = os.path.join("", name)
    if not os.path.isfile(fullname):
        raise ValueError(f"No image with name '{fullname}' found")

    image = pygame.image.load(fullname)
    return image


def move_essence(direction: str, distance_to_wall: int, distance: int,
                 object_rect: pygame.rect.Rect) -> pygame.rect.Rect:
    if direction == directions.DIR_LEFT:
        new_rect = object_rect.move(max(-distance_to_wall, -distance), 0)
    elif direction == directions.DIR_RIGHT:
        new_rect = object_rect.move(min(distance_to_wall, distance), 0)
    elif direction == directions.DIR_UP:
        new_rect = object_rect.move(0, max(-distance_to_wall, -distance))
    else:
        new_rect = object_rect.move(0, min(distance_to_wall, distance))
    return new_rect


class Pacman(pygame.sprite.Sprite):
    ticks_to_move_1_px = 14

    def __init__(self, start_direction: str, start_cords: tuple[int, int], game_field: GameField) -> None:
        if start_direction not in [directions.DIR_UP, directions.DIR_DOWN,
                                   directions.DIR_LEFT, directions.DIR_RIGHT]:
            raise ValueError("Incorrect direction given")

        super().__init__()
        self.current_direction = start_direction
        self.next_direction = None
        self.game_field = game_field
        self.ticks_passed = 0

        self.image = load_image("packman.png")
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = start_cords

    def change_direction(self, direction: str) -> None:
        if direction not in [directions.DIR_UP, directions.DIR_DOWN,
                             directions.DIR_LEFT, directions.DIR_RIGHT]:
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


class Ghost(pygame.sprite.Sprite):
    directions = [directions.DIR_UP, directions.DIR_DOWN, directions.DIR_LEFT, directions.DIR_RIGHT]
    ticks_to_move_1_px = 13

    def __init__(self, start_cords: tuple[int, int], game_field: GameField) -> None:
        super().__init__()
        self.game_field = game_field
        self.ticks_passed = 0
        self.last_cell_processed = None
        self.current_direction = directions.DIR_UP
        self.image = load_image("ghost.png")
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = start_cords

    def get_random_way(self):
        possible_ways = []
        for direction in Ghost.directions:
            distance = self.game_field.min_distance_to_wall(direction, self.rect.x, self.rect.y)
            if distance > 0:
                possible_ways.append((direction, distance))
        if len(possible_ways) == 1:
            return possible_ways[0]
        return random.choice([way for way in possible_ways if not directions.opposite(way[0], self.current_direction)])

    def move(self, ticks_passed: int) -> None:
        self.ticks_passed += ticks_passed
        if self.ticks_passed < Ghost.ticks_to_move_1_px:
            return

        cur_cell = get_indexes_by_cords(self.rect.x, self.rect.y)
        if cur_cell != self.last_cell_processed or self.current_direction is None:
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
