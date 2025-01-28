# Use official Python image as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy all the application files into the container
COPY . /app

# Install the required Python packages
RUN pip install --no-cache-dir flask mysql-connector-python

# Expose the port the app will run on
EXPOSE 5000

# Run the Flask app when the container starts
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]