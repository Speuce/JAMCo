FROM python:3.11-alpine3.17
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apk add alpine-sdk build-base

RUN mkdir /app
COPY backend/requirements.txt /app/
RUN pip install -r app/requirements.txt
COPY . /app
WORKDIR /app
EXPOSE 8000
#RUN python backend/manage.py migrate
CMD ["python", "backend/manage.py", "runserver", "0.0.0.0:8000"]
#ENTRYPOINT ["tail", "-f", "/dev/null"]
