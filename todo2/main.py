#!/usr/bin/env python3
"""
Todo2

A todo app.

"""

import curses

from app import App


if __name__ == "__main__":
    _app = App()
    curses.wrapper(_app.run)
