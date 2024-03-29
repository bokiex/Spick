# Use the official Python image from the Docker Hub
FROM python:3-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app

RUN apt-get update && \
    apt-get install -y pkg-config libmariadb-dev-compat libmariadb-dev gcc default-libmysqlclient-dev && \
    rm -rf /var/lib/apt/lists/*


COPY requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN python -m pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY ./app .

# Make port 8007 available to the world outside this container
EXPOSE 8007

# Define our command to be run when launching the container
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8007", "--reload"]
