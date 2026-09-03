FROM python:3.12-slim

# Tesseract OCR and language data for English, Hindi and Marathi.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        tesseract-ocr \
        tesseract-ocr-hin \
        tesseract-ocr-mar \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies first so Docker can reuse this layer.
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1

# Render supplies PORT at runtime.
CMD ["sh", "-c", "gunicorn -w 1 -b 0.0.0.0:${PORT:-10000} pdf_crop_worker:app"]
