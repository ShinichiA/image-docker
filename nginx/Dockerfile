FROM nginx:1.21-alpine

WORKDIR .

RUN rm /etc/nginx/conf.d/default.conf
COPY config/default.conf /etc/nginx/conf.d/
