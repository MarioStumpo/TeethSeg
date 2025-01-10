FROM python:3.9-slim

WORKDIR /

RUN apt update && apt install -y \
    libsm6 libxext6 libxrender-dev ffmpeg \
    build-essential cmake git

# Pre-install numpy and Cython
RUN pip install --no-cache-dir numpy Cython

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
