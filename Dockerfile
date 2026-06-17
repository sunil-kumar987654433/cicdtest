# 1. Base Python image
FROM python:3.13-slim

# 2. System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc python3-dev libpq-dev && rm -rf /var/lib/apt/lists/*

# 3. FIX: Working directory ko /app kiya
WORKDIR /app

# 4. Requirements copy aur install
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /app/requirements.txt

# 5. FIX: Saara project code /app me copy kiya
COPY . /app

# 6. Entrypoint permissions
RUN chmod +x /app/entrypoint.sh

EXPOSE 8000
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["web"]
