FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port (Railway auto-detects)
EXPOSE 8080

# Run bot (your existing agent.py)
CMD ["python", "agent.py"]
