FROM python:3-slim

# Set the working directory inside the Docker container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY ./requirements.txt .

# Install dependencies from requirements.txt
RUN pip install -r requirements.txt

# Copy the entire contents of the current directory into the container at /app
COPY . .

# Change directory to the location of main.py
WORKDIR /app

EXPOSE  8201

# Command to run your application using uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8201"]
