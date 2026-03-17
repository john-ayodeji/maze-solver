import heapq
import random
import time
from collections import deque
from time import perf_counter

from cell import Cell


class Maze:
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win=None,
        seed=None,
        generate_delay=0.002,
        solve_forward_delay=0.01,
        solve_backtrack_delay=0.04,
        wall_color="#0f172a",
        empty_color="#f8fafc",
        move_color="#ef4444",
        undo_color="#64748b",
        frontier_color="#38bdf8",
        final_path_color="#f97316",
    ):
        self.__x1 = x1
        self.__y1 = y1
        self.__num_rows = num_rows
        self.__num_cols = num_cols
        self.__cell_size_x = cell_size_x
        self.__cell_size_y = cell_size_y
        self.__win = win
        self.__cells = []

        self.__generate_delay = generate_delay
        self.__solve_forward_delay = solve_forward_delay
        self.__solve_backtrack_delay = solve_backtrack_delay

        self.__wall_color = wall_color
        self.__empty_color = empty_color
        self.__move_color = move_color
        self.__undo_color = undo_color
        self.__frontier_color = frontier_color
        self.__final_path_color = final_path_color

        self.last_solve_seconds = None

        if seed is not None:
            random.seed(seed)

        self.__create_cells()
        self.__break_entrance_and_exit()
        self.__break_walls_r(0, 0)
        self.__reset_cells_visited()

    def __create_cells(self):
        for i in range(self.__num_cols):
            column = []
            for j in range(self.__num_rows):
                column.append(
                    Cell(
                        self.__win,
                        wall_color=self.__wall_color,
                        empty_color=self.__empty_color,
                        move_color=self.__move_color,
                        undo_color=self.__undo_color,
                    )
                )
            self.__cells.append(column)

        for i in range(self.__num_cols):
            for j in range(self.__num_rows):
                self.__draw_cell(i, j)

    def __draw_cell(self, i, j):
        x1 = self.__x1 + i * self.__cell_size_x
        y1 = self.__y1 + j * self.__cell_size_y
        x2 = x1 + self.__cell_size_x
        y2 = y1 + self.__cell_size_y

        self.__cells[i][j].draw(x1, y1, x2, y2)
        self.__animate(self.__generate_delay)

    def __break_entrance_and_exit(self):
        self.__cells[0][0].has_top_wall = False
        self.__draw_cell(0, 0)

        self.__cells[self.__num_cols - 1][self.__num_rows - 1].has_bottom_wall = False
        self.__draw_cell(self.__num_cols - 1, self.__num_rows - 1)

    def __break_walls_r(self, i, j):
        self.__cells[i][j].visited = True

        while True:
            neighbors = []

            if i > 0 and not self.__cells[i - 1][j].visited:
                neighbors.append((i - 1, j))
            if i < self.__num_cols - 1 and not self.__cells[i + 1][j].visited:
                neighbors.append((i + 1, j))
            if j > 0 and not self.__cells[i][j - 1].visited:
                neighbors.append((i, j - 1))
            if j < self.__num_rows - 1 and not self.__cells[i][j + 1].visited:
                neighbors.append((i, j + 1))

            if not neighbors:
                self.__draw_cell(i, j)
                return

            ni, nj = random.choice(neighbors)

            if ni == i - 1:
                self.__cells[i][j].has_left_wall = False
                self.__cells[ni][nj].has_right_wall = False
            elif ni == i + 1:
                self.__cells[i][j].has_right_wall = False
                self.__cells[ni][nj].has_left_wall = False
            elif nj == j - 1:
                self.__cells[i][j].has_top_wall = False
                self.__cells[ni][nj].has_bottom_wall = False
            else:
                self.__cells[i][j].has_bottom_wall = False
                self.__cells[ni][nj].has_top_wall = False

            self.__break_walls_r(ni, nj)

    def __reset_cells_visited(self):
        for col in self.__cells:
            for cell in col:
                cell.visited = False

    def __neighbors(self, i, j):
        cell = self.__cells[i][j]
        neighbors = []

        if i > 0 and not cell.has_left_wall:
            neighbors.append((i - 1, j))
        if i < self.__num_cols - 1 and not cell.has_right_wall:
            neighbors.append((i + 1, j))
        if j > 0 and not cell.has_top_wall:
            neighbors.append((i, j - 1))
        if j < self.__num_rows - 1 and not cell.has_bottom_wall:
            neighbors.append((i, j + 1))

        return neighbors

    def __draw_step(self, from_pos, to_pos, undo=False, color=None):
        fi, fj = from_pos
        ti, tj = to_pos
        self.__cells[fi][fj].draw_move(self.__cells[ti][tj], undo=undo, color=color)
        self.__animate(self.__solve_backtrack_delay if undo else self.__solve_forward_delay)

    def __draw_path(self, came_from, goal):
        node = goal
        segments = []
        while came_from[node] is not None:
            prev = came_from[node]
            segments.append((prev, node))
            node = prev

        for prev, nxt in reversed(segments):
            self.__draw_step(prev, nxt, color=self.__final_path_color)

    def solve(self, method="dfs"):
        self.__reset_cells_visited()
        start = perf_counter()

        selected = method.lower()
        if selected == "dfs":
            solved = self._solve_r(0, 0)
        elif selected == "bfs":
            solved = self._solve_bfs()
        elif selected == "astar":
            solved = self._solve_astar()
        else:
            raise ValueError(f"Unknown solve method: {method}")

        self.last_solve_seconds = perf_counter() - start
        return solved

    def _solve_r(self, i, j):
        self.__animate(self.__solve_forward_delay)
        self.__cells[i][j].visited = True

        if i == self.__num_cols - 1 and j == self.__num_rows - 1:
            return True

        if (
            i > 0
            and not self.__cells[i][j].has_left_wall
            and not self.__cells[i - 1][j].visited
        ):
            self.__draw_step((i, j), (i - 1, j))
            if self._solve_r(i - 1, j):
                return True
            self.__draw_step((i, j), (i - 1, j), undo=True)

        if (
            i < self.__num_cols - 1
            and not self.__cells[i][j].has_right_wall
            and not self.__cells[i + 1][j].visited
        ):
            self.__draw_step((i, j), (i + 1, j))
            if self._solve_r(i + 1, j):
                return True
            self.__draw_step((i, j), (i + 1, j), undo=True)

        if (
            j > 0
            and not self.__cells[i][j].has_top_wall
            and not self.__cells[i][j - 1].visited
        ):
            self.__draw_step((i, j), (i, j - 1))
            if self._solve_r(i, j - 1):
                return True
            self.__draw_step((i, j), (i, j - 1), undo=True)

        if (
            j < self.__num_rows - 1
            and not self.__cells[i][j].has_bottom_wall
            and not self.__cells[i][j + 1].visited
        ):
            self.__draw_step((i, j), (i, j + 1))
            if self._solve_r(i, j + 1):
                return True
            self.__draw_step((i, j), (i, j + 1), undo=True)

        return False

    def _solve_bfs(self):
        start = (0, 0)
        goal = (self.__num_cols - 1, self.__num_rows - 1)
        q = deque([start])
        came_from = {start: None}
        self.__cells[0][0].visited = True

        while q:
            i, j = q.popleft()
            if (i, j) == goal:
                self.__draw_path(came_from, goal)
                return True

            for ni, nj in self.__neighbors(i, j):
                if self.__cells[ni][nj].visited:
                    continue
                self.__cells[ni][nj].visited = True
                came_from[(ni, nj)] = (i, j)
                self.__draw_step((i, j), (ni, nj), color=self.__frontier_color)
                q.append((ni, nj))

        return False

    def _solve_astar(self):
        start = (0, 0)
        goal = (self.__num_cols - 1, self.__num_rows - 1)

        def heuristic(pos):
            return abs(goal[0] - pos[0]) + abs(goal[1] - pos[1])

        open_heap = [(heuristic(start), 0, start)]
        g_score = {start: 0}
        came_from = {start: None}
        closed = set()

        self.__cells[0][0].visited = True

        while open_heap:
            _, current_g, current = heapq.heappop(open_heap)
            if current in closed:
                continue
            closed.add(current)

            if current == goal:
                self.__draw_path(came_from, goal)
                return True

            i, j = current
            for ni, nj in self.__neighbors(i, j):
                neighbor = (ni, nj)
                tentative_g = current_g + 1
                if tentative_g >= g_score.get(neighbor, float("inf")):
                    continue

                g_score[neighbor] = tentative_g
                came_from[neighbor] = current
                f_score = tentative_g + heuristic(neighbor)
                heapq.heappush(open_heap, (f_score, tentative_g, neighbor))

                if not self.__cells[ni][nj].visited:
                    self.__cells[ni][nj].visited = True
                    self.__draw_step(current, neighbor, color=self.__frontier_color)

        return False

    def __animate(self, delay=0.0):
        if self.__win is None:
            return

        self.__win.redraw()
        if delay > 0:
            time.sleep(delay)
