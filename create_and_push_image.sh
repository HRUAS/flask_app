#!/bin/bash

# Variables (replace these with your Docker Hub credentials and image name)
DOCKER_USERNAME="akhil1993"
DOCKER_IMAGE_NAME="flask-color-changer"
DOCKER_TAG="latest"  # Change this to a version/tag if needed

# Step 1: Log in to Docker Hub
echo "Logging in to Docker Hub..."
docker login -u "$DOCKER_USERNAME"
if [ $? -ne 0 ]; then
  echo "Docker login failed. Please check your credentials."
  exit 1
fi

# Step 2: Build the Docker image
echo "Building the Docker image..."
docker build -t "$DOCKER_USERNAME/$DOCKER_IMAGE_NAME:$DOCKER_TAG" .
if [ $? -ne 0 ]; then
  echo "Docker image build failed. Please check the Dockerfile and context."
  exit 1
fi

# Step 3: Push the Docker image to Docker Hub
echo "Pushing the Docker image to Docker Hub..."
docker push "$DOCKER_USERNAME/$DOCKER_IMAGE_NAME:$DOCKER_TAG"
if [ $? -ne 0 ]; then
  echo "Failed to push the Docker image to Docker Hub. Please try again."
  exit 1
fi

echo "Docker image pushed successfully to Docker Hub: $DOCKER_USERNAME/$DOCKER_IMAGE_NAME:$DOCKER_TAG"

# Step 4: Optional: Logout from Docker Hub
docker logout
