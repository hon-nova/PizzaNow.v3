FROM python:3.12-slim

WORKDIR /app

COPY bot/requirements.txt .

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    procps \
    build-essential \
 && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

COPY core ./core

COPY bot ./bot

ENV PORT=2025

CMD ["python", "-m", "bot.app.main"]