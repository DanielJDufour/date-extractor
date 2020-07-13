# -*- coding: utf-8 -*-

import unittest
from unittest import TestCase

from date_extractor import *

"""
class TimeZone(TestCase):
    def test_date_with_timezone(self):
        text = "Publication date 11 April 2019 | 13:46 ICT"
        date = extract_date(text, debug=True)
        self.assertEqual(str(date), "2019-04-11 00:00:00+")
"""


class TestTimeStamps(TestCase):
    def test_spaced(self):
        text = "2018-06-07 16:31:54"
        date = extract_date(text, debug=False)
        self.assertEqual(str(date), "2018-06-07 16:31:54+00:00")

    def test_t_separated(self):
        text = "2018-06-07T16:31:54"
        date = extract_date(text, debug=False)
        self.assertEqual(str(date), "2018-06-07 16:31:54+00:00")


class ChineseTest(TestCase):
    def test_taiwan_times(self):
        text = "壹、開會時間：109 年 3 月 27 日下午 2 時 0 分正"
        dates = extract_dates(text, debug=False)
        self.assertEqual(
            str(dates), "[datetime.datetime(2020, 3, 27, 0, 0, tzinfo=<UTC>)]"
        )

    def test_chinese_times(self):
        text = "2006年1月29日"
        dates = extract_dates(text, debug=False)
        self.assertEqual(
            str(dates), "[datetime.datetime(2006, 1, 29, 0, 0, tzinfo=<UTC>)]"
        )


class TestStringMethods(TestCase):
    def test_with_hours(self):
        text = "January 4, 2015 17:47"
        dates = extract_dates(text, debug=False)
        self.assertEqual(len(dates), 1)
        self.assertEqual(str(dates[0]), "2015-01-04 00:00:00+00:00")

    # if just a bunch of random numbers together don't parse date
    # assuming most people won't burry dates in strings like this
    def test_numberstring(self):
        text = "12837.1230120"
        dates = extract_dates(text, debug=False)
        self.assertEqual(len(dates), 0)

    def test_message(self):
        text = "<128937012837.12301209391023.daniel@firstdraftgis.com> Date: Wed, 16 May 2001 17:41:00 -0500 (PDT)"
        dates = extract_dates(text, debug=False)
        self.assertEqual(len(dates), 1)
        self.assertEqual(str(dates[0]), "2001-05-16 00:00:00+00:00")

    def test_example(self):
        text = "I arrived in that city on January 4, 1937"
        dates = extract_dates(text)
        self.assertEqual(len(dates), 1)
        self.assertEqual(str(dates[0]), "1937-01-04 00:00:00+00:00")

    def test_normalization(self):
        self.assertEqual(str(g("12/23/09")), "2009-12-23 00:00:00+00:00")

    def test_year1(self):
        self.assertEqual(str(g("2015-11-21")), "2015-01-01 00:00:00+00:00")

    def test_arabic(self):
        text = "٢١ نوفمبر ٢٠١٥"
        self.assertEqual(str(g(text)), "2015-11-21 00:00:00+00:00")

    def test_arabic2(self):
        text = """
        ٢١ تشرين ثاني/نوفمبر ٢٠١٥
        """
        self.assertEqual(str(g(text)), "2015-11-21 00:00:00+00:00")

    def test_year(self):
        text = """12/16/2010 9:09 AM ET\nA Run Like No Othe"""
        self.assertEqual(str(g(text)), "2010-12-16 00:00:00+00:00")

    def test_year_by_itself(self):
        text = "President Obama has used Oval Office speeches sparingly, compared with previous presidents. His previous two addresses, both in 2010, covered the Deepwater Horizon oil spill and the end of combat operations in Iraq."
        dates = extract_dates(text, debug=False)
        self.assertEqual(len(dates), 1)
        self.assertEqual(str(dates[0]), "2010-01-01 00:00:00+00:00")

    def test_mdyt(self):
        text = "9/1/99 22:00"
        self.assertEqual(str(g(text)), "1999-09-01 00:00:00+00:00")

    def test_future_dates(self):
        source_expected = [
            ("can you find correct date here 2033", "2033-01-01 00:00:00+00:00"),
            ("can you find correct date here june 2033", "2033-06-01 00:00:00+00:00"),
            ("can you find correct date here 2 june 2033", "2033-06-02 00:00:00+00:00"),
            (
                "can you find correct date here 12 january 2018",
                "2018-01-12 00:00:00+00:00",
            ),
            (
                "can you find correct date here 1 january 2018",
                "2018-01-01 00:00:00+00:00",
            ),
            ("can you find correct date here 31 april 2017", "None"),
            ("can you find correct date here 32 december 2017", "None"),
        ]

        for source, expected in source_expected:
            # print "sourece:", source
            extracted_as_list = (extract_dates(source, debug=False) or [None])[0]
            # print "extracted_as_list:", extracted_as_list
            self.assertEqual(str(extracted_as_list), expected)

            extracted_as_single = extract_date(source)
            # print "extracted_as_single:", extracted_as_single
            self.assertEqual(str(extracted_as_single), expected)

    def test_default_dates(self):

        source = "In year 2011 the incident happened."
        date = extract_dates(source)[0]
        expected = "2011-01-01 00:00:00+00:00"
        self.assertEqual(str(date), str(expected))
        date = extract_date(source)
        self.assertEqual(str(date), str(expected))

        source = "In year 2011 the incident happened."
        date = extract_dates(
            source, default_hour=12, default_minute=14, default_second=12
        )[0]
        expected = "2011-01-01 12:14:12+00:00"
        self.assertEqual(str(date), expected)
        date = extract_date(
            source, default_hour=12, default_minute=14, default_second=12
        )
        self.assertEqual(str(date), expected)

        source = "In year 2011 the incident happened."
        date, precision = extract_date(source, return_precision=True)
        expected = "2011-01-01 00:00:00+00:00"
        self.assertEqual(str(date), expected)
        self.assertEqual(precision, "year")

        source = "In 2 Jan 2011 the incident happened."
        date, precision = extract_date(source, return_precision=True)
        expected = "2011-01-02 00:00:00+00:00"
        self.assertEqual(str(date), expected)
        self.assertEqual(precision, "day")

        #'In 2nd Jan 2011 the incident happened.'
        source = "In Mar 2011 the incident happened."
        date, precision = extract_date(source, return_precision=True)
        expected = "2011-03-01 00:00:00+00:00"
        self.assertEqual(str(date), expected)
        self.assertEqual(precision, "month")

    def test_non_dates(self):
        source = "He was selected by the Sacramento Kings in the 2nd round (48th overall) of the 2004 NBA_Draft. A 6'4' guard from Morehead State University, Minard was signed by the Kings in July 2004, but they waived him in November the same year, and so far he has never appeared in an NBA game."
        dates = extract_dates(source, debug=False)
        self.assertEqual(len(dates), 2)

    def test_date_next_to_text(self):
        source = "some_text_20140205"
        date = extract_date(source, debug=False)
        self.assertEqual(str(date), "2014-02-05 00:00:00+00:00")

        source = "some_text20140205"
        date = extract_date(source, debug=False)
        self.assertEqual(str(date), "2014-02-05 00:00:00+00:00")


if __name__ == "__main__":
    unittest.main()
