#!/bin/bash

# Define the image name and container name
IMAGE_NAME="flask-color-changer"
CONTAINER_NAME="flask-color-changer-container"
HOST_LOG_DIR="$(pwd)/logs"  # Current directory's 'logs' folder

# Check if a port is provided as an argument, else use default 5000
if [ -z "$1" ]; then
  APP_PORT=5000  # Default port
else
  APP_PORT=$1  # Port provided by user
fi

# Step 1: Build the Docker image
echo "Building the Docker image..."
docker build -t $IMAGE_NAME .

# Step 2: Check if the container is already running, and if so, stop it
echo "Stopping and removing any existing containers with the name $CONTAINER_NAME..."
docker stop $CONTAINER_NAME 2>/dev/null || true
docker rm $CONTAINER_NAME 2>/dev/null || true

# Step 3: Create the logs directory in the current directory if it doesn't exist
echo "Creating logs directory in the current directory..."
mkdir -p $HOST_LOG_DIR

# Step 4: Run the Docker container
echo "Running the Docker container on port $APP_PORT..."
docker run -d \
  --name $CONTAINER_NAME \
  -p $APP_PORT:$APP_PORT \
  -v $HOST_LOG_DIR:/app/logs \
  $IMAGE_NAME

# Step 5: Provide feedback
echo "Docker container $CONTAINER_NAME is running on port $APP_PORT."
echo "Logs are being saved to $HOST_LOG_DIR."
