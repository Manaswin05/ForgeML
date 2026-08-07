FROM python:3.10-slim AS backend

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY backend/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ /app/

# ============================================
# Frontend build stage
# ============================================
FROM node:20-alpine AS frontend-build

WORKDIR /app/frontend

# Copy frontend package files
COPY frontend/package*.json ./

# Install frontend dependencies
RUN npm ci

# Copy frontend source code
COPY frontend/ ./

# Build frontend
RUN npm run build

# ============================================
# Final stage
# ============================================
FROM backend

# Create directories for static files
RUN mkdir -p /app/static

# Copy built frontend from frontend-build stage
COPY --from=frontend-build /app/frontend/dist /app/static

# Install additional python packages for static file serving
RUN pip install aiofiles

# Update app.py to serve static files
# Run the FastAPI server. Render uses the $PORT environment variable.
CMD uvicorn app:app --host 0.0.0.0 --port ${PORT:-8000}