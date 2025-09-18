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
    """

    def __init__(self, x: int = 0, y: int = 0) -> None:
        self.x = x
        self.y = y


class Size:
    """
    The size of a rect (rows and columns).
    """

    def __init__(self, width: int = 0, height: int = 0) -> None:
        self.width = width
        self.height = height


class Geometry:
    """
    Position and size.
    """

    def __init__(self, pos: Position = Position(),
                 size: Size = Size()) -> None:
        self.pos = pos
        self.size = size


class Padding:
    """
    The padding of a Pane.
    """

    def __init__(self, top: int = 0, right: int = 0, bottom: int = 0,
                 left: int = 0) -> None:
        self.top = top
        self.right = right
        self.bottom = bottom
        self.left = left


class Margin:
    """
    Maybe useful, maybe not.
    """

    ...


class Pane:

    def __init__(self, geometry: Geometry = Geometry(),
                 padding: Padding = None) -> None:
        self.top = geometry.pos.x
        self.left = geometry.pos.y
        self.rows = geometry.size.height
        self.cols = geometry.size.width
        self.padding = padding

        self.init()

    def init(self):
        ...
