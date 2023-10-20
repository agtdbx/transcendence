from alpine:3.18

RUN apk update && apk upgrade && apk add npm
RUN rm -f /var/cache/apk/*

RUN npm install node 2>/dev/null || echo node already install
RUN npm install bootstrap  2>/dev/null || echo bootstrap already install

# CMD sleep 500

RUN npm install --global nx@latest

WORKDIR /src

CMD nx run frontend:serve --host=0.0.0.0 --port=4200
