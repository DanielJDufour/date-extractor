from csv import DictReader
from datetime import date
from os.path import abspath, dirname, join

from .arabic import toArabic as a

rootdir = dirname(dirname(abspath(__file__)))

datadir = join(rootdir, "data")

# range generates a list of numbers from 1 to 31
# map converts everthing in the list to unicode
days_of_the_month_as_numbers = (
    list(map(str, list(reversed(range(1, 32)))))
    + list(map(lambda n: "0" + str(n), range(0, 10)))
    + list(map(a, list(reversed(range(1, 32)))))
)


with open(join(datadir, "days_of_the_month/ordinal/english.txt")) as f:
    days_of_the_month_as_ordinal = [ln["text"] for ln in DictReader(f) if ln["text"]]

months_verbose = []
for language in ["english", "arabic", "chinese", "french", "sorani", "turkish"]:
    with open(join(datadir, f"months_verbose/{language}.txt"), encoding="utf8") as f:
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
    + list(map(lambda n: "0" + str(n), range(0, 10)))
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
    with open(join(datadir, f"months_verbose/{language}.txt"), encoding="utf8") as f:
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

years_as_numbers = range(1900, current_year + 200)
_years_as_strings = list(map(str, years_as_numbers)) + list(map(a, years_as_numbers))
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

seconds = []
for n in range(0, 10):
    seconds.append("0" + str(n))
for n in range(10, 60):
    seconds.append(str(n))

times = []
for hour in hours:
    for minute in minutes:
        times.append(hour + ":" + minute)
