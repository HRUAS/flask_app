# Step 1: Use an official Python runtime as a parent image
FROM python:3.9-slim

# Step 2: Set the working directory inside the container
WORKDIR /app

# Step 3: Copy the current directory contents into the container at /app
COPY . /app

# Step 4: Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Install dependencies for log rotation (if using logrotate)
RUN apt-get update && apt-get install -y logrotate

# Step 6: Create a directory for logs and set permissions
RUN mkdir -p /app/logs && chmod 777 /app/logs

# Step 7: Expose port 5000 to allow outside access
EXPOSE 5000

# Step 8: Define environment variable to specify Flask app
ENV FLASK_APP=app.py

# Step 9: Set up a volume for the log directory to persist logs outside the container
VOLUME /app/logs

# Step 10: Run the Flask app when the container starts
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
