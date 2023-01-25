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

    def __init__(self) -> None:
        self.pygame_screen = None
        self.field_scheme = None

    def set_screen(self, pygame_screen: pygame.Surface):
        self.pygame_screen = pygame_screen

    def load_map_scheme(self, scheme_file_name: str) -> None:
        with open(scheme_file_name, 'r', encoding="utf-8") as input_file:
            data = input_file.read().split('\n')
        if not data:
            raise ValueError("Empty scheme file for game field")

        self.field_scheme = data
        self.width, self.height = max(map(len, self.field_scheme)), len(self.field_scheme)

    def get_screen_size(self) -> tuple[int, int]:
        if self.field_scheme is None:
            raise RuntimeError("Screen is not set yet")

        return self.width * GameField.CELL_SIZE, self.height * GameField.CELL_SIZE

    def render(self) -> None:
        print(self.field_scheme)
        for row in range(len(self.field_scheme)):
            for col in range(len(self.field_scheme[row])):
                if self.field_scheme[row][col] == '#':
                    pygame.draw.rect(self.pygame_screen, "blue",
                                     (GameField.CELL_SIZE * col, GameField.CELL_SIZE * row,
                                      GameField.CELL_SIZE, GameField.CELL_SIZE))
