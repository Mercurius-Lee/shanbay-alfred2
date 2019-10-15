#!/usr/bin/env python
# coding: utf-8


import unittest
import shanbay


class ITShanbay(unittest.TestCase):

    def test_is_upgrade_availabed(self):
        self.assertFalse(shanbay.is_upgrade_availabed())


if __name__ == '__main__':
    unittest.main()
