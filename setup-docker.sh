#!/bin/bash

# Exit script on any error
set -e

# Variables
IMAGE_NAME="webscraper"
DOCKERFILE=".devcontainer/Dockerfile"
CONTEXT="."

# Functions
function build_image() {
    echo "Building Docker image '${IMAGE_NAME}'..."
    docker build -f "$DOCKERFILE" -t "$IMAGE_NAME" "$CONTEXT"
    echo "Docker image '${IMAGE_NAME}' built successfully."
}

function run_container() {
    echo "Running Docker container from image '${IMAGE_NAME}'..."
    docker run --rm "$IMAGE_NAME"
    echo "Docker container exited."
}

# Script Execution
echo "Setting up Docker environment for the team..."

# Check if Docker is installed
if ! command -v docker &> /dev/null
then
    echo "Error: Docker is not installed. Please install Docker and try again."
    exit 1
fi

# Build the Docker image
build_image

# Run the Docker container
run_container

echo "Docker setup complete. Project is ready to run!"

# FOR WINDOWS USE GIT BASH
# Make it executable with:
# chmod +x setup-docker.sh
# RUN THE SCRIPT
# ./setup-docker.sh