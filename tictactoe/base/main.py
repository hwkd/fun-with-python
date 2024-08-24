#!/usr/bin/env python3

import sys
import signal
from game import Game


def main():
    Game().start()


if __name__ == "__main__":
    signal.signal(signal.SIGINT, lambda _x, _y: sys.exit(0))
    main()
