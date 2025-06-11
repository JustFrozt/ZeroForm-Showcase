# temp_code_mvp/Dockerfile

# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Prevent python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE 1
# Ensure python output is sent straight to the terminal
ENV PYTHONUNBUFFERED 1

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Define the command to run the application using a production server (Gunicorn)
CMD ["gunicorn", "--workers", "4", "--bind", "0.0.0.0:8000", "app:create_app()"]
