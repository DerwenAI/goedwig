#!/bin/bash -e

TAG=$(git tag | sort -r | head -1)
echo "'git tag'" > goedwig/tag.py 
echo "TAG = '$TAG'" >> goedwig/tag.py

rm -rf dist
python setup.py sdist bdist_wheel

twine upload --verbose dist/*
