#!/bin/bash

# Variables
DOCKER_USERNAME="akhil1993"
IMAGE_NAME="flask-color-changer"
IMAGE_TAG="latest"
FULL_IMAGE_NAME="$DOCKER_USERNAME/$IMAGE_NAME:$IMAGE_TAG"
CONTAINER_NAME="flask-color-changer-container"
HOST_LOG_DIR="$(pwd)/logs"  # Current directory's 'logs' folder

# Check if a port is provided as an argument, else use default 5000
if [ -z "$1" ]; then
  APP_PORT=5000  # Default port
else
  APP_PORT=$1  # Port provided by user
fi

# Step 1: Pull the Docker image from Docker Hub
echo "Pulling the Docker image from Docker Hub..."
docker pull $FULL_IMAGE_NAME
if [ $? -ne 0 ]; then
  echo "Failed to pull Docker image: $FULL_IMAGE_NAME. Please check the image name and credentials."
  exit 1
fi

# Step 2: Stop and remove any existing container with the same name
echo "Stopping and removing any existing containers with the name $CONTAINER_NAME..."
docker stop $CONTAINER_NAME 2>/dev/null || true
docker rm $CONTAINER_NAME 2>/dev/null || true

# Step 3: Create the logs directory in the current directory if it doesn't exist
echo "Creating logs directory in the current directory..."
mkdir -p $HOST_LOG_DIR

# Step 4: Run the Docker container using the pulled image
echo "Running the Docker container on port $APP_PORT..."
docker run -d \
  --name $CONTAINER_NAME \
  -p $APP_PORT:$APP_PORT \
  -v $HOST_LOG_DIR:/app/logs \
  $FULL_IMAGE_NAME

if [ $? -ne 0 ]; then
  echo "Failed to start the Docker container. Please check the logs and configuration."
  exit 1
fi

# Step 5: Provide feedback
echo "Docker container $CONTAINER_NAME is running on port $APP_PORT."
echo "Logs are being saved to $HOST_LOG_DIR."
