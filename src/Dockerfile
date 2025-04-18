# Use a more feature-rich base image that includes common tools like curl, nc, dig, etc.
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Install required tools and Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    netcat \
    dnsutils \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application with proper lifespan handling
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--lifespan", "on"]