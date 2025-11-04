FROM python:3.11-slim

# Make sure we can see all output, even if pip fails
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libffi-dev \
    libssl-dev \
    python3-dev \
    curl \
    ca-certificates \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

# Force pip to show full debug output
RUN echo "===== Starting pip install =====" && \
    cat requirements.txt && \
    python -m pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -vvv -r requirements.txt || \
    (echo "❌ PIP INSTALL FAILED - showing environment and requirements" && \
     python -m pip --version && \
     cat requirements.txt && \
     exit 1)

COPY . .

CMD ["python", "app.py"]
