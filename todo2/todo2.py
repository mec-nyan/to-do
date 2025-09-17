#!/usr/bin/env python3
"""
Todo 2

A todo app for the terminal.

"""

import curses
import sys
import json

# ┌───────────┐
# │ Main Loop │
# └───────────┘


def main(_):
    """
    This should be a docstring!
    """

    # Check if there are previously saved items. If so, load them.
    # TODO: Check if the file exists.
    with open("items.json", "r") as saved:
        items: dict[str, list[str]] = json.load(saved)

    # ┌────┐
    # │ UI │
    # └────┘

    if not curses.has_colors():
        sys.exit(1)

    curses.start_color()
    curses.use_default_colors()
    curses.curs_set(False)

    screen = curses.initscr()
    rows, columns = screen.getmaxyx()

    # Split in two panes.
    pane_left_w = columns // 2
    pane_right_w = columns - pane_left_w

    pane_left = curses.newwin(rows, pane_left_w, 0, 0)
    pane_right = curses.newwin(rows, pane_right_w, 0, pane_left_w)

    selected = 0
    todos = list(items.keys())
    quit = False

    while not quit:
        pane_left.erase()
        pane_right.erase()

        for i, todo in enumerate(todos):
            indicator = " "
            if i == selected:
                indicator = ">"
            pane_left.addstr(f"{indicator} {todo}\n")

        pane_left.noutrefresh()

        sub_items = items[todos[selected]]
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
            case 'q':
                quit = True


if __name__ == "__main__":
    curses.wrapper(main)
