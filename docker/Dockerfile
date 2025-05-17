FROM python:3.12-slim

ARG DB_HOST
ARG DB_USER
ARG DB_PASS
ARG DB_NAME

ENV DB_HOST=$DB_HOST
ENV DB_USER=$DB_USER
ENV DB_PASS=$DB_PASS
ENV DB_NAME=$DB_NAME

RUN apt-get update && apt-get install -y \
    curl libpq-dev gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install uv

WORKDIR /app
COPY . /app
EXPOSE 8080
CMD ["uv", "run", "python", "run.py"]