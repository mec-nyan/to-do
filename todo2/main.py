#!/usr/bin/env python3
"""
Todo2

A todo app.

"""


from app import App


if __name__ == "__main__":
    try:
        App().run()
    except Exception as e:
        print(type(e))
        print(e.args)
        print(e)
