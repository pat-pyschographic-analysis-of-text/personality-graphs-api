#!/usr/bin/env bash

AWS_USER_ID=$(aws sts get-caller-identity | jq '.["UserId"]' | tr -d '"')

aws lambda create-function \
  --function-name timeseries_data_generate \
  --runtime python3.7 \
  --handler api.main \
  --timeout 30 \
  --role arn:aws:iam::$AWS_USER_ID:role/aws-lambda-cli-role \
  --zip-file fileb://function.zip
