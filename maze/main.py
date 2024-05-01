#!/usr/bin/env python3

from random import randint
from collections import defaultdict

PATH = " "
WALL = "\u25FC"


class Maze:
    num_of_rows: int
    num_of_cols: int
    maze: list[list[str]]
    visited: list[list[str]]
    rooms: dict[str, int]
    room_char: str = "a"

    def __init__(self, rows: int = 20, cols: int = 20) -> None:
        self.num_of_rows = rows
        self.num_of_cols = cols
        self.generate_maze()
        self.rooms = defaultdict(int)
        self.init_visited()

    def generate_maze(self):
        self.maze = []
        for i in range(self.num_of_rows):
            self.maze.append([PATH for _ in range(self.num_of_cols)])
            for j in range(self.num_of_cols):
                if randint(0, 2) != 0:
                    self.maze[i][j] = PATH
                else:
                    self.maze[i][j] = WALL

    def init_visited(self):
        self.visited = []
        for i in range(self.num_of_rows):
            self.visited.append([PATH for _ in range(self.num_of_cols)])
            for j in range(self.num_of_cols):
                if randint(0, 1) == 0:
                    self.visited[i][j] = None
                else:
                    self.visited[i][j] = WALL

    def display(self):
        for i in range(self.num_of_rows):
            for j in range(self.num_of_cols):
                print(self.maze[i][j], end=" ")
            print()
        print()

    def display_visited(self):
        for i in range(self.num_of_rows):
            for j in range(self.num_of_cols):
                print(self.visited[i][j], end=" ")
            print()
        print()

    def calc_room_sizes(self) -> list[int]:
        for i in range(self.num_of_rows):
            for j in range(self.num_of_cols):
                size = self.room_size(i, j)
                if size > 0:
                    self.rooms[self.room_char] = size
                    self.next_room_char()

    def room_size(self, row, col) -> int:
        if min(row, col) < 0 or max(row, col) >= self.num_of_rows:
            return 0

        cell = self.visited[row][col]
        if (cell is WALL) or (cell is not None):
            return 0

        self.visited[row][col] = self.room_char
        size = 1
        size += self.room_size(row - 1, col)
        size += self.room_size(row + 1, col)
        size += self.room_size(row, col - 1)
        size += self.room_size(row, col + 1)
        return size

    def next_room_char(self) -> str:
        c = ord(self.room_char) + 1
        if c > 122:
            c = 65
        self.room_char = chr(c)
        return self.room_char


def main():
    m = Maze(25, 25)
    m.display()
    m.calc_room_sizes()
    m.display_visited()
    for k, v in m.rooms.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
