# 1. Base Python image use karein
FROM python:3.13-slim

# 2. System dependencies install karein (Required for building wheels like psycopg2)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 3. Working directory set karein
WORKDIR /code

# 4. Requirements copy karke optimize installation karein
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /code/requirements.txt

# 5. Baaki saara project code copy karein
COPY . /code

# 6. Entrypoint script ko executable banayein
RUN chmod +x /code/entrypoint.sh

# 7. Port 8000 expose karein (Sirf web app ke liye kaam aayega)
EXPOSE 8000

# 8. Script ko main entrypoint set karein
ENTRYPOINT ["/code/entrypoint.sh"]

# Default command agar docker-compose override na kare
CMD ["web"]

