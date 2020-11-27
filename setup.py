from os import path

from setuptools import setup

this_directory = path.abspath(path.dirname(__file__))

with open(path.join(this_directory, "README.md")) as f:
    long_description = f.read()

setup(
    name="date-extractor",
    packages=["date_extractor"],
    package_dir={"date_extractor": "date_extractor"},
    package_data={
        "date_extractor": [
            "__init__.py",
            "enumerations/__init__.py",
            "enumerations/arabic.py",
            "data/days_of_the_month/ordinal/english.txt",
            "data/days_of_the_week/full/english.txt",
            "data/days_of_the_week/short/english.txt",
            "data/months_verbose/arabic.txt",
            "data/months_verbose/chinese.txt",
            "data/months_verbose/english.txt",
            "data/months_verbose/french.txt",
            "data/months_verbose/sorani.txt",
            "data/months_verbose/turkish.txt",
            "tests/__init__.py",
            "tests/test.py",
        ]
    },
    version="5.1.5",
    description="Extract dates from text",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Daniel J. Dufour",
    author_email="daniel.j.dufour@gmail.com",
    url="https://github.com/DanielJDufour/date-extractor",
    download_url="https://github.com/DanielJDufour/date-extractor/tarball/download",
    keywords=["date", "datetime", "python", "tagging"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    install_requires=["pytz", "regex"],
)
