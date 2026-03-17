import tkinter as tk
from tkinter import ttk

from maze import Maze
from window import Window


class MazeApp:
    def __init__(self):
        self.win = Window(980, 760, bg="#f8fafc")
        self.win.root.title("Maze Lab")

        self.maze = None
        self.margin = 12

        self.rows_var = tk.StringVar(value="18")
        self.cols_var = tk.StringVar(value="26")
        self.cell_size_var = tk.StringVar(value="28")
        self.seed_var = tk.StringVar(value="0")
        self.algorithm_var = tk.StringVar(value="dfs")

        self.gen_delay_var = tk.StringVar(value="0.001")
        self.forward_delay_var = tk.StringVar(value="0.004")
        self.backtrack_delay_var = tk.StringVar(value="0.03")

        self.status_var = tk.StringVar(value="Set options, then click Generate + Solve")

        self._build_controls()

    def _build_controls(self):
        controls = ttk.Frame(self.win.root, padding=8)
        controls.pack(fill="x")

        ttk.Label(controls, text="Rows").grid(row=0, column=0, sticky="w")
        ttk.Entry(controls, textvariable=self.rows_var, width=6).grid(row=0, column=1, padx=4)

        ttk.Label(controls, text="Cols").grid(row=0, column=2, sticky="w")
        ttk.Entry(controls, textvariable=self.cols_var, width=6).grid(row=0, column=3, padx=4)

        ttk.Label(controls, text="Cell").grid(row=0, column=4, sticky="w")
        ttk.Entry(controls, textvariable=self.cell_size_var, width=6).grid(row=0, column=5, padx=4)

        ttk.Label(controls, text="Seed").grid(row=0, column=6, sticky="w")
        ttk.Entry(controls, textvariable=self.seed_var, width=8).grid(row=0, column=7, padx=4)

        ttk.Label(controls, text="Algorithm").grid(row=0, column=8, sticky="w")
        ttk.Combobox(
            controls,
            textvariable=self.algorithm_var,
            values=("dfs", "bfs", "astar"),
            width=8,
            state="readonly",
        ).grid(row=0, column=9, padx=4)

        ttk.Label(controls, text="Gen Delay").grid(row=1, column=0, sticky="w")
        ttk.Entry(controls, textvariable=self.gen_delay_var, width=8).grid(row=1, column=1, padx=4)

        ttk.Label(controls, text="Forward Delay").grid(row=1, column=2, sticky="w")
        ttk.Entry(controls, textvariable=self.forward_delay_var, width=8).grid(row=1, column=3, padx=4)

        ttk.Label(controls, text="Backtrack Delay").grid(row=1, column=4, sticky="w")
        ttk.Entry(controls, textvariable=self.backtrack_delay_var, width=8).grid(row=1, column=5, padx=4)

        ttk.Button(controls, text="Generate", command=self.generate).grid(row=1, column=7, padx=4)
        ttk.Button(controls, text="Solve", command=self.solve).grid(row=1, column=8, padx=4)
        ttk.Button(controls, text="Generate + Solve", command=self.generate_and_solve).grid(row=1, column=9, padx=4)

        ttk.Label(self.win.root, textvariable=self.status_var, padding=8).pack(fill="x")

    def _get_int(self, value, default, min_value, max_value):
        try:
            parsed = int(value)
        except ValueError:
            return default
        return max(min_value, min(max_value, parsed))

    def _get_float(self, value, default, min_value, max_value):
        try:
            parsed = float(value)
        except ValueError:
            return default
        return max(min_value, min(max_value, parsed))

    def _build_maze(self):
        rows = self._get_int(self.rows_var.get(), 18, 2, 200)
        cols = self._get_int(self.cols_var.get(), 26, 2, 200)
        cell_size = self._get_int(self.cell_size_var.get(), 28, 6, 60)

        seed_text = self.seed_var.get().strip()
        seed = int(seed_text) if seed_text else None

        generate_delay = self._get_float(self.gen_delay_var.get(), 0.001, 0.0, 0.2)
        forward_delay = self._get_float(self.forward_delay_var.get(), 0.004, 0.0, 0.2)
        backtrack_delay = self._get_float(self.backtrack_delay_var.get(), 0.03, 0.0, 0.5)

        canvas_w = max(600, self.margin * 2 + cols * cell_size)
        canvas_h = max(420, self.margin * 2 + rows * cell_size)
        self.win.resize_canvas(canvas_w, canvas_h)
        self.win.clear_canvas()

        self.maze = Maze(
            self.margin,
            self.margin,
            rows,
            cols,
            cell_size,
            cell_size,
            self.win,
            seed=seed,
            generate_delay=generate_delay,
            solve_forward_delay=forward_delay,
            solve_backtrack_delay=backtrack_delay,
            wall_color="#0f172a",
            empty_color="#f8fafc",
            move_color="#ef4444",
            undo_color="#94a3b8",
            frontier_color="#0ea5e9",
            final_path_color="#f97316",
        )

    def generate(self):
        self._build_maze()
        self.status_var.set("Maze generated")

    def solve(self):
        if self.maze is None:
            self._build_maze()

        method = self.algorithm_var.get().strip().lower()
        solved = self.maze.solve(method=method)
        elapsed = self.maze.last_solve_seconds or 0.0
        self.status_var.set(
            f"{method.upper()} | solved={solved} | time={elapsed:.4f}s"
        )

    def generate_and_solve(self):
        self.generate()
        self.solve()

    def run(self):
        self.win.wait_for_close()


def main():
    app = MazeApp()
    app.run()


if __name__ == "__main__":
    main()
