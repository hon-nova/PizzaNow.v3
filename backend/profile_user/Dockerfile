FROM python:3.12-slim

WORKDIR /app

COPY profile_user/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    procps \
 && rm -rf /var/lib/apt/lists/*

COPY core ./core

COPY profile_user ./profile_user

ENV PORT=2025

CMD ["python", "-m", "profile_user.app.main"]