from sys import version_info
python_version = version_info.major

from collections import Counter
from datetime import date, datetime
from . import enumerations
import pytz
import re

flags = re.IGNORECASE|re.MULTILINE|re.UNICODE

# the tzinfo (a.k.a. timezone) defaults to UTC
# you can override this by setting date_extractor.timezone to what you wish
global tzinfo
tzinfo = pytz.UTC

month_to_number = enumerations.month_to_number

#num converts text to a number
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
next_year_short = int(str(current_year+1)[2:])
previous_century_short = str(current_year-100)[0:2]
current_century_short = str(current_year)[0:2]
def normalize_year(y, debug=False):

    if debug: print("starting normalize_year with " + str(y))

    # we run int(y) to convert to number just in case arabic
    y_str = str(int(y)).rstrip('s').rstrip("'")
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
    patterns = {}

    # iterate through the names of the variables in the enumerations
    for key in dir(enumerations):

        # ignore inherited methods that come with most python modules
        # also ignore short variables of 1 length
        if not key.startswith("_") and len(key) > 1 and isinstance(getattr(enumerations, key), list):
            pattern = "(?:" + "|".join(getattr(enumerations, key)) + ")"

            # check to see if pattern is in unicode
            # if it's not convert it
            if python_version == 2 and isinstance(pattern, str):
                pattern = pattern.decode("utf-8")

            patterns[key] = pattern

    #merge months as regular name, abbreviation and number all together
    patterns['day'] = u'(?P<day>' + patterns['days_of_the_month_as_numbers'] + u'|' + patterns['days_of_the_month_as_ordinal'] + ')(?!\d{2,4})'

    #merge months as regular name, abbreviation and number all together
    # makes sure that it doesn't pull out 3 as the month in January 23, 2015
    patterns['month'] = u'(?<! \d)(?P<month>' + patterns['months_verbose'] + u'|' + patterns['months_abbreviated'] + u'|' + patterns['months_as_numbers'] + u')' + u"(?:" + "/" + patterns['months_verbose'] + u")?" + u"(?!\d-\d{1,2}T)"

    # spaces or punctuation separatings days, months and years
    # blank space, comma, dash, period, backslash
    # todo: write code for forward slash, an escape character
    #patterns['punctuation'] = u"(?P<punctuation>, |:| |,|-|\.|\/|)"
    patterns['punctuation'] = u"(?:, |:| |,|-|\.|\/|)"
    patterns['punctuation_fixed_width'] = u"(?: |,|;|-|\.|\/)"
    patterns['punctuation_nocomma'] = u"(?: |-|\.|\/)"
    #patterns['punctuation_second'] = u"\g<punctuation>"
    patterns['punctuation_second'] = patterns['punctuation']

    # matches the year as two digits or four
    # tried to match the four digits first
    # (?!, \d{2,4}) makes sure it doesn't pick out 23 as the year in January 23, 2015
    patterns['year'] = u"(?P<year>" + patterns['years'] + u")" + "(?!th)"

    patterns['dmy'] = u"(?<!\d{2}:)" + u"(?<!\d)" + u"(?P<dmy>" + patterns['day'].replace("day", "day_dmy") + patterns['punctuation'].replace("punctuation","punctuation_dmy") + patterns['month'].replace("month","month_dmy") + patterns['punctuation_second'].replace("punctuation","punctuation_dmy") + patterns['year'].replace("year", "year_dmy") + u")" + u"(?!-\d{1,2})" + "(?<!" + patterns['times'] + ")"

    patterns['mdy'] =  u"(?!\d{2}:)" + u"(?<!\d{3})" + u"(?P<mdy>" + patterns['month'].replace("month", "month_mdy") + patterns['punctuation'].replace("punctuation","punctuation_mdy") + patterns['day'].replace("day","day_mdy") + "(?:" + patterns['punctuation_second'].replace("punctuation","punctuation_mdy") + "|, )" + patterns['year'].replace("mdy","year_mdy") + u")" + u"(?!(-|/|)\d{1,3})" + "(?<!" + patterns['nots'] + ")" + "(?<!" + patterns['times'] + ")"


    #we don't include T in the exclusion at end because sometimes T comes before hours and minutes
    patterns['ymd'] = u"(?<![\dA-Za-z])" + u"(?P<ymd>" + patterns['year'].replace("year","year_ymd") + patterns['punctuation'].replace("punctuation","punctuation_ymd") + patterns['month'].replace("month","month_ymd") + patterns['punctuation_second'].replace("punctuation","punctuation_ymd") + patterns['day'].replace("day","day_ymd") + u")" + "(?<![^\d]\d{4})" + u"(?!-\d{1,2}-\d{1,2})(?![\dABCDEFGHIJKLMNOPQRSUVWXYZabcdefghijklmnopqrsuvwxyz])" + "(?<!" + patterns['nots'] + ")" + "(?<!" + patterns['times'] + ")"

    patterns['my'] = u"(?<!\d{3})" + u"(?<!32 )" + u"(?P<my>" + patterns['month'].replace("month","month_my") + patterns['punctuation_nocomma'] + patterns['year'].replace("year","year_my") + u")"

    # just the year
    # avoiding 32 december 2017
    patterns['y'] = u"(?<!\d{2}:)" + "(?<!\d)" + "(?<!" + patterns['months_last_three_letters'] + patterns['punctuation_fixed_width'] + ")" +  u"(?P<y>" + patterns['year'].replace("year","year_y") + u")" + "(?!" + patterns['punctuation_fixed_width'] + patterns['months_abbreviated'] + ")" + u"(?!\d)" + u"(?!:\d{2})"
    patterns['date'] = date = u"(?P<date>" + patterns['mdy'] + "|" + patterns['dmy'] + "|" + patterns['ymd'] + "|" + patterns['my'] + "|" + patterns['y'] + u")"

    patterns['date_compiled'] = re.compile(date, flags)

global patterns
generate_patterns()

def datetime_from_dict(match, debug=False, default_hour=0, default_minute=0, default_second=0, return_precision=False):

    try:

        if debug: print("starting datetime_from_dict with " + str(match))

        month = match.get('month', None)
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
            #print "exception is", e
            pass

        try:
            year = normalize_year(match["year"], debug=debug)
            #print "year", year 
        except Exception as e:
            #print e
            pass

        try:
            new_date_time = datetime(year, month, day, default_hour, default_minute, default_second, tzinfo=tzinfo)
            if return_precision:
                return (new_date_time, precision)
            else:
                return new_date_time
        except Exception as e:
            #print e
            pass

    except Exception as e:
        print(e)

def is_date_in_list(date, list_of_dates):
    return any((are_dates_same(date, d) for d in list_of_dates))

def are_dates_same(a,b):
    for level in ("year","month","day"):
        if level in a and level in b and a[level] != b[level]:
            return False
    return True
    

def remove_duplicates(seq):
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if not (x in seen or seen_add(x))]
 
def extract_dates(text, sorting=None, debug=False, default_hour=0, default_minute=0, default_second=0, return_precision=False):
    global patterns

    # convert to unicode if the text is in a bytestring
    # we conver to unicode because it is easier to work with
    # and it handles text in foreign languages much better
    if python_version == 2 and isinstance(text, str):
        text = text.decode('utf-8')

    matches = []
    completes = []
    partials = []

    #print "about to finditer"
    for match in re.finditer(re.compile(patterns['date'], flags), text):
        if debug: print("\n\nmatch is " + str(match.groupdict()))
        # this goes through the dictionary and removes empties and changes the keys back, e.g. from month_myd to month
        if python_version == 2:
            match = dict((k.split("_")[0], num(v)) for k, v in match.groupdict().iteritems() if num(v))
        elif python_version == 3:
            match = dict((k.split("_")[0], num(v)) for k, v in match.groupdict().items() if num(v))

        if all(k in match for k in ("day","month", "year")): 
            completes.append(match)
        else:
            partials.append(match)

    if debug: print("\ncompletes are " + str(completes))

    # iterate through partials
    # if a more specific date is given in the completes, drop the partial
    # for example if Feb 1, 2014 is picked up and February 2014, too, drop February 2014

    partials = [partial for partial in partials if not is_date_in_list(partial, completes)]
    if debug: print("\npartials are " +  str(partials))
  
    # convert completes and partials and return list ordered by:
    # complete/partial, most common, most recent
    results = []
    for d in completes + partials:
        try:
            results.append(datetime_from_dict(d, debug, default_hour, default_minute, default_second, return_precision))
        except ValueError as e:
            pass

    if sorting:
        counter = Counter(results)
        if return_precision:
            results = remove_duplicates(sorted(results, key = lambda x: (counter[x[1]], x[1].toordinal()), reverse=True))
        else:
            results = remove_duplicates(sorted(results, key = lambda x: (counter[x], x.toordinal()), reverse=True))

    #average_date = mean([d for d in completes])

    if debug: print("extract_dates returning: " + str(results)) 

    return results
e=extract_dates

def getFirstDateFromText(text, debug=False, default_hour=0, default_minute=0, default_second=0, return_precision=False):
    #print("starting getFirstDateFromText")
    global patterns

    # convert to unicode if the text is in a bytestring
    # we conver to unicode because it is easier to work with
    # and it handles text in foreign languages much better
    if python_version == 2 and isinstance(text, str):
        text = text.decode('utf-8')

    for match in re.finditer(patterns['date_compiled'], text):
        #print("\nmatch is", match.group(0))
        #print("\nmatch.index is", ([item for item in match.groupdict().items() if item[1]]))
        if not isDefinitelyNotDate(match.group(0)):
            if python_version == 2:
                match = dict((k.split("_")[0], num(v)) for k, v in match.groupdict().iteritems() if num(v))
            elif python_version == 3:
                match = dict((k.split("_")[0], num(v)) for k, v in match.groupdict().items() if num(v))
            return datetime_from_dict(match, debug, default_hour, default_minute, default_second, return_precision)
    #print "finishing getFirstDateFromText"

# the date of a webpage, like a blog or article, will often be the first date mentioned
extract_date = g = getPageDate = getFirstDateFromText


def isDefinitelyNotDate(text):
    if re.match("\d{1,2}-\d{1,2}.\d{1,2}",text, flags=flags):
        return True 
    return False
