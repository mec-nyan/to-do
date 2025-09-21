"""
App.py

Main app.

"""

import curses
import sys
import json

from pane import Pane, SimplePane, Geometry, Position, Size, Padding


class ErrorNoColours(Exception):
    ...


class App:
    """
    This is the main app.

    It should have a simple implementation. We'll have to split its run method
    later.
    """

    MIN_WIDTH = 100

    def __init__(self, opts=None) -> None:
        self.screen = curses.initscr()
        self.rows, self.columns = self.screen.getmaxyx()

        curses.noecho()
        curses.cbreak()
        curses.curs_set(False)

        try:
            curses.start_color()
            curses.use_default_colors()
        except:
            raise ErrorNoColours

    def load(self, file: str = "items.json") -> None:
        # Check that the file exists, or created
        with open(file, "a") as _:
            ...

        with open(file, "r") as saved:
            self.items: dict[str, list[str]] = json.load(saved)

    def init(self) -> None:
        self.add_title()

    def add_title(self, title: str = "Shit to do") -> None:
        self.title = title
        self.title_pane = SimplePane(Geometry(Position(),
                                              Size(self.columns, 3)))
        self.title_pane.addstr_centered(1, self.title)
        self.title_pane.getch()

    def get_left_pane_size(self, width: int, padding: int) -> Geometry:
        return Geometry(
            # Left 3 rows at the top (title) and 3 at the bottom (status)
            Position(padding, 3),
            Size(width // 2, self.rows - 6),
        )

    def get_right_pane_size(self, width: int, left_width: int,
                            padding: int) -> Geometry:
        return Geometry(
            # Left 3 rows at the top (title) and 3 at the bottom (status)
            Position(left_width + padding, 3),
            Size(width - left_width, self.rows - 6),
        )

    def get_input_win_size(self) -> Geometry:
        return Geometry(
            Position((self.columns - self.MIN_WIDTH) // 2, self.rows // 2 - 2),
            Size(self.MIN_WIDTH, 3)
        )

    def get_available_width(self) -> tuple[int, int]:
        horz_padding = 0
        if self.columns > self.MIN_WIDTH:
            max_horz_padding = 16
            horz_padding = min((self.columns - self.MIN_WIDTH) //
                               2, max_horz_padding)
        return self.columns - horz_padding * 2, horz_padding

    def put_panes(self) -> tuple[Pane, Pane, Pane]:
        available_width, margin_left = self.get_available_width()

        padding = Padding(1, 2)
        left_geom = self.get_left_pane_size(available_width, margin_left)
        pane_left = Pane(left_geom, padding, True)

        right_geom = self.get_right_pane_size(available_width,
                                              left_geom.size.width, margin_left)
        pane_right = Pane(right_geom, padding, True)

        # Insert window:
        input_geom = self.get_input_win_size()
        input_win = Pane(input_geom, Padding(), True)

        return pane_left, pane_right, input_win

    def end(self) -> None:
        self.screen.keypad(0)
        curses.echo()
        curses.nocbreak()
        curses.endwin()

    def do_stuff(self) -> None:
        pane_left, pane_right, input_win = self.put_panes()
        pane_left.addstr("Left")
        pane_left.noutrefresh()
        pane_right.addstr("Right")
        pane_right.noutrefresh()
        input_win.addstr("Input")
        input_win.rect.refresh()
        input_win.outer_rect.box()
        input_win.outer_rect.refresh()
        input_win.getch()
        # sys.exit()
        pane_left.rect.box()
        pane_left.refresh()
        pane_right.rect.box()
        pane_right.refresh()

        def get_item() -> str:
            max_str_len = input_win.available_width() - 3
            curses.curs_set(True)
            input_str = []
            getting = True
            accept = False
            while getting:
                input_win.erase()
                # input_win.box()
                input_win.addstr(1, 2, f"> {''.join(input_str)}")
                next = input_win.getch()
                match chr(next):
                    case '\x1b':
                        getting = False
                    case '\n':
                        getting = False
                        accept = True
                    case '\x7f':
                        if len(input_str) > 0:
                            input_str.pop()
                    case '\x15':  # C-U
                        input_str = []
                    case _:
                        if chr(next).isprintable() and len(input_str) < max_str_len:
                            input_str.append(chr(next))
            curses.curs_set(False)
            if accept:
                return ''.join(input_str)
            return ""

        def show_codes() -> None:
            last = 0
            curses.curs_set(True)
            while True:
                self.screen.move(self.rows - 1, 0)
                self.screen.clrtoeol()
                self.screen.addstr(
                    f"hex: {hex(last):>6} oct: {oct(last):>6} dec: {last:>6}", curses.A_ITALIC)
                next = self.screen.getch()
                if last == next:
                    break
                last = next
            self.screen.move(self.rows - 1, 0)
            self.screen.clrtoeol()
            self.screen.noutrefresh()
            curses.curs_set(False)

        def delete_item(key: str) -> bool:
            self.screen.move(self.rows - 1, 0)
            self.screen.clrtoeol()
            curses.curs_set(True)
            self.screen.addstr(f'Delete item "{key}"? ')
            action = self.screen.getch()
            if chr(action) == '\n':
                del self.items[key]
                return True
            self.screen.move(self.rows - 1, 0)
            self.screen.clrtoeol()
            self.screen.noutrefresh()
            curses.curs_set(False)
            return False

        selected = 0
        quit = False

        while not quit:
            todos = list(self.items.keys())

            pane_left.erase()
            pane_right.erase()

            for i, todo in enumerate(todos):
                indicator = " "
                if i == selected:
                    indicator = ">"
                pane_left.addstr(f"{indicator} {todo}\n")

            pane_left.noutrefresh()

            sub_items = self.items[todos[selected]]
            if len(sub_items) == 0:
                pane_right.addstr("???")
            else:
                for i, si in enumerate(sub_items):
                    pane_right.addstr(f"{i+1}.- {si}\n")

            pane_right.noutrefresh()

            curses.doupdate()

            action = pane_left.getch()
            match chr(action):
                case 'j':
                    selected += 1
                    if selected == len(todos):
                        selected = 0  # Wrap around.
                case 'k':
                    selected -= 1
                    if selected < 0:
                        selected = len(todos) - 1
                case 'i':
                    new_item = get_item()
                    if len(new_item) > 0:
                        self.items[new_item] = []
                        with open("./items.json", "w") as file:
                            file.write(json.dumps(self.items, indent="  "))
                case 'c':
                    show_codes()
                case 'x':
                    if delete_item(todos[selected]):
                        with open("./items.json", "w") as file:
                            file.write(json.dumps(self.items, indent="  "))
                        if selected > 0:
                            selected -= 1
                case 'q' | '\x1b':
                    quit = True

    def run(self):
        """
        Start here!
        """
        try:
            self.load()
            self.init()
            self.do_stuff()
        except Exception as e:
            raise e
        finally:
            self.end()
