#!/usr/bin/env python3
"""
A basic terminal to-do app.

Because I always forget to do some stuff!
"""

import curses
from curses import ascii
import locale

from niceties import rounded_box


# Aux
def split_string(line: str, max_len: int) -> list[str]:
    out: list[str] = []
    while len(line) > max_len:
        # Assume we'll find a space before max_len...
        split_point = 0
        while True:
            next_point = line.find(" ", split_point + 1)
            if next_point == -1:
                break
            if next_point > max_len:
                break
            split_point = next_point
        if split_point < len(line):
            out.append(line[:split_point])
            line = line[split_point:].strip()
    out.append(line)
    return out


def popup(screen, msg, ask=False, icon=""):
    msg = icon + " " + msg
    if ask:
        msg += " "

    rows, cols = screen.getmaxyx()

    popup_h = 5
    popup_w = len(msg) + 4
    if ask:
        popup_w += 1

    if popup_w > cols - 2:
        raise
    popup_y = (rows - popup_h) // 2
    popup_x = (cols - popup_w) // 2

    popup = curses.newwin(popup_h, popup_w, popup_y, popup_x)
    curses.init_pair(1, 1, 0)
    popup.bkgdset(curses.color_pair(1))

    rounded_box(popup)

    popup.addstr(2, 2, msg)

    return popup


def dialog(screen, msg):
    curses.curs_set(True)
    curses.echo()

    win = popup(screen, msg, ask=True, icon=" ")
    answer = win.getch()

    curses.curs_set(False)
    curses.noecho()

    return answer


def notes(screen):
    screen.noutrefresh()
    note = curses.newwin(16, 32, 4, 8)
    curses.init_pair(1, 0, 3)
    colour = curses.color_pair(1)
    note.bkgd(colour)
    note.addstr(0, 30, "x")
    note.addstr(1, 1, "Ima note!")
    note.getch()


def todo(screen):
    go_back = True

    items = []
    with open("items.txt", "r") as f:
        content = f.read()
        if len(content) > 1:
            items = content.split("\n")

    rows, cols = screen.getmaxyx()

    prompt = curses.newwin(3, 50, rows - 10, (cols - 50) // 2)

    info_line = curses.newwin(1, cols, rows - 2, 0)

    current = 0

    margin = 8
    max_line_len = cols - (2 * margin)

    go_on = True
    while go_on:
        while True:
            curses.curs_set(False)
            screen.move(4, 0)
            screen.clrtobot()
            y_pos = 4
            for i in range(len(items)):
                cursor = current == i and ">" or " "
                line = f"{cursor} [ ] "
                screen.addstr(y_pos, margin, line)

                lines = split_string(items[i], max_line_len - len(line))
                x_pos = margin + len(line)
                for line in lines:
                    screen.addstr(y_pos, x_pos, line)
                    y_pos += 1

            screen.refresh()

            info_line.addstr(
                0,
                4,
                "<i> Add item, <j> Next, <k> Previous, <x> Delete, <q> Quit, <esc> Back",
            )
            info_line.refresh()

            c = chr(screen.getch())
            if c == "j" and current < len(items) - 1:
                current += 1
            elif c == "k" and current > 0:
                current -= 1
            elif c == "q":
                go_on = False
                go_back = False
                break
            elif c == "\033":
                go_on = False
                break
            elif c == "x":
                # TODO: Show the result on the same dialog window.
                confirm = dialog(screen, f"Delete item '{items[current]}'?")
                message = "Cancelled"
                if confirm == ord("y"):
                    message = "Item deleted!"
                    items.pop(current)
                    if current > 0:
                        current -= 1
                info_line.clear()
                info_line.addstr(0, 4, message)
                info_line.refresh()
                curses.napms(1000)
            elif c == "i":
                curses.curs_set(True)
                text = []
                info_line.clear()
                info_line.addstr(0, 4, "<Enter> Add item, <Esc> Cancel")
                while True:
                    info_line.refresh()
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

    return go_back


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

    while True:
        screen.clear()
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
        elif c == "n":
            screen.clear()
            screen.addnstr(2, 0, "Notes".center(cols), cols)
            if not notes(screen):
                break
        elif c == "t":
            screen.clear()
            screen.addnstr(2, 0, "To do".center(cols), cols)
            if not todo(screen):
                break
        else:
            screen.clear()
            screen.addnstr(2, 0, "To do (lol)!".center(cols), cols)
            screen.refresh()
            curses.napms(500)
            exit(0)


finally:
    if "screen" in locals():
        curses.echo()
        curses.nocbreak()
        curses.endwin()
