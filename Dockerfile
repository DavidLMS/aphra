# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the necessary files to install dependencies
COPY requirements.txt ./
COPY setup.py ./
COPY config.toml ./config.toml

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Ensure the entry script has execution permissions
RUN chmod +x /app/entrypoint.sh

# Set the default entry point for the container
ENTRYPOINT ["./entrypoint.sh"]