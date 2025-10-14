FROM python:3.12-slim

WORKDIR /app

COPY paypal/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    procps \
 && rm -rf /var/lib/apt/lists/*

COPY core ./core

COPY paypal ./paypal

# Remove any accidentally copied .env files
RUN find . -type f -name ".env*" -delete

ENV PORT=2025

CMD ["python", "-m", "paypal.app.main"]