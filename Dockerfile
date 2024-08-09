# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /workspace

# Copy the necessary files to install dependencies
COPY requirements.txt ./
COPY setup.py ./
COPY config.toml ./config.toml

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Ensure the entry script has execution permissions
RUN chmod +x /workspace/entrypoint.sh

# Set the entrypoint to the script and pass any arguments
ENTRYPOINT ["/workspace/entrypoint.sh"]
