# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Expose port (Render will override this, but it's good practice)
EXPOSE 8000

# Command to run the application using sh to ensure PORT is expanded correctly
CMD sh -c "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"
