# Use an official Python runtime as a parent image
FROM python:3.12-slim as iati-test-dev

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . /usr/src/app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements/dev.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run the application
CMD [ "gunicorn", "-c", "./build/dev/gunicorn.py", "config.wsgi:application", "--reload" ]
