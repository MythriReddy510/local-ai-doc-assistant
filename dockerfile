# Use official Python 3.11 image as base
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Install system dependencies needed by some packages
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first
COPY requirements.txt .

# Upgrade pip first then install packages
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project
COPY . .

# Create uploads folder
RUN mkdir -p data/uploads

# Expose port 8000
EXPOSE 8000

# Start the FastAPI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]