#!/bin/bash

aws dynamodb batch-write-item \
  --request-items "$(jq -c . table_data.json)" \
  --return-consumed-capacity TOTAL