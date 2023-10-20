from alpine:3.18

RUN apk update && apk upgrade && apk add npm
RUN rm -f /var/cache/apk/*

RUN npm install || echo 'noting to setup'

RUN npm install --global nx@latest

WORKDIR /src

CMD nx run frontend:serve --host=0.0.0.0 --port=4200
