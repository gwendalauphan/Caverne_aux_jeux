FROM python:3.12-slim

RUN apt update && apt install -y \
    tk \
    libtk8.6 \
    make \
    binutils

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY Makefile .

#Copier le repertoire app
WORKDIR /app
COPY app .
