#!/usr/bin/env bash

mkdir -p lambda
pipenv lock -r > requirements.txt
pip install -r requirements.txt --no-deps -t lambda
cd lambda
zip -r ../function.zip .
cd ..
zip -r function.zip api.py
