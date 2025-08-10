FROM python:3.12-slim

RUN apt update && apt install -y \
    tk \
    libtk8.6

COPY requirements.txt .
RUN pip install -r requirements.txt

#Copier le repertoire app
WORKDIR /app
COPY app .
