FROM nginx
MAINTAINER Zotov Alexey

COPY nginx.conf /etc/nginx/nginx.conf

WORKDIR /etc/nginx

COPY  ./httptest /etc/nginx/static/httptest

EXPOSE 3000
