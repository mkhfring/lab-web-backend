# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory in the container
WORKDIR /app

RUN apt-get update && apt-get install -y libmagic1
# Copy requirements.txt to the docker image and install packages
COPY requirements-dev.txt /app/
COPY requirements-ci.txt /app/
RUN pip install --no-cache-dir -r requirements-dev.txt
RUN pip install --no-cache-dir -r requirements-ci.txt

# Copy the current directory contents into the container at /app
COPY . /app/
RUN pip install --no-cache-dir -e .

# Expose the Flask port (5000 by default)
EXPOSE 5001

ENV FLASK_APP=flasker:create_app

# Run gunicorn
CMD flask init_db && flask add_members && gunicorn -b :5001 server:gunicorn_app

