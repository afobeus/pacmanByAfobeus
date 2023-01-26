import os
import pygame


def load_image(name: str) -> pygame.image:
    fullname = os.path.join("", name)
    if not os.path.isfile(fullname):
        raise ValueError(f"No image with name '{fullname}' found")

    image = pygame.image.load(fullname)
    return image


class Packman(pygame.sprite.Sprite):
    def __init__(self, start_direction, start_cords) -> None:
        super().__init__()
        self.current_direction = start_direction
        self.current_cords = start_cords
        self.image = load_image("packman.png")
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.current_cords
        self.ticks_passed = 0

    def change_direction(self, direction: str) -> None:
        if direction not in ["left", "right", "up", "down"]:
            raise ValueError("Incorrect direction given")
        self.current_direction = direction

    def move(self, ticks_passed: int) -> None:
        self.ticks_passed += ticks_passed
        if self.ticks_passed < 20:
            return

        if self.current_direction == "left":
            self.rect = self.rect.move(-self.ticks_passed // 20, 0)
            self.ticks_passed %= 20
