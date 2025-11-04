# Use a lightweight but complete Python image
FROM python:3.11-slim

# Install system dependencies required by gevent and Flask
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libffi-dev \
    libssl-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy requirements first to leverage caching
COPY requirements.txt .

# Upgrade pip and install dependencies
RUN python -m pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of the code
COPY . .

# Expose the Flask port
EXPOSE 8080

# Run the app
CMD ["python", "app.py"]
