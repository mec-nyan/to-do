#!/usr/bin/env python3
'''test_to-do.py'''

import unittest
import todo

class TestFunc(unittest.TestCase):

    def test_main(self):
        self.assertEqual(0, todo.main(), "Oops!")


if __name__ == "__main__":
    unittest.main()
