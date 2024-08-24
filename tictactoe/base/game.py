EMPTY = " "


class Game:
    symbols: list[str] = ["O", "X"]

    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self.board = [[EMPTY for _ in range(3)] for _ in range(3)]

    def start(self) -> None:
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

    def display(self) -> None:
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

    def next_move(self, turn: int) -> tuple[int, int]:
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

    def place(self, symbol: str, move: tuple[int, int]):
        i, j = move
        self.board[i][j] = symbol

    def is_gameover(self):
        b = self.board
        full = True
        for i in range(3):
            for j in range(3):
                if b[i][j] == EMPTY:
                    full = False

        for i in range(3):
            if b[i][0] == b[i][1] == b[i][2] != EMPTY:
                return True, b[i][0]
            if b[0][i] == b[1][i] == b[2][i] != EMPTY:
                return True, b[0][i]

        if b[0][0] == b[1][1] == b[2][2] != EMPTY:
            return True, b[0][0]
        if b[2][0] == b[1][1] == b[0][2] != EMPTY:
            return True, b[2][0]

        return full, None
