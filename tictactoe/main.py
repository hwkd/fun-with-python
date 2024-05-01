#!/usr/bin/env python3

import sys
import signal

EMPTY = " "


class Game:
    symbols = ["O", "X"]

    def __init__(self) -> None:
        self.board = []
        for i in range(3):
            self.board.append([])
            for j in range(3):
                self.board[i].append(EMPTY)

    def start(self):
        self.display()
        turn = 1
        gameover = False
        winner = None
        while not gameover:
            turn = (turn + 1) % 2
            move = self.next_move(turn)
            self.place(self.symbols[turn], move)
            self.display()
            gameover, winner = self.is_gameover()
        print(f"Winner: {winner}")

    def display(self):
        rep = ""
        for i in range(3):
            for j in range(3):
                rep += self.board[i][j]
                if j != 2:
                    rep += " | "
            rep += "\n"
            if i != 2:
                rep += "---------\n"
        print(rep)

    def next_move(self, turn: int) -> tuple[int,int]:
        while True:
            try:
                move = int(input(f"Player {turn + 1}: "))
                if 0 <= move <= 8:
                    move = int(move)
                    i, j = divmod(move, 3) 
                    if self.board[i][j] != EMPTY:
                        raise ValueError("Illegal move. Already occupied.")
                    return i, j
                else:
                    raise ValueError
            except ValueError as e:
                if e.args:
                    print(e.args[0])
                else:
                    print("Invalid move. Place between 0 and 8.")

    def place(self, symbol, move):
        i, j = move 
        self.board[i][j] = symbol

    def is_gameover(self):
        b = self.board
        full = True
        for i in range(3):
            for j in range(3):
                if b[i][j] == EMPTY:
                    full = False

        if b[0][0] == b[0][1] == b[0][2] != EMPTY:
            return True, b[0][0]
        if b[1][0] == b[1][1] == b[1][2] != EMPTY:
            return True, b[1][0]
        if b[2][0] == b[2][1] == b[2][2] != EMPTY:
            return True, b[2][0]
        if b[0][0] == b[1][0] == b[2][0] != EMPTY:
            return True, b[0][0]
        if b[0][1] == b[1][1] == b[2][1] != EMPTY:
            return True, b[0][1]
        if b[0][2] == b[1][2] == b[2][2] != EMPTY:
            return True, b[0][2]
        if b[0][0] == b[1][1] == b[2][2] != EMPTY:
            return True, b[0][0]
        if b[2][0] == b[1][1] == b[0][2] != EMPTY:
            return True, b[2][0]
        return full, None

def main():
    Game().start()


if __name__ == "__main__":
    signal.signal(signal.SIGINT, lambda _x, _y: sys.exit(0))
    main()
