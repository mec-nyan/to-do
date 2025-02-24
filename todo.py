#!/usr/bin/env python3
"""
A basic terminal to-do app.

Because I always forget to do some stuff!
"""

import curses
import curses.ascii
import locale


def rounded_box(win):
    y, x = 0, 0
    rows, cols = win.getmaxyx()
    topleft = "╭"
    topright = "╮"
    botleft = "╰"
    botright = "╯"
    win.addstr(y, x, topleft)
    win.addstr(y + rows - 1, x, botleft)
    win.addstr(y, x + cols - 1, topright)
    win.addstr(y + rows - 1, x + cols - 2, botright)
    win.insstr(y + rows - 1, x + cols - 2, "─")


def main(stdscr):
    loc = locale.setlocale(locale.LC_ALL, "")
    if not loc:
        return 1

    screen = curses.newwin(0, 0, 0, 0)
    rows, cols = screen.getmaxyx()

    screen.addnstr(2, 0, "Welcome!".center(cols), cols)
    screen.noutrefresh()

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
            c = screen.getch()
            c = chr(c)
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
                    prompt.box()
                    rounded_box(prompt)
                    prompt.move(1, 2)
                    prompt.addstr(line)
                    c = prompt.getch()
                    if curses.ascii.isprint(c):
                        text.append(chr(c))
                    elif c == ord("\033"):
                        break
                    elif c == ord("\177"):
                        if len(text):
                            text.pop()
                    elif c == ord("\n"):
                        items.append(line)
                        text.clear()
                        break

    with open("items.txt", "w") as f:
        f.write("\n".join(items))

    return 0


if __name__ == "__main__":
    curses.wrapper(main)
