from arabic import toArabic as a
from os.path import abspath, dirname
from datetime import date

dirpath = dirname(abspath(__file__))

days_of_the_week_verbose = ["Sunday","Monday","Tuesday","Wednesday","Wenesday","Wendsday","Thursday","Friday","Saturday"]

days_of_the_week_abbreviated = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]

# range generates a list of numbers from 1 to 31
# map converts everthing in the list to unicode
days_of_the_month_as_numbers = map(unicode, list(reversed(range(1,32)))) + map(lambda n : u"0"+unicode(n),range(0, 10)) + map(a, list(reversed(range(1,32))))

# ordinal is a function that converts a number to its ordinal
# for example it converts 22 to 22nd
# we start it with __ because we want to keep it private
__ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n/10%10!=1)*(n%10<4)*n%10::4])
days_of_the_month_as_ordinal = [__ordinal(n) for n in range(1,32)]

months_verbose = ["January","Febuary","February","March","April","May","June","July","August","September","October","November","December"]

#for language in ("arabic", "french", "kurdish", "turkish"):
for language in ["arabic"]:
    with open(dirpath + "/data/months_verbose/" + language + ".txt") as f:
        months_verbose += [line.strip().split(">")[0].strip() for line in f.read().decode("utf-8").split("\n") if line and not line.startswith("#")]


months_abbreviated = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"] 

# range generates a list of numbers from 1 to 12
# map converts everthing in the list to unicode
months_as_numbers = map(unicode,range(1,13)) + map(lambda n : u"0"+unicode(n),range(0, 10)) + map(a,range(1,13))

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

for language in ["arabic"]:
    with open(dirpath + "/data/months_verbose/" + language + ".txt") as f:
        for line in f.read().decode("utf-8").split("\n"):
            if line and not line.startswith("#"):
                split = line.strip().split(">")
                month_to_number[split[0].strip()] = split[1].strip()

current_year = date.today().year
curent_year_abbreviated = int(str(current_year)[-2:])
years = map(unicode,range(1990, current_year+1)) + [u"15",u"16"] + map(a,range(1990, current_year+1))
