from .arabic import toArabic as a
from os.path import abspath, dirname
from datetime import date

dirpath = dirname(abspath(__file__))

days_of_the_week_verbose = [
    "Sunday",
    "Monday",
    "Tuesday",
    "Wednesday",
    "Wenesday",
    "Wendsday",
    "Thursday",
    "Friday",
    "Saturday",
]

days_of_the_week_abbreviated = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

# range generates a list of numbers from 1 to 31
# map converts everthing in the list to unicode
days_of_the_month_as_numbers = (
    list(map(str, list(reversed(range(1, 32)))))
    + list(map(lambda n: u"0" + str(n), range(0, 10)))
    + list(map(a, list(reversed(range(1, 32)))))
)


days_of_the_month_as_ordinal = [
    "1st",
    "1th",
    "2nd",
    "2th",
    "3rd",
    "3th",
    "4th",
    "5th",
    "6th",
    "7th",
    "8th",
    "9th",
    "10th",
    "11th",
    "12th",
    "13th",
    "14th",
    "15th",
    "16th",
    "17th",
    "18th",
    "19th",
    "20th",
    "21st",
    "21th",
    "22nd",
    "22th",
    "23rd",
    "23th",
    "24th",
    "25th",
    "26th",
    "27th",
    "28th",
    "29th",
    "30th",
    "31st",
    "31th",
]

months_verbose = [
    "January",
    "Febuary",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]

for language in ("arabic", "chinese", "french", "sorani", "turkish"):
    with open(
        dirpath + "/data/months_verbose/" + language + ".txt", encoding="utf-8"
    ) as f:
        for line in f:
            try:
                line = line.strip()
                if line and not line.startswith("#"):
                    months_verbose.append(line.split(">")[0].strip())
            except Exception as e:
                print("[date-extractor] caught exception: " + str(e))

months_last_three_letters = [
    month[-3:] if len(month[-3:]) == 3 else " " + month[-2:] for month in months_verbose
]

months_abbreviated = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
]

# range generates a list of numbers from 1 to 12
# map converts everthing in the list to unicode
months_as_numbers = (
    list(map(str, range(1, 13)))
    + list(map(lambda n: u"0" + str(n), range(0, 10)))
    + list(map(a, range(1, 13)))
)

month_to_number = {
    "Jan": 1,
    "January": 1,
    "Feb": 2,
    "Febuary": 2,
    "February": 2,
    "Mar": 3,
    "March": 3,
    "Apr": 4,
    "April": 4,
    "May": 5,
    "Jun": 6,
    "June": 6,
    "Jul": 7,
    "July": 7,
    "Aug": 8,
    "August": 8,
    "Sep": 9,
    "Sept": 9,
    "September": 9,
    "Oct": 10,
    "October": 10,
    "Nov": 11,
    "November": 11,
    "Dec": 12,
    "December": 12,
}

for language in ("arabic", "chinese", "french", "sorani", "turkish"):
    with open(
        dirpath + "/data/months_verbose/" + language + ".txt", encoding="utf-8"
    ) as f:
        for line in f:
            try:
                line = line.strip()
                if line and not line.startswith("#"):
                    splat = line.split(">")
                    month_to_number[splat[0].strip()] = splat[1].strip()
            except Exception as e:
                print("[date-extractor] caught exception: " + str(e))

current_year = date.today().year

current_year_abbreviated = int(str(current_year)[-2:])

_years_as_numbers = range(1900, current_year + 200)
_years_as_strings = list(map(str, _years_as_numbers)) + list(map(a, _years_as_numbers))
years = _years_as_strings + [y[-2:] for y in _years_as_strings]

tw_years = list(map(str, range(0, current_year - 1912 + 2 + 100)))

nots = []
for short_y in range(int(str(current_year + 2)[-2:]) + 2, 85):
    for m in range(1, 10):
        for d in range(1, 10):
            nots.append(str(short_y) + str(m) + str(d))

hours = []
for n in range(0, 10):
    hours.append("0" + str(n))
for n in range(10, 24):
    hours.append(str(n))

minutes = []
for n in range(0, 10):
    minutes.append("0" + str(n))
for n in range(10, 60):
    minutes.append(str(n))


minutes = []
for n in range(0, 10):
    minutes.append("0" + str(n))
for n in range(10, 60):
    minutes.append(str(n))

times = []
for hour in hours:
    for minute in minutes:
        times.append(hour + ":" + minute)
