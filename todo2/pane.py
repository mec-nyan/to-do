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
