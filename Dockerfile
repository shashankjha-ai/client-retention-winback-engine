# Use Python 3.11 slim image
FROM python:3.11-slim

# Set container working directory
WORKDIR /app

# Copy dependency manifest
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source and tests
COPY src/ ./src/
COPY tests/ ./tests/

# Set default command to run pytest suite
CMD ["pytest", "tests/"]
