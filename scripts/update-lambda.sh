#!/usr/bin/env bash

aws lambda update-function-code \
  --function-name personality-graphs-api \
  --s3-bucket colejhudson \
  --s3-key functions/personality-graphs-api/function.zip \
  --publish
