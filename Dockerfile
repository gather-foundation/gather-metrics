# Use the official Python image from the Docker Hub
FROM python:3.12-alpine

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the application source code
COPY ./src /app/src

# Copy the static and data directories from the root
COPY ./static /app/static
COPY ./data /app/data

# Set the command to run FastAPI with Uvicorn
CMD ["fastapi", "run", "src/main.py", "--port", "80"]
