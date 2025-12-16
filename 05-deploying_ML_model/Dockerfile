# Use a lightweight Python base image to reduce container size
# We will take this image and add things on top of it
FROM python:3.8.12-slim

# Install Pipenv because our project uses it for dependency management
RUN pip install --no-cache-dir pipenv

# Set the working directory inside the container and cd there
WORKDIR /app

# Copy dependency definitions Pipfiles to the current working directory
# In this case, it's /app inside the container
COPY ["Pipfile", "Pipfile.lock", "./"]

# Install project dependencies into the system environment
# If we just do pipenv install, it creates a virtualenv inside the container, but we don't need that since the container is already isolated
# --system --deploy installs packages globally (no virtualenv inside container)
RUN pipenv install --system --deploy

# Copy actual service code to the working directory inside the container
COPY ["predict.py", "churn_prediction_model_C=1.0.bin", "./"]

# Expose the port the application listens on
# We are telling Docker that we want this port to be open to the host machine when the container is running
EXPOSE 9696

# Start the production-grade WSGI server
# Gunicorn will serve the Flask app defined in predict.py
ENTRYPOINT ["gunicorn", "--bind=0.0.0.0:9696", "predict:app"]
