# Use a full Python image for simplicity
FROM python:3.11

# Set working directory
WORKDIR /app

# Copy only requirements.txt first
COPY requirements.txt .

# Upgrade pip and install dependencies
RUN python -m pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project
COPY . .

# Expose Flask default port
EXPOSE 8080

# Run the app
CMD ["python", "app.py"]
