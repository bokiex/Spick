# Use the official Python image from the Docker Hub
FROM python:3-slim

# Set the working directory in the container
WORKDIR /app

COPY requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN python -m pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY ./app .

# Make port available to the world outside this container
EXPOSE 8008

# Define our command to be run when launching the container
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8008", "--reload"]
