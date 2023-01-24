import pygame
import os


def load_image(name: str) -> pygame.image:
    fullname = os.path.join("pictures", name)
    if not os.path.isfile(fullname):
        raise ValueError(f"No image with name '{fullname}' found")

    image = pygame.image.load(fullname)
    return image


class GameField:
    CELL_SIZE = 40

    def __init__(self, pygame_screen: pygame.Surface) -> None:
        self.pygame_screen = pygame_screen

    def load_map_scheme(self, scheme_file_name: str) -> None:
        with open(scheme_file_name, 'r', encoding="utf-8") as input_file:
            data = input_file.readlines()
        if not data:
            raise ValueError("Empty scheme file for game field")

        self.field_scheme = [[symbol for symbol in line[:-1]] for line in data]

    def get_field_size(self) -> tuple[int, int]:
        width, height = len(self.field_scheme[0]), len(self.field_scheme)
        return width, height

    def render(self) -> None:
        for row in range(len(self.field_scheme)):
            for col in range(len(self.field_scheme[0])):
                if self.field_scheme[row][col] == '*':
                    pygame.draw.rect(self.pygame_screen, "blue",
                                     (GameField.CELL_SIZE * row, GameField.CELL_SIZE * col,
                                      GameField.CELL_SIZE, GameField.CELL_SIZE))
