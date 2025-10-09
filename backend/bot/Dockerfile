FROM python:3.12-slim

WORKDIR /app

COPY bot/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    procps \
 && rm -rf /var/lib/apt/lists/*

COPY core ./core

COPY bot ./bot

ENV PORT=2025

CMD ["python", "-m", "bot.app.main"]