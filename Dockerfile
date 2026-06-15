# 1. Base Python image use karein
FROM python:3.11-slim

# 2. Working directory set karein
WORKDIR /code

# 3. Pehle requirements copy karein (Docker caching optimize karne ke liye)
COPY ./requirements.txt /code/requirements.txt

# 4. Dependencies install karein
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /code/requirements.txt

# 5. Baaki saara project code copy karein
COPY . /code

# 6. Port 8000 expose karein
EXPOSE 8000

# 7. FastAPI app run karne ki command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
