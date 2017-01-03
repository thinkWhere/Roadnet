#!/usr/bin/env bash

# Remove old pyc files that may exist from previous branches
find ./ -iname "*.pyc" -delete

# Run tests using virtual frame buffer
xvfb-run nosetests --with-coverage \
          --exe \
          --cover-erase \
          --cover-package Roadnet \
          --with-xunit --xunit-file=shippable/testresults/nosetests.xml $1 $2

coverage xml -o shippable/codecoverage/coverage.xml
