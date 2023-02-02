import pygame

import directions


def get_indexes_by_cords(x: int, y: int) -> tuple[int, int]:
    return y // GameField.cell_size, x // GameField.cell_size


class Pellet:
    def __init__(self, value: int = 10) -> None:
        self.eaten = False
        self.value = value

    def __repr__(self) -> str:
        return str(self.eaten)

    def set_eaten(self, eaten: bool) -> None:
        self.eaten = eaten

    def is_eaten(self) -> bool:
        return self.eaten

    def get_value(self) -> int:
        return self.value


class GameField:
    cell_size, cell_border_width = 40, 1
    wall_border_color, cell_border_color = "blue", (63, 63, 252)
    pellet_color, pellet_radius = "yellow", 7

    def __init__(self) -> None:
        self.pygame_screen = None
        self.field_scheme = None

    def set_screen(self, pygame_screen: pygame.Surface) -> None:
        self.pygame_screen = pygame_screen

    def load_map_scheme(self, scheme_file_name: str) -> None:
        with open(scheme_file_name, 'r', encoding="utf-8") as input_file:
            data = input_file.read().split('\n')
        if not data:
            raise ValueError("Empty scheme file for game field")

        self.width, self.height = max(map(len, data)), len(data)
        self.field_scheme = list(map(lambda x: x.ljust(self.width, '.'), data))
        self.pellets = [[Pellet() if self.field_scheme[row][col] == ' ' else None for col in range(self.width)]
                        for row in range(self.height)]

    def get_screen_size(self) -> tuple[int, int]:
        if self.field_scheme is None:
            raise RuntimeError("Screen is not set yet")

        return self.width * GameField.cell_size, self.height * GameField.cell_size

    def distance_to_wall(self, direction: str, object_x: int, object_y: int) -> int:
        object_row, object_col = get_indexes_by_cords(object_x, object_y)
        result = 0
        if direction == directions.DIR_LEFT:
            for col in range(object_col, -1, -1):
                if self.field_scheme[object_row][col] not in "*#":
                    result += 1
                else:
                    break
            return max(0, object_x - GameField.cell_size * (object_col - result + 1))
        elif direction == directions.DIR_RIGHT:
            for col in range(object_col, self.width):
                if self.field_scheme[object_row][col] not in "*#":
                    result += 1
                else:
                    break
            return max(0, GameField.cell_size * (object_col + result + 1) - object_x - GameField.cell_size - 1)
        elif direction == directions.DIR_UP:
            for row in range(object_row, -1, -1):
                if self.field_scheme[row][object_col] not in "*#":
                    result += 1
                else:
                    break
            return max(0, object_y - GameField.cell_size * (object_row - result + 1))
        elif direction == directions.DIR_DOWN:
            for row in range(object_row, self.height):
                if self.field_scheme[row][object_col] not in "*#":
                    result += 1
                else:
                    break
            return max(0, GameField.cell_size * (object_row + result + 1) - object_y - GameField.cell_size - 1)

    def min_distance_to_wall(self, direction: str, object_x: int, object_y: int) -> int:
        packman_rectangle_vertexes = [(object_x, object_y), (object_x + GameField.cell_size - 1, object_y),
                                      (object_x, object_y + GameField.cell_size - 1),
                                      (object_x + GameField.cell_size - 1, object_y + GameField.cell_size - 1)]
        return min(self.distance_to_wall(direction, *vertex) for vertex in packman_rectangle_vertexes)

    def render(self) -> None:
        if self.field_scheme is None or self.pygame_screen is None:
            raise RuntimeError("Unable to render game field, because field scheme or"
                               "pygame screen are not set")

        # drawing rectangles like walls borders
        for row in range(len(self.field_scheme)):
            for col in range(len(self.field_scheme[row])):
                if self.field_scheme[row][col] == '#':
                    pygame.draw.rect(self.pygame_screen, GameField.wall_border_color,
                                     (GameField.cell_size * col, GameField.cell_size * row,
                                      GameField.cell_size, GameField.cell_size))
                elif self.field_scheme[row][col] == '*':
                    pygame.draw.rect(self.pygame_screen, GameField.cell_border_color,
                                     (GameField.cell_size * col, GameField.cell_size * row,
                                      GameField.cell_size, GameField.cell_size),
                                     GameField.cell_border_width)
        # deleting borders between neighbour wall cells
        for row in range(len(self.field_scheme)):
            for col in range(len(self.field_scheme[row])):
                if not self.field_scheme[row][col] == '*':
                    continue

                if col > 0 and self.field_scheme[row][col - 1] == '*':
                    pygame.draw.line(self.pygame_screen, "black",
                                     (GameField.cell_size * col, GameField.cell_size * row + 1),
                                     (GameField.cell_size * col,
                                      GameField.cell_size * (row + 1) - 2))
                if col < len(self.field_scheme[row]) - 1 and self.field_scheme[row][col + 1] == '*':
                    pygame.draw.line(self.pygame_screen, "black",
                                     (GameField.cell_size * (col + 1) - 1,
                                      GameField.cell_size * row + 1),
                                     (GameField.cell_size * (col + 1) - 1,
                                      GameField.cell_size * (row + 1) - 2), 1)
                if row > 0 and self.field_scheme[row - 1][col] == '*':
                    pygame.draw.line(self.pygame_screen, "black",
                                     (GameField.cell_size * col + 1, GameField.cell_size * row),
                                     (GameField.cell_size * (col + 1) - 2,
                                      GameField.cell_size * row))
                if row < self.height - 1 and self.field_scheme[row + 1][col] == '*':
                    pygame.draw.line(self.pygame_screen, "black",
                                     (GameField.cell_size * col + 1,
                                      GameField.cell_size * (row + 1) - 1),
                                     (GameField.cell_size * (col + 1) - 2,
                                      GameField.cell_size * (row + 1) - 1), 1)

        for row in range(self.height):
            for col in range(self.width):
                if isinstance(self.pellets[row][col], Pellet) and not self.pellets[row][col].is_eaten():
                    pygame.draw.circle(self.pygame_screen, GameField.pellet_color,
                                       (GameField.cell_size * col + GameField.cell_size / 2,
                                        GameField.cell_size * row + GameField.cell_size / 2), GameField.pellet_radius)

