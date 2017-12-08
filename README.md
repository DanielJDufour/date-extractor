[![Build Status](https://travis-ci.org/DanielJDufour/date-extractor.svg?branch=master)](https://travis-ci.org/DanielJDufour/date-extractor)

[![Requirements Status](https://requires.io/github/DanielJDufour/date-extractor/requirements.svg?branch=master)](https://requires.io/github/DanielJDufour/date-extractor/requirements/?branch=master)

[![Hex.pm](https://img.shields.io/hexpm/l/plug.svg?maxAge=2592000?style=plastic)]()

# date-extractor
date-extractor helps you extract dates from text

# Installation
```
pip install pytz
pip install date-extractor
```

# Use
```
from date_extractor import extract_dates
text = "I arrived in that city on January 4, 1937"
dates = extract_dates(text)
```

# Returning Precision
```
from date_extractor import extract_date
text = "I arrived in that city in 1937"
date, precision = extract_date(text, return_precision=True)
# precision = 'year'
```


# Features
| Languages Supported |
| ------------------- |
| Arabic |
| English |
| French |
| Sorani (Kurdish) |
| Turkish |

# Testing
To test the package run
```
python -m unittest date_extractor.tests.test
```

If you are using Python 3, you may need to run the following to test
```
python3 -m unittest date_extractor.tests.test
```

# Versions
Works on Python 2 and 3!

# Users
If you use date-extractor and don't mind sharing that, let us know and we can note it on the Readme.  It will be helpful for potential users to see how people are using it.
