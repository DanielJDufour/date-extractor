
# make sure libraries used for publishing are up to date
python3 -m pip install --user --upgrade setuptools wheel twine
pip install --upgrade twine

python3 setup.py sdist
