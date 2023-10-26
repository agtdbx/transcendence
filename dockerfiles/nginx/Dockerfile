# Choose the os of container
FROM alpine:3.17

# Make updates and install needed pakages
RUN apk update && apk upgrade && apk add nginx openssl
RUN rm -f /var/cache/apk/*

# Create folders
RUN mkdir -p /var/www/html

# Copy conf
COPY nginx.conf /etc/nginx/http.d/nginx.conf
RUN rm -f /etc/nginx/http.d/default.conf

# Execute nginx command at run after the image build
CMD nginx -g "daemon off;"
