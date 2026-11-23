FROM python:3.11-slim

WORKDIR /app

# Listen on all interfaces so the published port reaches the service.
# config.py turns Flask debug mode off automatically when HOST is not loopback.
ENV HOST=0.0.0.0 PORT=5000 PYTHONUNBUFFERED=1

# CPU-only torch first (about 200 MB; nothing here trains). requirements.txt
# then sees torch already satisfied, so pip does not pull the 2-3 GB CUDA build.
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000
CMD ["python", "app.py"]
