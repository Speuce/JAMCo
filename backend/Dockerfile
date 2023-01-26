FROM python:3.11-alpine3.17
# TODO remove from production
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apk add alpine-sdk build-base

RUN mkdir /backend
COPY requirements.txt /backend/
WORKDIR /backend
RUN pip install -r requirements.txt
EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
