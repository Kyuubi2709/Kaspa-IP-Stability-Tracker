# Use a stable Python base image
FROM python:3.10

# Environment configuration
ENV PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    API_URL="https://api.runonflux.io/apps/location/kaspanodekat"  # ✅ default value

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libffi-dev \
    libssl-dev \
    python3-dev \
    curl \
    ca-certificates \
 && rm -rf /var/lib/apt/lists/*

# Create working directory
WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN echo "===== Installing Python dependencies =====" && \
    python -m pip install --upgrade pip setuptools wheel && \
    pip install -r requirements.txt

# Copy all project files
COPY . .

# Expose Flask port
EXPOSE 8080

# Start the Flask app
CMD ["python", "app.py"]
