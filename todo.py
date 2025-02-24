#!/usr/bin/env python3
"""
A basic terminal to-do app.

Because I always forget to do some stuff!
"""

import curses
from curses import ascii
import locale

from niceties import rounded_box


def todo(screen):
    items = []
    with open("items.txt", "r") as f:
        content = f.read()
        if len(content) > 1:
            items = content.split("\n")

    prompt = curses.newwin(3, 50, rows - 10, (cols - 50) // 2)

    current = 0

    go_on = True
    while go_on:
        while True:
            curses.curs_set(False)
            screen.move(3, 0)
            screen.clrtobot()
            for i in range(len(items)):
                screen.addstr(3 + i, 8, f"{current == i and '>' or ' '} [ ] {items[i]}")
            screen.refresh()
            c = chr(screen.getch())
            if c == "j" and current < len(items) - 1:
                current += 1
            elif c == "k" and current > 0:
                current -= 1
            elif c == "q":
                go_on = False
                break
            elif c == "x":
                screen.addstr(rows - 1, 4, f"Delete item < {items[current]} > ? ")
                confirm = screen.getch()
                if confirm == ord("y"):
                    items.pop(current)
                    screen.move(rows - 1, 4)
                    screen.clrtoeol()
                    screen.addstr("Item deleted!")
                    if current > 0:
                        current -= 1
                    screen.refresh()
                    curses.napms(1000)
            elif c == "i":
                curses.curs_set(True)
                text = []
                while True:
                    line = "".join(text)
                    prompt.clear()
                    rounded_box(prompt)
                    prompt.move(1, 2)
                    prompt.addstr(line)
                    d = prompt.getch()
                    if ascii.isprint(d):
                        text.append(chr(d))
                    elif d == ord("\033"):
                        break
                    elif d == ord("\177"):
                        if len(text):
                            text.pop()
                    elif d == ord("\n"):
                        items.append(line)
                        text.clear()
                        break

    with open("items.txt", "w") as f:
        f.write("\n".join(items))


def setup():
    curses.noecho()
    curses.cbreak()
    curses.curs_set(False)
    if curses.has_colors():
        try:
            curses.start_color()
            # curses.use_default_colors()
        except:
            raise

    loc = locale.setlocale(locale.LC_ALL, "")
    if not loc:
        raise


try:
    screen = curses.initscr()
    setup()

    rows, cols = screen.getmaxyx()

    screen.addnstr(2, 0, "Welcome!".center(cols), cols)

    menu = [
        {"item": "View to-do list", "keymap": "t"},
        {"item": "View notes", "keymap": "n"},
        {"item": "Quit", "keymap": "q"},
        {"item": "Help", "keymap": "?"},
    ]

    for i in range(len(menu)):
        key = menu[i]["keymap"]
        item = menu[i]["item"]
        screen.addstr(6 + i * 2, 0, f"{item:32} -> {key}".center(cols))

    c = chr(screen.getch())
    if c == "q":
        screen.clear()
        screen.addnstr(2, 0, "Bye!".center(cols), cols)
        screen.refresh()
        curses.napms(500)
        exit(0)
    elif c == "n" or c == "?":
        screen.clear()
        screen.addnstr(2, 0, "To do (lol)!".center(cols), cols)
        screen.refresh()
        curses.napms(500)
        exit(0)
    elif c == "t":
        screen.clear()
        screen.addnstr(2, 0, "To do".center(cols), cols)
        todo(screen)


finally:
    if "screen" in locals():
        curses.echo()
        curses.nocbreak()
        curses.endwin()
