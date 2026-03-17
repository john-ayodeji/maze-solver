from tkinter import Canvas, Tk


class Window:
    def __init__(self, width, height, bg="#f8fafc"):
        self.root = Tk()
        self.root.title("Maze Solver")
        self.canvas = Canvas(
            self.root,
            width=width,
            height=height,
            bg=bg,
            highlightthickness=0,
        )
        self.canvas.pack()
        self.running = False
        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.root.update_idletasks()
        self.root.update()

    def wait_for_close(self):
        self.running = True
        while self.running:
            self.redraw()

    def close(self):
        self.running = False

    def draw_line(self, line, fill_color):
        line.draw(self.canvas, fill_color)

    def clear_canvas(self):
        self.canvas.delete("all")

    def resize_canvas(self, width, height):
        self.canvas.config(width=width, height=height)
