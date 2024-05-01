#!/usr/bin/env python3

import signal
import sys
import time
import random

EMPTY_PIECE = "  "
PIECE = "\u25FE"


class Board:
    num_of_cols: int
    num_of_rows: int
    board: list[list[int]] = []

    def __init__(self, cols: int = 20, rows: int = 20) -> None:
        self.num_of_cols = cols
        self.num_of_rows = rows
        self.init_board(self.board)
        self.place_pieces_randomly()

    def init_board(self, board: list[list[str]]) -> None:
        for i in range(self.num_of_cols):
            board.append([])
            for _ in range(self.num_of_rows):
                board[i].append(EMPTY_PIECE)

    def place_pieces_randomly(self) -> None:
        for i in range(self.num_of_cols):
            for j in range(self.num_of_rows):
                r = random.randint(0, 2)
                if r == 0:
                    self.board[i][j] = EMPTY_PIECE
                else:
                    self.board[i][j] = PIECE

    def display(self) -> None:
        for i in range(self.num_of_cols):
            if i == 0:
                print("Conway's Game of Life:")
            else:
                print()
            for j in range(self.num_of_rows):
                print(self.board[i][j], end="")
        print(end="\n\n")

    def count_neighbours(self, row: int, col: int) -> int:
        neighbours = 0
        for i in range(-1, 2):
            if row == 0:
                y = self.num_of_rows - 1
            elif row == self.num_of_rows - 1:
                y = 0
            else:
                y = row + i
            for j in range(-1, 2):
                if col == 0:
                    x = self.num_of_cols - 1
                elif col == self.num_of_cols - 1:
                    x = 0
                else:
                    x = col + j
                if row == y and col == x:
                    continue
                if self.board[y][x] != EMPTY_PIECE:
                    neighbours += 1
        return neighbours

    def run(self):
        next_board: list[list[int]] = []
        self.init_board(next_board)
        for i in range(self.num_of_rows):
            for j in range(self.num_of_cols):
                neighbours = self.count_neighbours(i, j)
                if neighbours == 3:
                    next_board[i][j] = PIECE
                elif 2 <= neighbours <= 3:
                    next_board[i][j] = self.board[i][j]
                else:
                    next_board[i][j] = EMPTY_PIECE
        self.board = next_board


def main():
    board = Board(40, 40)
    board.display()
    while True:
        board.run()
        board.display()
        time.sleep(0.2)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, lambda _x, _y: sys.exit(0))
    main()
