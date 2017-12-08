from sys import version_info
python_version = version_info.major


from .arabic import toArabic as a
from os.path import abspath, dirname
from datetime import date

dirpath = dirname(abspath(__file__))

days_of_the_week_verbose = ["Sunday","Monday","Tuesday","Wednesday","Wenesday","Wendsday","Thursday","Friday","Saturday"]

days_of_the_week_abbreviated = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]

# range generates a list of numbers from 1 to 31
# map converts everthing in the list to unicode
if python_version == 2:
    days_of_the_month_as_numbers = map(unicode, list(reversed(range(1,32)))) + map(lambda n : u"0"+unicode(n),range(0, 10)) + map(a, list(reversed(range(1,32))))
elif python_version == 3:
    days_of_the_month_as_numbers = list(map(str, list(reversed(range(1,32))))) + list(map(lambda n : u"0"+str(n),range(0, 10))) + list(map(a, list(reversed(range(1,32)))))
    

# ordinal is a function that converts a number to its ordinal
# for example it converts 22 to 22nd
# we start it with __ because we want to keep it private
__ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n/10%10!=1)*(n%10<4)*n%10::4])
days_of_the_month_as_ordinal = [__ordinal(n) for n in range(1,32)]

months_verbose = ["January","Febuary","February","March","April","May","June","July","August","September","October","November","December"]

for language in ("arabic", "french", "sorani", "turkish"):
    if python_version == 2:
        with open(dirpath + "/data/months_verbose/" + language + ".txt") as f:
            for line in f:
                try:
                    line = line.decode("utf-8").strip()
                    if line and not line.startswith("#"):
                        months_verbose.append(line.split(">")[0].strip())
                except Exception as e:
                    print("[date-extractor] caught exception: " + str(e))
    elif python_version == 3:
        with open(dirpath + "/data/months_verbose/" + language + ".txt", encoding="utf-8") as f:
            for line in f:
                try:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        months_verbose.append(line.split(">")[0].strip())
                except Exception as e:
                    print("[date-extractor] caught exception: " + str(e))

months_last_three_letters = [month[-3:] if len(month[-3:]) == 3 else " " + month[-2:] for month in months_verbose]

months_abbreviated = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"] 

# range generates a list of numbers from 1 to 12
# map converts everthing in the list to unicode
if python_version == 2:
    months_as_numbers = map(unicode,range(1,13)) + map(lambda n : u"0"+unicode(n),range(0, 10)) + map(a,range(1,13))
elif python_version == 3:
    months_as_numbers = list(map(str,range(1,13))) + list(map(lambda n : u"0"+str(n),range(0, 10))) + list(map(a,range(1,13)))

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
        "December": 12
        }

for language in ("arabic", "french", "sorani", "turkish"):


    if python_version == 2:
        with open(dirpath + "/data/months_verbose/" + language + ".txt") as f:
            for line in f:
                try:
                    line = line.decode("utf-8").strip()
                    if line and not line.startswith("#"):
                        splat = line.split(">")
                        month_to_number[splat[0].strip()] = splat[1].strip()
                except Exception as e:
                    print("[date-extractor] caught exception: " + str(e))
    elif python_version == 3:
        with open(dirpath + "/data/months_verbose/" + language + ".txt", encoding="utf-8") as f:
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

_years_as_numbers = range(1900, current_year+200)
if python_version == 2:
    _years_as_strings = map(unicode,_years_as_numbers) + map(a,_years_as_numbers)
elif python_version == 3:
    _years_as_strings = list(map(str,_years_as_numbers)) + list(map(a,_years_as_numbers))
years = _years_as_strings + [y[-2:] for y in _years_as_strings]

nots = []
for short_y in range( int(str(current_year+2)[-2:]) + 2, 85):
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

times = []
for hour in hours:
    for minute in minutes:
        times.append(hour + ":" + minute)
