"""
Niceties

AKA curses tweaks!
"""

def rounded_box(win):
    y, x = 0, 0
    rows, cols = win.getmaxyx()
    topleft = "╭"
    topright = "╮"
    botleft = "╰"
    botright = "╯"
    win.box()
    win.addstr(y, x, topleft)
    win.addstr(y + rows - 1, x, botleft)
    win.addstr(y, x + cols - 1, topright)
    win.addstr(y + rows - 1, x + cols - 2, botright)
    win.insstr(y + rows - 1, x + cols - 2, "─")
