import pygame

import core


def get_indexes_by_cords(x: int, y: int) -> tuple[int, int]:
    return y // GameField.cell_size, x // GameField.cell_size


class Pellet:
    def __init__(self, value: int = 10, magic: bool = False) -> None:
        self.eaten = False
        self.value = value
        self.magic = magic

    def __repr__(self) -> str:
        return str(self.eaten)

    def set_eaten(self, eaten: bool) -> None:
        self.eaten = eaten

    def is_eaten(self) -> bool:
        return self.eaten

    def is_magic(self) -> bool:
        return self.magic

    def get_value(self) -> int:
        return self.value


class GameField:
    cell_size, cell_border_width = 40, 1
    standard_screen_size = 800, 800
    wall_border_color, cell_border_color = "blue", (63, 63, 252)
    pellet_color, pellet_radius = "yellow", 5
    magic_pellet_color, magic_pellet_radius = "yellow", 12

    def __init__(self) -> None:
        self.pygame_screen = None
        self.field_scheme = None

    def set_screen(self, pygame_screen: pygame.Surface) -> None:
        self.pygame_screen = pygame_screen

    def set_pacman(self, pacman) -> None:
        self.pacman = pacman

    def set_ghosts(self, ghosts: list) -> None:
        self.ghosts = ghosts

    def load_map_scheme(self, scheme_file_name: str) -> None:
        with open(scheme_file_name, 'r', encoding="utf-8") as input_file:
            data = input_file.read().split('\n')
        if not data:
            raise ValueError("Empty scheme file for game field")

        self.width, self.height = max(map(len, data)), len(data)
        self.screen_size = min(GameField.standard_screen_size[0], self.width * GameField.cell_size),\
            min(GameField.standard_screen_size[1], self.height * GameField.cell_size)
        self.field_scheme = list(map(lambda x: x.ljust(self.width, '.'), data))
        self.shift_x, self.shift_y = self.get_start_shifts()
        print(self.shift_x, self.shift_y)
        self.pellets = []
        for row in range(self.height):
            current_row = []
            for col in range(self.width):
                if self.field_scheme[row][col] == ' ':
                    current_row.append(Pellet())
                elif self.field_scheme[row][col] == '$':
                    current_row.append(Pellet(0, True))
                else:
                    current_row.append(None)
            self.pellets.append(current_row)

    def get_ghosts_cells(self) -> list[tuple[int, int]]:
        return [(row, col) for col in range(self.width) for row in range(self.height)
                if self.field_scheme[row][col] == '@']

    def get_pacman_cords(self) -> tuple[int, int]:
        for row in range(self.height):
            for col in range(self.width):
                if self.field_scheme[row][col] == '%':
                    return col * GameField.cell_size, row * GameField.cell_size

    def get_start_shifts(self) -> tuple[int, int]:
        pacman_cords = self.get_pacman_cords()
        shift_x = min(0, -pacman_cords[0] + self.screen_size[0] // 2)
        shift_y = min(0, -pacman_cords[1] + self.screen_size[1] // 2)
        return shift_x, shift_y

    def get_screen_size(self) -> tuple[int, int]:
        if self.field_scheme is None:
            raise RuntimeError("Screen is not set yet")
        return self.screen_size

    def distance_to_wall(self, direction: str, object_x: int, object_y: int) -> int:
        object_row, object_col = get_indexes_by_cords(object_x, object_y)
        result = 0
        if direction == core.DIR_LEFT:
            for col in range(object_col, -1, -1):
                if self.field_scheme[object_row][col] not in "*#":
                    result += 1
                else:
                    break
            return max(0, object_x - GameField.cell_size * (object_col - result + 1))
        elif direction == core.DIR_RIGHT:
            for col in range(object_col, self.width):
                if self.field_scheme[object_row][col] not in "*#":
                    result += 1
                else:
                    break
            return max(0, GameField.cell_size * (object_col + result + 1) - object_x - GameField.cell_size - 1)
        elif direction == core.DIR_UP:
            for row in range(object_row, -1, -1):
                if self.field_scheme[row][object_col] not in "*#":
                    result += 1
                else:
                    break
            return max(0, object_y - GameField.cell_size * (object_row - result + 1))
        elif direction == core.DIR_DOWN:
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
        shift_x, shift_y = self.shift_x, self.shift_y
        for row in range(len(self.field_scheme)):
            for col in range(len(self.field_scheme[row])):
                if self.field_scheme[row][col] == '#':
                    pygame.draw.rect(self.pygame_screen, GameField.wall_border_color,
                                     (GameField.cell_size * col + shift_x, GameField.cell_size * row + shift_y,
                                      GameField.cell_size, GameField.cell_size))
                elif self.field_scheme[row][col] == '*':
                    pygame.draw.rect(self.pygame_screen, GameField.cell_border_color,
                                     (GameField.cell_size * col + shift_x, GameField.cell_size * row + shift_y,
                                      GameField.cell_size, GameField.cell_size),
                                     GameField.cell_border_width)
        # deleting borders between neighbour wall cells
        for row in range(len(self.field_scheme)):
            for col in range(len(self.field_scheme[row])):
                if not self.field_scheme[row][col] == '*':
                    continue

                if col > 0 and self.field_scheme[row][col - 1] == '*':
                    pygame.draw.line(self.pygame_screen, "black",
                                     (GameField.cell_size * col + shift_x,
                                      GameField.cell_size * row + 1 + shift_y),
                                     (GameField.cell_size * col + shift_x,
                                      GameField.cell_size * (row + 1) - 2 + shift_y))
                if col < len(self.field_scheme[row]) - 1 and self.field_scheme[row][col + 1] == '*':
                    pygame.draw.line(self.pygame_screen, "black",
                                     (GameField.cell_size * (col + 1) - 1 + shift_x,
                                      GameField.cell_size * row + 1 + shift_y),
                                     (GameField.cell_size * (col + 1) - 1 + shift_x,
                                      GameField.cell_size * (row + 1) - 2 + shift_y), 1)
                if row > 0 and self.field_scheme[row - 1][col] == '*':
                    pygame.draw.line(self.pygame_screen, "black",
                                     (GameField.cell_size * col + 1 + shift_x,
                                      GameField.cell_size * row + shift_y),
                                     (GameField.cell_size * (col + 1) - 2 + shift_x,
                                      GameField.cell_size * row + shift_y))
                if row < self.height - 1 and self.field_scheme[row + 1][col] == '*':
                    pygame.draw.line(self.pygame_screen, "black",
                                     (GameField.cell_size * col + 1 + shift_x,
                                      GameField.cell_size * (row + 1) - 1 + shift_y),
                                     (GameField.cell_size * (col + 1) - 2 + shift_x,
                                      GameField.cell_size * (row + 1) - 1 + shift_y), 1)

        for row in range(self.height):
            for col in range(self.width):
                cur_object = self.pellets[row][col]
                if isinstance(cur_object, Pellet) and not cur_object.is_eaten():
                    if cur_object.is_magic():
                        color, radius = GameField.magic_pellet_color, GameField.magic_pellet_radius
                    else:
                        color, radius = GameField.pellet_color, GameField.pellet_radius
                    pygame.draw.circle(self.pygame_screen, color,
                                       (GameField.cell_size * col + GameField.cell_size / 2 + shift_x,
                                        GameField.cell_size * row + GameField.cell_size / 2 + shift_y), radius)

    def get_pellets_left(self) -> int:
        return sum(bool(self.pellets[row][col].get_value()) for row in range(self.height) for col in range(self.width)
                   if self.pellets[row][col] is not None and not self.pellets[row][col].is_eaten())

    def set_magic_state(self) -> None:
        for ghost in self.ghosts:
            ghost.set_magic_state(True)

    def update_shift(self, direction: str, pixels: int) -> None:
        if direction == core.DIR_UP:
            self.shift_y = min(0, self.shift_y + pixels)
        elif direction == core.DIR_DOWN:
            self.shift_y = max(-self.height * GameField.cell_size + self.screen_size[1], self.shift_y - pixels)
        elif direction == core.DIR_LEFT:
            self.shift_x = min(0, self.shift_x + pixels)
        elif direction == core.DIR_RIGHT:
            self.shift_x = max(-self.width * GameField.cell_size + self.screen_size[0], self.shift_x - pixels)
