import unittest

from maze import Maze


class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(len(m1._Maze__cells), num_cols)
        self.assertEqual(len(m1._Maze__cells[0]), num_rows)

    def test_maze_create_cells_small(self):
        num_cols = 2
        num_rows = 2
        m = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(len(m._Maze__cells), num_cols)
        self.assertEqual(len(m._Maze__cells[0]), num_rows)

    def test_maze_create_cells_single_column(self):
        num_cols = 1
        num_rows = 5
        m = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(len(m._Maze__cells), num_cols)
        self.assertEqual(len(m._Maze__cells[0]), num_rows)

    def test_maze_create_cells_single_row(self):
        num_cols = 7
        num_rows = 1
        m = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(len(m._Maze__cells), num_cols)
        self.assertEqual(len(m._Maze__cells[0]), num_rows)

    def test_maze_create_cells_large(self):
        num_cols = 20
        num_rows = 30
        m = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(len(m._Maze__cells), num_cols)
        self.assertEqual(len(m._Maze__cells[0]), num_rows)


    def test_maze_break_entrance_and_exit(self):
        num_cols = 5
        num_rows = 4
        m = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertFalse(m._Maze__cells[0][0].has_top_wall)
        self.assertFalse(m._Maze__cells[num_cols - 1][num_rows - 1].has_bottom_wall)

    def test_maze_break_entrance_and_exit_large(self):
        num_cols = 12
        num_rows = 10
        m = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertFalse(m._Maze__cells[0][0].has_top_wall)
        self.assertFalse(m._Maze__cells[num_cols - 1][num_rows - 1].has_bottom_wall)

    def test_maze_reset_cells_visited(self):
        num_cols = 6
        num_rows = 5
        m = Maze(0, 0, num_rows, num_cols, 10, 10)
        for col in m._Maze__cells:
            for cell in col:
                self.assertFalse(cell.visited)

    def test_maze_reset_cells_visited_large(self):
        num_cols = 12
        num_rows = 10
        m = Maze(0, 0, num_rows, num_cols, 10, 10)
        for col in m._Maze__cells:
            for cell in col:
                self.assertFalse(cell.visited)


if __name__ == "__main__":
    unittest.main()
