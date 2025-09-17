# Use Python 3.11 base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies (including Tesseract-OCR)
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . /app

# Copy locally downloaded Python dependencies
COPY wheelhouse /app/wheelhouse

# Install dependencies from wheelhouse (if available)
RUN pip install --no-index --find-links=/app/wheelhouse -r requirements.txt

# Install the package
RUN pip install .

# Expose FastAPI default port
EXPOSE 9001

# Start the FastAPI server
CMD ["realtime_va"]

# # -------- Stage 1: Builder --------
# FROM python:3.11-slim AS builder

# WORKDIR /app

# # Install build dependencies
# RUN apt-get update && apt-get install -y \
#     build-essential \
#     libgl1 \
#     libglib2.0-0 \
#     && rm -rf /var/lib/apt/lists/*

# # Install from wheelhouse or requirements.txt
# COPY wheelhouse /app/wheelhouse
# COPY requirements.txt .
# RUN pip install --no-index --find-links=wheelhouse -r requirements.txt

# # Copy source and install the app
# COPY . .
# RUN pip install .

# # -------- Stage 2: Final minimal image --------
# FROM python:3.11-slim

# WORKDIR /app

# # Runtime dependencies only
# RUN apt-get update && apt-get install -y \
#     libgl1 \
#     libglib2.0-0 \
#     && rm -rf /var/lib/apt/lists/*

# # Copy only installed packages from builder stage
# COPY --from=builder /usr/local /usr/local

# # Copy app code if needed at runtime
# COPY --from=builder /app /app

# EXPOSE 9001

# CMD ["realtime_va"]
