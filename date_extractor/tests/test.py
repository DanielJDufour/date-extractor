#-*- coding: utf-8 -*-
import unittest
from date_extractor import *

class TestStringMethods(unittest.TestCase):

    def test_year(self):
        self.assertEqual(str(g("2015-11-21")),'2015-01-01 00:00:00+00:00')

    def test_arabic(self):
        text = "٢١ نوفمبر ٢٠١٥".decode("utf-8")
        self.assertEqual(str(g(text)),'2015-11-21 00:00:00+00:00')

    def test_arabic2(self):
        text = """
        ٢١ تشرين ثاني/نوفمبر ٢٠١٥
        """.decode("utf-8")
        self.assertEqual(str(g(text)),'2015-11-21 00:00:00+00:00')


if __name__ == '__main__':
    unittest.main()
