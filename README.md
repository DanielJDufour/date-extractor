[![Build Status](https://travis-ci.org/DanielJDufour/date-extractor.svg?branch=master)](https://travis-ci.org/DanielJDufour/date-extractor)

[![Requirements Status](https://requires.io/github/DanielJDufour/date-extractor/requirements.svg?branch=master)](https://requires.io/github/DanielJDufour/date-extractor/requirements/?branch=master)

[![Hex.pm](https://img.shields.io/hexpm/l/plug.svg?maxAge=2592000?style=plastic)]()

# date-extractor
date-extractor helps you extract dates from text

# Installation
```
pip3 install date-extractor
```

# Use
```python
from date_extractor import extract_dates

text = "I arrived in that city on January 4, 1937"
dates = extract_dates(text)
# [datetime.datetime(1937, 1, 4, 0, 0, tzinfo=<UTC>)]
```

Date extractor also works on dates with hours, minutes and seconds:
```python
from date_extractor import extract_date

date = extract_date("2018-06-07 16:31:54")
# datetime.datetime(2018, 6, 7, 16, 31, 54, tzinfo=<UTC>)
```

# Returning Precision
```python
from date_extractor import extract_date

text = "I arrived in that city in 1937"
date, precision = extract_date(text, return_precision=True)
# precision = 'year'
```


# Features
| Languages Supported |
| ------------------- |
| Arabic |
| Chinese (incl. Taiwan) |
| English |
| French |
| Sorani (Kurdish) |
| Turkish |

# Testing
To test the package run
```
python3 -m unittest date_extractor.tests.test
```

# Support
Contact Daniel Dufour at daniel.j.dufour@gmail.com
