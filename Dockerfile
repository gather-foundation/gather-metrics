# Use the official Python image from the Docker Hub
FROM python:3.12-alpine

# Set the working directory in the container
WORKDIR /code

# Copy the requirements file and install dependencies
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the application source code
COPY ./src /code/app

# Copy the static and data directories from the root
COPY ./static /code/app/static
COPY ./data /code/app/data

# Set the command to run FastAPI with Uvicorn
CMD ["fastapi", "run", "app/main.py", "--port", "80"]
