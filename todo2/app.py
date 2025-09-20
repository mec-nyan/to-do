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

    def end(self) -> None:
        self.screen.keypad(0)
        curses.echo()
        curses.nocbreak()
        curses.endwin()

    def do_stuff(self) -> None:
        # Add title:
        win_title = "Shit to do"
        title_pane = SimplePane(Geometry(Position(), Size(self.columns, 3)))
        title_pane.addstr_centered(1, win_title)
        title_pane.getch()

        # Split in two panes.

        horz_padding = 0
        if self.columns > self.MIN_WIDTH:
            max_horz_padding = 16
            horz_padding = min((self.columns - self.MIN_WIDTH) //
                               2, max_horz_padding)

        available_width = self.columns - horz_padding * 2
        pane_left_w = available_width // 2
        pane_right_w = available_width - pane_left_w

        # pane_left = curses.newwin(rows - 6, pane_left_w, 3, horz_padding)
        # pane_right = curses.newwin(
        #     rows - 6, pane_right_w, 3, pane_left_w + horz_padding)

        pane_left = Pane(Geometry(Position(horz_padding, 3), Size(
            pane_left_w, self.rows - 6)), Padding(1, 2), True)
        pane_left.addstr("Left")
        pane_left.getch()

        pane_right = Pane(Geometry(Position(pane_left_w + horz_padding, 3),
                          Size(pane_right_w, self.rows - 6)), Padding(1, 2), True)
        pane_right.addstr("Right")
        pane_right.getch()

        # Insert window:
        input_win_w = self.MIN_WIDTH
        input_win_h = 3
        input_win_x = (self.columns - self.MIN_WIDTH) // 2
        input_win_y = self.rows // 2 - 2
        # input_win = curses.newwin(
        #     input_win_h,
        #     input_win_w,
        #     input_win_y,
        #     input_win_x)

        input_win = Pane(Geometry(Position(input_win_x, input_win_y), Size(
            input_win_w, input_win_h)), Padding(), True)
        input_win.getch()

        sys.exit()

        def get_item() -> str:
            max_str_len = input_win_w - 7
            curses.curs_set(True)
            input_str = []
            getting = True
            accept = False
            while getting:
                input_win.erase()
                input_win.box()
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
            self.do_stuff()
        except Exception as e:
            raise e
        finally:
            self.end()
