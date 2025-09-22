# Base image
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# RUN apt-get update && apt-get install -y \
#     build-essential \
#     libpq-dev \
#     && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app/ 

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000
