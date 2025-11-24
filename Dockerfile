# Multi-stage build for production
FROM node:20 AS frontend
WORKDIR /frontend

# Increase Node.js memory limit for Tailwind build
ENV NODE_OPTIONS="--max-old-space-size=4096"

# Copy frontend package files
COPY frontend/package*.json ./
RUN npm ci --only=production

# Copy frontend source and build
COPY frontend/ ./
RUN npm run build

# Production Python image
FROM python:3.11-slim

WORKDIR /app

# Copy built frontend assets
COPY --from=frontend /frontend/dist /app/staticfiles/css/

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

EXPOSE 8000

# Port mapping to localhost is configured at runtime. Example:
# docker run -p 127.0.0.1:8000:8000 <image-name>

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
