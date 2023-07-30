# Use an official Python runtime as a parent image
FROM python:3.11.4

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory files (i.e., the app) to the Docker container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Define environment variable
ENV NAME email-autodrafts

# Run main.py when the container launches
CMD ["python", "main.py"]
