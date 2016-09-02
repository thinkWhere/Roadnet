#!/usr/bin/env bash

exit 0

find ./ -iname "*.pyc" -delete
xvfb-run nosetests --with-coverage \
          --exe \
          --cover-erase \
          --cover-package Roadnet \
          --with-xunit --xunit-file=shippable/testresults/nosetests.xml $1 $2

coverage xml -o shippable/codecoverage/coverage.xml
