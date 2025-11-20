# Dockerfile
FROM python:3.14-slim

WORKDIR /app

# Copy requirements and app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code and model
COPY app.py /app/
COPY savedmodel.pth /app/

EXPOSE 5000

# Run with gunicorn for production-ish usage
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app", "--workers=2"]
