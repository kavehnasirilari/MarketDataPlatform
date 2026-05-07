# Base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy dependencies file
COPY syncer_service/requirements.txt ./requirements.txt

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy required project modules
COPY syncer_service ./syncer_service
COPY database ./database
COPY core ./core

# Default command
CMD ["python", "-m", "syncer_service.syncer.run_base_sync"]