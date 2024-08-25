import sys
import signal
import numpy as np

from game import GameEnv
from train import train


def main():
    print("Training the agent...")
    q_table = train(show_results=True)
    print("Training done.\n")

    env = GameEnv()
    env.display()

    state = env.reset()
    while True:
        # Agent's move.
        position = np.argmax(q_table[state, :])
        env.make_move(position)
        print("Agent made a move:", position)
        env.display()
        if check_gameover(env):
            break

        # Human's move.
        position = int(input("Enter your move: "))
        next_state, _, _ = env.make_move(position)
        print("You made a move:", position)
        env.display()
        if check_gameover(env):
            break

        state = next_state


def check_gameover(env):
    if env.gameover:
        print("Gameover.")
        if env.winner is not None:
            print("Winner:", "Agent" if env.winner == 0 else "Human")
        else:
            print("Draw.")
        return True


if __name__ == "__main__":
    signal.signal(signal.SIGINT, lambda _x, _y: sys.exit(0))
    main()
