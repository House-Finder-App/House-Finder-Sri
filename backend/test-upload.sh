#!/bin/bash

# Check if an image file was provided
if [ -z "$1" ]; then
    echo "Usage: ./test-upload.sh <path-to-image>"
    exit 1
fi

# Check if the file exists
if [ ! -f "$1" ]; then
    echo "Error: File '$1' not found"
    exit 1
fi

# Test coordinates (San Francisco)
LAT=37.7749
LNG=-122.4194

# Send the image to our endpoint
curl -X POST \
  -H "Content-Type: multipart/form-data" \
  -F "image=@$1" \
  -F "lat=$LAT" \
  -F "lng=$LNG" \
  http://localhost:5000/api/image/upload

echo # Add a newline at the end 