#!/usr/bin/env python3
"""
Todo 2

A todo app for the terminal.

"""

import curses
import sys
import os

# Check if there are previously saved items. If so, load them.


# ┌───────────┐
# │ Main Loop │
# └───────────┘

def main(_):
    """
    This should be a docstring!
    """
    # ┌────┐
    # │ UI │
    # └────┘

    if not curses.has_colors():
        sys.exit(1)

    curses.start_color()
    curses.use_default_colors()

    screen = curses.initscr()
    columns, rows = screen.getmaxyx()

    screen.addstr(f"Rows: {rows}\nCols: {columns}")
    screen.getch()


if __name__ == "__main__":
    curses.wrapper(main)
