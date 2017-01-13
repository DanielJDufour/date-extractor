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

# Versions
Works on Python 2 and 3!
