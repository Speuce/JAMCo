FROM python:3.11-alpine3.17
# TODO remove from production
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apk add alpine-sdk build-base

# gcc required for python cryptography package
RUN apk add gcc musl-dev python3-dev libffi-dev openssl-dev

RUN mkdir /backend
COPY requirements.txt /backend/
WORKDIR /backend
RUN pip install -r requirements.txt
EXPOSE 8000

ENTRYPOINT [ "sh", "docker-entrypoint.sh" ]
