FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies (needed for compiling some python packages)
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY backend/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend code to the container
COPY backend/ /app/

# Run the FastAPI server. Render uses the $PORT environment variable.
CMD uvicorn app:app --host 0.0.0.0 --port ${PORT:-8000}
