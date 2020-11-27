import re
from collections import Counter
from datetime import date, datetime

import pytz
import regex

from . import enumerations

flags = re.IGNORECASE | re.MULTILINE | re.UNICODE

# the tzinfo (a.k.a. timezone) defaults to UTC
# you can override this by setting date_extractor.timezone to what you wish
global tzinfo
tzinfo = pytz.UTC

month_to_number = enumerations.month_to_number

# num converts text to a number
def num(text):
    if text:
        if text.isdigit():
            return int(text)
        else:
            text_title = text.title()
            if text_title in month_to_number:
                return month_to_number[text_title]


# normalizes year to four digits
# e.g., 90s to 1990 and 11 to 2011

current_year = date.today().year
next_year_short = int(str(current_year + 1)[2:])
previous_century_short = str(current_year - 100)[0:2]
current_century_short = str(current_year)[0:2]


def normalize_year(y, debug=False):

    if debug:
        print("starting normalize_year with " + str(y))

    # we run int(y) to convert to number just in case arabic
    y_str = str(int(y)).rstrip("s").rstrip("'")
    len_y_str = len(y_str)
    if 1 <= len_y_str <= 2:
        y_int = int(y_str)
        if len_y_str == 1:
            y_str = "0" + y_str
        if y_int > next_year_short:
            y_int = int(previous_century_short + y_str)
        else:
            y_int = int(current_century_short + y_str)
        return y_int
    else:
        return int(y)


def generate_patterns():
    global patterns
    p = {}

    # iterate through the names of the variables in the enumerations
    for key in dir(enumerations):

        # ignore inherited methods that come with most python modules
        # also ignore short variables of 1 length
        if (
            not key.startswith("_")
            and len(key) > 1
            and isinstance(getattr(enumerations, key), list)
        ):
            p[key] = "(?:" + "|".join(getattr(enumerations, key)) + ")"

    # merge months as regular name, abbreviation and number all together
    p["day"] = (
        "(?P<day>"
        + "|".join(
            [p["days_of_the_month_as_numbers"], p["days_of_the_month_as_ordinal"]]
        )
        + ")"
        + "(?!\d{2,4})"
    )

    # merge months as regular name, abbreviation and number all together
    # makes sure that it doesn't pull out 3 as the month in January 23, 2015
    p["month"] = (
        "(?<! \d)"
        + "(?P<month>"
        + "|".join(
            [p["months_verbose"], p["months_abbreviated"], p["months_as_numbers"]]
        )
        + ")"
        + "(?:"
        + "/"
        + p["months_verbose"]
        + ")?"
        + "(?!\d-\d{1,2}T)"
    )

    # spaces or punctuation separatings days, months and years
    # blank space, comma, dash, period, backslash
    # todo: write code for forward slash, an escape character
    # patterns['punctuation'] = "(?P<punctuation>, |:| |,|-|\.|\/|)"
    p["punc"] = "(?:, |:| |,|-|\.|\/|)"
    p["punctuation_fixed_width"] = "(?: |,|;|-|\.|\/)"
    p["punctuation_nocomma"] = "(?: |-|\.|\/)"
    # patterns['punctuation_second'] = "\g<punctuation>"
    p["punctuation_second"] = p["punc"]

    # matches the year as two digits or four
    # tried to match the four digits first
    # (?!, \d{2,4}) makes sure it doesn't pick out 23 as the year in January 23, 2015
    p["year"] = "(?P<year>" + p["years"] + ")" + "(?!th)"

    p["dmy"] = (
        "(?<!\d{2}:)"
        + "(?<!\d)"
        + "(?P<dmy>"
        + p["day"]
        + p["punc"]
        + p["month"]
        + p["punctuation_second"]
        + p["year"]
        + ")"
        + "(?!-\d{1,2})"
        + "(?<!"
        + p["times"]
        + ")"
    )

    p["mdy"] = (
        "(?!\d{2}:)"
        + "(?<!\d{3})"
        + "(?P<mdy>"
        + p["month"]
        + p["punc"]
        + p["day"]
        + "(?:"
        + p["punctuation_second"]
        + "|, )"
        + p["year"]
        + ")"
        + "(?!(-|/|)\d{1,3})"
        + "(?<!"
        + p["nots"]
        + ")"
        + "(?<!"
        + p["times"]
        + ")"
    )

    # we don't include T in the exclusion at end because sometimes T comes before hours and minutes
    p["ymd"] = (
        "(?<![\d])"
        + "(?P<ymd>"
        + p["year"]
        + p["punc"]
        + p["month"]
        + p["punctuation_second"]
        + p["day"]
        + ")"
        + "(?<![^\d]\d{4})"
        + "(?!-\d{1,2}-\d{1,2})"
        + "(?![\dABCDEFGHIJKLMNOPQRSUVWXYZabcdefghijklmnopqrsuvwxyz])"
        + "(?<!"
        + p["nots"]
        + ")"
        + "(?<!"
        + p["times"]
        + ")"
    )

    p["my"] = (
        "(?<!\d{3})"
        + "(?<!32 )"
        + "(?P<my>"
        + p["month"]
        + p["punctuation_nocomma"]
        + p["year"]
        + ")"
    )

    # just the year
    # avoiding 32 december 2017
    p["y"] = (
        "(?<!\d{2}:)"
        + "(?<!\d)"
        + "(?<!"
        + p["months_last_three_letters"]
        + p["punctuation_fixed_width"]
        + ")"
        + "(?P<y>"
        + p["year"]
        + ")"
        + "(?!"
        + p["punctuation_fixed_width"]
        + p["months_abbreviated"]
        + ")"
        + "(?!\d)"
        + "(?!:\d{2})"
    )

    # 公元 = common era
    # 民國 = republic
    p["system"] = "(?P<system>公元|民國)?"

    p["chinese"] = (
        p["system"]
        + "(?P<year>"
        + "|".join([p["years"], "(?P<tw_year>" + p["tw_years"] + ")"])
        + ")"
        + " ?年 ?"
        + "(?P<month>"
        + p["months_as_numbers"]
        + ")"
        + " ?月 ?"
        + "(?P<day>"
        + p["day"]
        + ")"
        + " ?日 ?"
    )

    iso_years = "|".join(map(str, range(1900, current_year + 200)))
    iso_months = "|".join([str(n).zfill(2) for n in range(1, 13)])
    iso_days = "|".join([str(n).zfill(2) for n in range(1, 32)])
    iso_hours = "|".join([str(n).zfill(2) for n in range(0, 24)])
    iso_minutes = "|".join([str(n).zfill(2) for n in range(0, 60)])
    iso_seconds = "|".join([str(n).zfill(2) for n in range(0, 60)])

    p["iso"] = (
        f"(?P<year>{iso_years})-(?P<month>{iso_months})-(?P<day>{iso_days})"
        + "[ T]"
        + f"(?P<hour>{iso_hours}):(?P<minute>{iso_minutes}):(?P<second>{iso_seconds})"
    )

    p["date"] = (
        "(?P<date>"
        + "|".join(
            [p["iso"], p["chinese"], p["mdy"], p["dmy"], p["ymd"], p["my"], p["y"]]
        )
        + ")"
    )
    p["date_compiled"] = regex.compile(p["date"], flags)

    patterns = p


global patterns
generate_patterns()


def datetime_from_dict(
    match,
    debug=False,
    default_hour=0,
    default_minute=0,
    default_second=0,
    return_precision=False,
):

    try:

        if debug:
            print("starting datetime_from_dict with " + str(match))

        month = match.get("month", None)
        if month:
            precision = "month"
        else:
            month = 1
            precision = "year"
        if isinstance(month, int):
            pass
        elif month.isdigit():
            month = int(month)
        else:
            month = month_to_number[month.title()]

        try:
            day = match.get("day", None)
            if day:
                precision = "day"
                day = int(day)
            else:
                day = 1
        except Exception as e:
            # print "exception is", e
            pass

        try:
            if "tw_year" in match:
                year = 1911 + match["tw_year"]
            else:
                year = normalize_year(match["year"], debug=debug)
            # print "year", year
        except Exception as e:
            # print e
            pass

        try:
            hour = int(match["hour"])
        except Exception as e:
            hour = default_hour

        try:
            minute = int(match["minute"])
        except Exception as e:
            minute = default_minute

        try:
            second = int(match["second"])
        except Exception as e:
            second = default_second

        try:
            new_date_time = datetime(
                year,
                month,
                day,
                hour,
                minute,
                second,
                tzinfo=tzinfo,
            )
            if return_precision:
                return (new_date_time, precision)
            else:
                return new_date_time
        except Exception as e:
            # print e
            pass

    except Exception as e:
        print(e)


def is_date_in_list(date, list_of_dates):
    return any((are_dates_same(date, d) for d in list_of_dates))


def are_dates_same(a, b):
    for level in ("year", "month", "day"):
        if level in a and level in b and a[level] != b[level]:
            return False
    return True


def remove_duplicates(seq):
    seen = set()
    return [x for x in seq if not (x in seen or seen.add(x))]


def extract_dates(
    text,
    sorting=None,
    debug=False,
    default_hour=0,
    default_minute=0,
    default_second=0,
    return_precision=False,
    earliest_possible_year=1900,
):
    global patterns

    matches = []
    completes = []
    partials = []

    # print "about to finditer"
    for match in regex.finditer(regex.compile(patterns["date"], flags), text):
        if debug:
            print("\n\nmatch is " + str(match.groupdict()))
        # this goes through the dictionary and removes empties and changes the keys back, e.g. from month_myd to month
        match = dict((k, num(v)) for k, v in match.groupdict().items() if num(v))

        if all(k in match for k in ("day", "month", "year")):
            completes.append(match)
        else:
            partials.append(match)

    if debug:
        print("\ncompletes are " + str(completes))

    # iterate through partials
    # if a more specific date is given in the completes, drop the partial
    # for example if Feb 1, 2014 is picked up and February 2014, too, drop February 2014

    partials = [
        partial for partial in partials if not is_date_in_list(partial, completes)
    ]
    if debug:
        print("\npartials are " + str(partials))

    # convert completes and partials and return list ordered by:
    # complete/partial, most common, most recent
    results = []
    for d in completes + partials:
        try:
            results.append(
                datetime_from_dict(
                    d,
                    debug,
                    default_hour,
                    default_minute,
                    default_second,
                    return_precision,
                )
            )
        except ValueError as e:
            pass

    if sorting:
        counter = Counter(results)
        if return_precision:
            results = remove_duplicates(
                sorted(
                    results,
                    key=lambda x: (counter[x[1]], x[1].toordinal()),
                    reverse=True,
                )
            )
        else:
            results = remove_duplicates(
                sorted(results, key=lambda x: (counter[x], x.toordinal()), reverse=True)
            )

    # average_date = mean([d for d in completes])

    if debug:
        print("extract_dates returning: " + str(results))

    return results


e = extract_dates


def getFirstDateFromText(
    text,
    debug=False,
    default_hour=0,
    default_minute=0,
    default_second=0,
    return_precision=False,
    earliest_possible_year=1900,
):
    # print("starting getFirstDateFromText")
    global patterns

    for match in regex.finditer(patterns["date_compiled"], text):
        # print("\nmatch is", match.group(0))
        # print("\nmatch.index is", ([item for item in match.groupdict().items() if item[1]]))
        if not isDefinitelyNotDate(match.group(0)):
            match = dict((k, num(v)) for k, v in match.groupdict().items() if num(v))
            return datetime_from_dict(
                match,
                debug,
                default_hour,
                default_minute,
                default_second,
                return_precision,
            )
    # print "finishing getFirstDateFromText"


# the date of a webpage, like a blog or article, will often be the first date mentioned
extract_date = g = getPageDate = getFirstDateFromText


def isDefinitelyNotDate(text):
    if re.match("\d{1,2}-\d{1,2}.\d{1,2}", text, flags=flags):
        return True
    return False
