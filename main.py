from window import Window
from maze import Maze


def main():
    win = Window(800, 600)

    maze = Maze(10, 10, 12, 16, 48, 48, win, seed=0)
    maze.solve()

    win.wait_for_close()


if __name__ == "__main__":
    main()
