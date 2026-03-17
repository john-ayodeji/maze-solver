from point import Line, Point


class Cell:
    def __init__(
        self,
        win=None,
        wall_color="#0f172a",
        empty_color="#f8fafc",
        move_color="#ef4444",
        undo_color="#64748b",
    ):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.visited = False
        self.__x1 = -1
        self.__x2 = -1
        self.__y1 = -1
        self.__y2 = -1
        self.__win = win
        self.__wall_color = wall_color
        self.__empty_color = empty_color
        self.__move_color = move_color
        self.__undo_color = undo_color

    def draw(self, x1, y1, x2, y2):
        self.__x1 = x1
        self.__y1 = y1
        self.__x2 = x2
        self.__y2 = y2

        if self.__win is None:
            return

        self.__win.draw_line(
            Line(Point(x1, y1), Point(x1, y2)),
            self.__wall_color if self.has_left_wall else self.__empty_color,
        )
        self.__win.draw_line(
            Line(Point(x2, y1), Point(x2, y2)),
            self.__wall_color if self.has_right_wall else self.__empty_color,
        )
        self.__win.draw_line(
            Line(Point(x1, y1), Point(x2, y1)),
            self.__wall_color if self.has_top_wall else self.__empty_color,
        )
        self.__win.draw_line(
            Line(Point(x1, y2), Point(x2, y2)),
            self.__wall_color if self.has_bottom_wall else self.__empty_color,
        )

    def draw_move(self, to_cell, undo=False, color=None):
        fill_color = color if color is not None else (self.__undo_color if undo else self.__move_color)
        from_center = Point(
            (self.__x1 + self.__x2) / 2,
            (self.__y1 + self.__y2) / 2,
        )
        to_center = Point(
            (to_cell.__x1 + to_cell.__x2) / 2,
            (to_cell.__y1 + to_cell.__y2) / 2,
        )
        if self.__win is not None:
            self.__win.draw_line(Line(from_center, to_center), fill_color)
