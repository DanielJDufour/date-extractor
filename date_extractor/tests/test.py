#-*- coding: utf-8 -*-

from sys import version_info
python_version = version_info.major

import unittest
from date_extractor import *

class TestStringMethods(unittest.TestCase):

    def test_normalization(self):
        self.assertEqual(str(g("12/23/09")), "2009-12-23 00:00:00+00:00")

    def test_year(self):
        self.assertEqual(str(g("2015-11-21")),'2015-01-01 00:00:00+00:00')

    def test_arabic(self):
        if python_version == 2:
            text = "٢١ نوفمبر ٢٠١٥".decode('utf-8')
            self.assertEqual(str(g(text)),'2015-11-21 00:00:00+00:00')
        elif python_version == 3:
            text = "٢١ نوفمبر ٢٠١٥"
            self.assertEqual(str(g(text)),'2015-11-21 00:00:00+00:00')



    def test_arabic2(self):
        text = """
        ٢١ تشرين ثاني/نوفمبر ٢٠١٥
        """
        if python_version == 2:
            text = text.decode("utf-8")
        self.assertEqual(str(g(text)),'2015-11-21 00:00:00+00:00')

    def test_year(self):
        text = """12/16/2010 9:09 AM ET\nA Run Like No Othe"""
        self.assertEqual(str(g(text)), '2010-12-16 00:00:00+00:00')

    def test_year_by_itself(self):
        text = "President Obama has used Oval Office speeches sparingly, compared with previous presidents. His previous two addresses, both in 2010, covered the Deepwater Horizon oil spill and the end of combat operations in Iraq."
        self.assertEqual(str(g(text)), '2010-01-01 00:00:00+00:00')

    def test_mdyt(self):
        text = "9/1/99 22:00"
        self.assertEqual(str(g(text)), "1999-09-01 00:00:00+00:00")


if __name__ == '__main__':
    unittest.main()
