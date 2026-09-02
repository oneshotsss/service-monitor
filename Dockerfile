FROM python:3.11-slim

WORKDIR /app

# system deps for psycopg if needed
RUN apt-get update && apt-get install -y gcc libpq-dev build-essential --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
