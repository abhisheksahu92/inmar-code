# Use the official Python image from the Docker Hub
FROM ubuntu
FROM python:latest

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Update aptitude with new repo
RUN apt-get update

# Install software
RUN apt-get install -y git

# Make a new directory to put our code in.
RUN mkdir /src

# Set the working directory in the container
WORKDIR /src

# Copy the requirements file into the container
COPY . /src

# Install dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy the entire project into the container
COPY . /src/

# Run database migrations and upload data
RUN python manage.py migrate && \
    python manage.py upload_data && \
    python manage.py test


