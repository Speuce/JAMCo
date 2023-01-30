FROM node:19-alpine3.17
RUN mkdir /frontend
COPY . /frontend
WORKDIR /frontend
EXPOSE 3000

RUN npm install -g npm
ENTRYPOINT [ "sh", "docker-entrypoint.sh" ]