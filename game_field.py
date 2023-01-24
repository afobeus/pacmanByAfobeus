import pygame
import os


def load_image(name: str) -> pygame.image:
    fullname = os.path.join("pictures", name)
    if not os.path.isfile(fullname):
        raise ValueError(f"No image with name '{fullname}' found")

    image = pygame.image.load(fullname)
    return image


class GameField:
    def __init__(self, pygame_screen: pygame.Surface) -> None:
        self.pygame_screen = pygame_screen

    def load_map_scheme(self, scheme_file_name: str) -> None:
        with open(scheme_file_name, 'r', encoding="utf-8") as input_file:
            data = input_file.readlines()
        if not data:
            raise ValueError("Empty scheme file for game field")

        self.field_scheme = [[symbol for symbol in line[:-1]] for line in data]

    def render(self) -> None:
        pass
