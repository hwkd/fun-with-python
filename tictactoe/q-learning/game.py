import numpy as np

EMPTY = -1


class GameEnv:
    action_space: int = 9
    state_space: int = 19683

    def __init__(self) -> None:
        self.reset()

    def reset(self) -> int:
        self.player = 0
        self.gameover = False
        self.winner = None
        self.board = [[EMPTY for _ in range(3)] for _ in range(3)]
        self.legal_move = True
        return self.get_state()

    def make_move(self, position):
        i, j = divmod(position, 3)
        if self.board[i][j] != EMPTY:
            self.legal_move = False
        else:
            self.legal_move = True
            self.board[i][j] = self.player
        self.player = (self.player + 1) % 2
        self.gameover, self.winner = self.is_gameover()
        return self.get_state(), self.get_reward(), self.gameover

    def get_state(self):
        # Get the state as a single integer between 0 and 19683 that represents the board.
        state = 0
        for i in range(3):
            for j in range(3):
                state = state * 3 + self.board[i][j] + 1
        return state - 1

    def get_reward(self):
        # Heavily penalise illegal move.
        if not self.legal_move:
            return -1000
        if self.gameover:
            if self.winner is not None:
                # +20 when winning, and -10 when losing.
                return 50 if self.winner == 0 else -100
            # -5 when ending in a draw.
            return -5
        # Every move has a cost of -1.
        return -1

    def get_random_move(self):
        avail_moves = self.get_avail_moves()
        i = np.random.randint(0, len(avail_moves))
        return avail_moves[i]

    def get_avail_moves(self):
        avail_moves = []
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == EMPTY:
                    avail_moves.append(i * 3 + j)
        return avail_moves

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

    def display(self) -> None:
        rep = ""
        for i in range(3):
            for j in range(3):
                rep += str(self.board[i][j])
                if j != 2:
                    rep += " | "
            rep += "\n"
            if i != 2:
                rep += "---------\n"
        print(rep)
