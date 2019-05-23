#!/usr/bin/env bash

aws lambda update-function-code \
  --function-name timeseries_data_generate \
  --zip-file fileb://function.zip
