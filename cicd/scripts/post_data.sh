#!/bin/bash

curl -X POST $1/books \
  -H 'Content-Type: application/json' \
  -d '{"authors": ["Eric Tung"],"description": "Test data for POST Endpoint","isbn": "1111111111111","name":"string","title": "Test Book"}'