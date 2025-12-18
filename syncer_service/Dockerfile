# Base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install required system libs
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy dependencies
COPY requirements.txt .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy project code
COPY . .

# Default command (can be modified later)
CMD ["python", "syncer/main.py"]
