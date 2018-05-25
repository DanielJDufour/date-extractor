import setuptools

print("starting setup.py")

with open("README.md") as f:
    long_description = f.read()

print("long_description:", long_description)

setuptools.setup(
    name = 'date-extractor',
    version = '3.9.1',
    author = 'Daniel J. Dufour',
    author_email = 'daniel.j.dufour@gmail.com',
    description = 'Extract dates from text',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url = 'https://github.com/DanielJDufour/date-extractor',
    project_urls={
        "Source": "https://github.com/DanielJDufour/date-extractor",
        "Tracker": "https://github.com/DanielJDufour/date-extractor/issues"
    },
    packages=setuptools.find_packages(),
    package_data = {'date_extractor': ['arabic.py', 'enumerations.py', '__init__.py', 'data/months_verbose/arabic.txt', 'data/months_verbose/french.txt', 'data/months_verbose/sorani.txt', 'data/months_verbose/turkish.txt', 'tests/__init__.py', 'tests/test.py']},
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Development Status :: 6 - Mature",
        "Intended Audience :: Developers",
        "Natural Language :: English"
    ),
    keywords = "data datetime extraction python tagging",
    install_requires=["pytz"]
)
