from distutils.core import setup

setup(
  name = 'date-extractor',
  packages = ['date_extractor'],
  package_dir = {'date_extractor': 'date_extractor'},
  package_data = {'date_extractor': ['arabic.py', 'enumerations.py', '__init__.py', 'data/months_verbose/arabic.txt', 'data/months_verbose/french.txt', 'data/months_verbose/sorani.txt', 'data/months_verbose/turkish.txt', 'tests/__init__.py', 'tests/test.py']},
  version = '3.0',
  description = 'Extract dates from text',
  author = 'Daniel J. Dufour',
  author_email = 'daniel.j.dufour@gmail.com',
  url = 'https://github.com/DanielJDufour/date-extractor',
  download_url = 'https://github.com/DanielJDufour/date-extractor/tarball/download',
  keywords = ['date','datetime','python','tagging'],
  classifiers = [],
  install_requires=["pytz"]
)
