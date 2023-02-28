#   Build the frontend to static files
FROM node:19-alpine3.17 as frontend
COPY ./frontend ./frontend
WORKDIR /frontend
RUN npm install -g npm
RUN npm install
RUN npx vite build

# build the backend (actually used in production)
FROM python:3.11-alpine3.17
# TODO remove
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apk add alpine-sdk build-base
COPY ./backend ./backend
COPY --from=frontend /frontend/dist ./backend/global_static/dist
WORKDIR /backend
RUN pip install -r requirements.txt
RUN python manage.py collectstatic --noinput
EXPOSE 8000

ENTRYPOINT [ "sh", "./docker-entrypoint.sh" ]
