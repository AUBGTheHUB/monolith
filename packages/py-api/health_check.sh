#!/bin/bash

URL="http://localhost:6969/v2/health"
response=$(curl -s -w "%{http_code}" $URL)

status_code=${response: -3}

if [ $status_code -eq 200 ]; then
    echo "Request successful (Status Code: 200)"
else
    echo "Request failed with the following status code: ${status_code}"
    echo "Response: ${response%???}"
    exit 1
fi
