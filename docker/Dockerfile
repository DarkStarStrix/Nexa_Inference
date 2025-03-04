# docker/Dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ app/

# Set environment variables
ENV PYTHONPATH=/app
ENV PORT=8080

# Run the application
CMD ["python", "-m", "app.main"]