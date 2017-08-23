#!/bin/bash

find src -name '*.pyc' -delete
find tests -name '*.pyc' -delete
rm -rf build dist src/*.egg-info *.egg-info __pycache__
