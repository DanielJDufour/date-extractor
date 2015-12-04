#!/bin/bash
version=$(cat setup.py  | grep version | grep -oP '(\d.\d)')
echo 'old version is' $version
left=$(echo $version | grep -oP '\d(?=.)')
right=$(echo $version | grep -oP '(?<=.)\d')

if (( right == 9 )); then
    right=0
    left=$((left+1))
else
    right=$((right+1))
fi
version="$left.$right"
echo "new version is" $version

# replace version in setup.py
sed -i "s/.*version.*/  version = '$version',/" setup.py

git add --all :/
git commit

git tag $version -m "Adds a tag so that we can put this on PyPI."

git push --tags origin master

python setup.py register -r pypi
python setup.py sdist upload -r pypi
