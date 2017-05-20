#!/bin/bash
rm source/tmp.jpg
rm source/logs/*
find ./ -name *.pyc -exec rm {} +
patool create findrecipe.zip source/
