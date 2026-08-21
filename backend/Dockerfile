FROM python:3.12-slim

WORKDIR /app

# Install system dependencies (for better compatibility)
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Create non-root user
RUN useradd --create-home --uid 1000 appuser
USER appuser

# Default command
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]