#!/bin/bash -e

git tag | sort -r | head -1 > TAG

rm -rf dist
python setup.py sdist bdist_wheel

twine upload --verbose dist/*
