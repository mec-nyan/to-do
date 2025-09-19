"""
pane.py


A 'Pane' is a rectangular portion of the screen, with some nice features like:

    - Borders
    - Padding (margins?)
    - Text functions (i.e. how to break strings, justify, center, etc)
    - ...

"""

import curses


class Position:
    """
    A point on the screen. Usually the top left corner.


    Default is 0, 0.
    """

    def __init__(self, x: int = 0, y: int = 0) -> None:
        self.x = x
        self.y = y


class Size:
    """
    The size of a rect (rows and columns).

    Default is 0, 0 (will use max rows and cols (see curses.newwin)).
    """

    def __init__(self, width: int = 0, height: int = 0) -> None:
        self.width = width
        self.height = height


class Geometry:
    """
    Position and size.

    Default is 0, 0, 0, 0 (see curses.newwin).
    """

    def __init__(self, pos: Position = Position(),
                 size: Size = Size()) -> None:
        self.pos = pos
        self.size = size


class Padding:
    """
    The padding of a Pane.

    TODO: Maybe use default values (i.e 1, 2).
    """

    def __init__(self, top: int = None, right: int = None, bottom: int = None,
                 left: int = None) -> None:
        self.top = 0
        self.right = 0
        self.bottom = 0
        self.left = 0

        # CSS style initialisation.
        if top is not None:
            self.top = top
            self.right = top
            self.bottom = top
            self.left = top
        if right is not None:
            self.right = right
            self.left = right
        if bottom is not None:
            self.bottom = bottom
        if left is not None:
            self.left = left


class Margin:
    """
    Maybe useful, maybe not.
    """

    def __init__(self, top: int = None, right: int = None, bottom: int = None,
                 left: int = None) -> None:
        self.top = 0
        self.right = 0
        self.bottom = 0
        self.left = 0

        # CSS style initialisation.
        if top is not None:
            self.top = top
            self.bottom = top
        if right is not None:
            self.right = right
            self.left = right
        if bottom is not None:
            self.bottom = bottom
        if left is not None:
            self.left = left


class SimplePane:
    """
    SimplePlane pane has no borders nor padding.
    """

    def __init__(self, geometry: Geometry = Geometry()) -> None:
        self.top = geometry.pos.y
        self.left = geometry.pos.x
        self.rows = geometry.size.height
        self.cols = geometry.size.width

        # TODO: Check for errors/exceptions
        self.rect = curses.newwin(self.rows, self.cols, self.top, self.left)

    def erase(self) -> None:
        self.rect.erase()

    def clear(self) -> None:
        self.rect.clear()

    def clear_to_eol(self) -> None:
        self.rect.clrtoeol()

    def clear_to_bot(self) -> None:
        self.rect.clrtobot()

    def refresh(self) -> None:
        self.rect.refresh()

    def noutrefresh(self) -> None:
        self.rect.noutrefresh()

    def getch(self) -> int:
        return self.rect.getch()

    def addstr(self, *args) -> None:
        self.rect.addstr(*args)

    def addstr_centered(self, line: int, text: str, *args) -> None:
        # TODO: Better size checking!
        # TODO: Better error handling!
        if len(text) > self.cols:
            raise
        padding = (self.cols - len(text)) // 2
        self.rect.addstr(line, padding, text, *args)

    def move(self, x, y) -> None:
        self.rect.move(y, x)


class Pane(SimplePane):

    def __init__(self, geometry: Geometry = Geometry(),
                 padding: Padding = Padding(), border: bool = False,
                 title: str = None, title_pos: str = None) -> None:

        if border:
            padding.right += 1
            padding.left += 1
            padding.top += 1
            padding.bottom += 1

        # Inner pane geometry
        self.inner_top = padding.top
        self.inner_left = padding.left
        self.inner_rows = geometry.size.height - (padding.top + padding.bottom)
        self.inner_cols = geometry.size.width - (padding.left + padding.right)

        super().__init__(Geometry(
            Position(self.inner_left, self.inner_top),
            Size(self.inner_cols, self.inner_rows)
        ))

        # Create an outer window for border/title
        # TODO: Should we allow for modification?
        if border or title:
            self.outer_rect = curses.newwin(geometry.size.height,
                                            geometry.size.width,
                                            geometry.pos.y,
                                            geometry.pos.x)

        # Border
        # TODO: Assume padding is at least 1 (for border drawing).
        if border:
            # TODO: Other borders (i.e. rounded, dotted, etc)
            self.outer_rect.box()
            self.outer_rect.refresh()

        # Title
        if title is not None:
            match title_pos:
                case 'left':
                    ...
                case 'right':
                    ...
                case 'center':
                    ...
                case _:
                    ...
            self.outer_rect.noutrefresh()
