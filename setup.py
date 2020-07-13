from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))

with open(path.join(this_directory, 'README.md')) as f:
    long_description = f.read()

setup(
  name = 'date-extractor',
  packages = ['date_extractor'],
  package_dir = {'date_extractor': 'date_extractor'},
  package_data = {'date_extractor': ['arabic.py', 'enumerations.py', '__init__.py', 'data/months_verbose/arabic.txt', 'data/months_verbose/chinese.txt', 'data/months_verbose/french.txt', 'data/months_verbose/sorani.txt', 'data/months_verbose/turkish.txt', 'tests/__init__.py', 'tests/test.py']},
  version = "5.0.0",
  description = 'Extract dates from text',
  long_description = long_description,
  long_description_content_type='text/markdown',
  author = 'Daniel J. Dufour',
  author_email = 'daniel.j.dufour@gmail.com',
  url = 'https://github.com/DanielJDufour/date-extractor',
  download_url = 'https://github.com/DanielJDufour/date-extractor/tarball/download',
  keywords = ['date','datetime','python','tagging'],
  classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 3',
    'License :: OSI Approved :: Apache Software License',
    'Operating System :: OS Independent',
  ],
  install_requires=["pytz", "regex"]
)
