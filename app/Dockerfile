# Use the official Python image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the application files into the container
COPY . /app

# Install necessary dependencies
RUN pip install --no-cache-dir flask mysql-connector-python

# Expose port 5000
EXPOSE 5000

# Command to run the application
CMD ["python", "index.py"]
