#!/bin/bash
version=$(cat setup.py  | grep version | grep -oP '(\d.\d)')
echo 'version is' $version
left=$(echo $version | grep -oP '\d(?=.)')
echo 'left is' $left
right=$(echo $version | grep -oP '(?<=.)\d')
echo 'right is' $right

if (( right == 9 )); then
    echo "right is 9"
    right=0
    left=$((left+1))
    echo "left is" $left
else
    echo "right is not 9, so just add 1 to right"
    right=$((right+1))
fi
version="$left.$right"
echo "version is" $version

# replace version in setup.py
sed -i "s/.*version.*/  version = '$version',/" setup.py

git tag $version -m "Adds a tag so that we can put this on PyPI."

git push --tags origin master
