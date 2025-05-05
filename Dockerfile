# Use the official Python base image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all source files, including .env
COPY . .

# Set environment variable for Flask
ENV PORT=8080

# Expose the port Flask runs on
EXPOSE 8080

COPY . .

# Start the Flask app
CMD ["python", "app.py"]


