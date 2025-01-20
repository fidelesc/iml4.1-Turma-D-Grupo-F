#!/bin/bash

# Exit script on any error
set -e

# Define container and volume variables
IMAGE_NAME="webscraper"
CONTAINER_VOLUME="/app/data"

# Detect OS and set volume paths accordingly
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    # Windows (Git Bash or similar)
    HOST_VOLUME="$(pwd -W)/data" # Convert to Windows-style path
else
    # Linux/MacOS
    HOST_VOLUME="$(pwd)/data"
fi

# Ensure the host data directory exists
mkdir -p "$HOST_VOLUME"

# Run Docker container with volume mapping
echo "Running Docker container with host volume: $HOST_VOLUME"
docker run --rm -v "$HOST_VOLUME:$CONTAINER_VOLUME" "$IMAGE_NAME"

echo "Docker container finished execution. Output should be in the 'data' folder."
