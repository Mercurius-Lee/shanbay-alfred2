#!/usr/bin/env python
# coding: utf-8


import unittest
import shanbay


class TestShanbay(unittest.TestCase):

    def test__parse_version(self):
        self.assertEqual((1, 4, 1), shanbay._parse_version('1.4.1'))
        self.assertEqual((1, 5, 0), shanbay._parse_version('1.5'))

    def test__version_compare(self):
        self.assertEqual('lt', shanbay._version_compare('1.4.0', '1.5.0'))
        self.assertEqual('eq', shanbay._version_compare('1.5.0', '1.5.0'))
        self.assertEqual('eq', shanbay._version_compare('1.5', '1.5.0'))
        self.assertEqual('gt', shanbay._version_compare('2.5', '1.7.0'))
        self.assertEqual('lt', shanbay._version_compare('0.1', '1.0'))


if __name__ == '__main__':
    unittest.main()

