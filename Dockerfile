# Use an official lightweight Python image as the base
FROM python:3.11-slim

# Set environment variables to prevent Python from generating .pyc files and buffering stdout and stderr
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code into the container
COPY . .

# Expose the port your app runs on
EXPOSE 8000

# Define the command to run your application
# Note: Railway and other platforms might override the CMD to use a specific port
CMD ["gunicorn", "main:server", "-b", "0.0.0.0:8000"]
