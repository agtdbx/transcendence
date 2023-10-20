FROM alpine:3.18

RUN apk update && apk upgrade && apk add npm
RUN rm -f /var/cache/apk/*

WORKDIR /src

RUN npm install || echo 'requirement already install'
RUN npm install --global nx@latest

CMD nx run frontend:serve --host=0.0.0.0 --port=4200
