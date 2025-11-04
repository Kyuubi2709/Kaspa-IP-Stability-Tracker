# Use Python 3.11 slim base for smaller image but full package compatibility
FROM python:3.10

# Avoid Python buffering output and ensure pip behaves consistently
ENV PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

# Install essential build tools and libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libffi-dev \
    libssl-dev \
    python3-dev \
    curl \
    ca-certificates \
 && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Copy only requirements first (to leverage Docker layer caching)
COPY requirements.txt .

# Upgrade pip/setuptools/wheel and install Python dependencies with verbose logging
RUN echo "===== Starting pip install =====" && \
    python -m pip install --upgrade pip setuptools wheel && \
    echo "===== Installing requirements =====" && \
    cat requirements.txt && \
    pip install -vvv -r requirements.txt

# Copy remaining project files
COPY . .

# Expose Flask port
EXPOSE 8080

# Default command to start the Flask app
CMD ["python", "app.py"]
