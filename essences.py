import os
import pygame

from game_field import GameField


def load_image(name: str) -> pygame.image:
    fullname = os.path.join("", name)
    if not os.path.isfile(fullname):
        raise ValueError(f"No image with name '{fullname}' found")

    image = pygame.image.load(fullname)
    return image


class Pacman(pygame.sprite.Sprite):
    def __init__(self, start_direction: str, start_cords: tuple[int, int], game_field: GameField) -> None:
        if start_direction not in ["left", "right", "up", "down"]:
            raise ValueError("Incorrect direction given")

        super().__init__()
        self.current_direction = start_direction
        self.game_field = game_field
        self.ticks_passed = 0

        self.image = load_image("packman.png")
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = start_cords

    def change_direction(self, direction: str) -> None:
        if direction not in ["left", "right", "up", "down"]:
            raise ValueError("Incorrect direction given")
        self.current_direction = direction

    def move(self, ticks_passed: int) -> None:
        self.ticks_passed += ticks_passed
        if self.ticks_passed < 20:
            return

        distance_to_wall = self.game_field.min_distance_to_wall(self.current_direction, self.rect.x, self.rect.y)
        if distance_to_wall == 0:
            self.ticks_passed %= 20
            return

        if self.current_direction == "left":
            self.rect = self.rect.move(max(-distance_to_wall, -self.ticks_passed // 20), 0)
        elif self.current_direction == "right":
            self.rect = self.rect.move(min(distance_to_wall, self.ticks_passed // 20), 0)
        elif self.current_direction == "up":
            self.rect = self.rect.move(0, max(-distance_to_wall, -self.ticks_passed // 20))
        else:
            self.rect = self.rect.move(0, min(distance_to_wall, self.ticks_passed // 20))

        self.ticks_passed %= 20
