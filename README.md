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
