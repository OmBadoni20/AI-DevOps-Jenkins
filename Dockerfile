FROM python:3.11-slim

WORKDIR /app

# Copy dependency file first for better Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Create a dedicated non-root user and group
RUN groupadd --system appuser && \
    useradd --system --no-create-home --gid appuser appuser && \
    chown -R appuser:appuser /app

# Run application as non-root user
USER appuser

EXPOSE 5000

CMD ["python", "app.py"]