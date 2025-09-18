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
            self.bottom = top
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
        self.top = geometry.pos.x
        self.left = geometry.pos.y
        self.rows = geometry.size.height
        self.cols = geometry.size.width

        # TODO: Check for errors/exceptions
        self.rect = curses.newwin(self.cols, self.rows, self.top, self.left)

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

    def move(self, x, y) -> None:
        self.rect.move(y, x)


class Pane:

    def __init__(self, geometry: Geometry = Geometry(),
                 padding: Padding = Padding(), border: bool = False,
                 title: str = None, title_pos: str = None) -> None:

        # Outer pane geometry
        self.top = geometry.pos.x
        self.left = geometry.pos.y
        self.rows = geometry.size.height
        self.cols = geometry.size.width

        # Inner pane geometry
        self.inner_top = padding.top
        self.inner_left = padding.left
        self.inner_rows = self.rows - (padding.top + padding.bottom)
        self.inner_cols = self.cols - (padding.left + padding.right)

        # TODO: Should we check for errors/exceptions?
        self.outer_pane = curses.newwin(self.cols, self.rows, self.left,
                                        self.right)
        self.inner_pane = curses.newwin(self.inner_cols, self.inner_rows,
                                        self.inner_top, self.inner_left)

        # Border
        # TODO: Assume padding is at least 1 (for border drawing).
        if border:
            # TODO: Other borders (i.e. rounded, dotted, etc)
            self.outer_pane.box()

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
