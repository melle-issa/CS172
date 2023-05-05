#!/bin/bash

echo 'installing beautifulsoup'
pip3 install beautifulsoup4

echo 'installing lmxl'
pip3 install lxml

echo 'installing request libraries'
pip3 install lxml



seedFile="${1#*:}"
numPages="${3#*:}"
hopsAway="${2#*:}"
outputDir="$4"

echo 'running'
python3 main.py "$seedFile" $numPages $hopsAway "$outputDir"
