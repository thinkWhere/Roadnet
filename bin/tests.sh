#!/usr/bin/env bash
find ./ -iname "*.pyc" -delete

nosetests --with-coverage \
          --exe \
          --cover-erase --cover-html \
          --cover-package Roadnet  $1 $2
