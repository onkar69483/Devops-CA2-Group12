# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose port Django will run on
EXPOSE 8000

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run migrations (optional)
# RUN python manage.py migrate

# Start Django server
CMD ["gunicorn", "wealthwise.wsgi:application", "--bind", "0.0.0.0:8000"]
