# Contributing


## Release Workflow
```bash
git tag $DATE_EXTRACTOR_VERSION
git push --tags origin master
python setup.py sdist
twine upload dist/*
```
