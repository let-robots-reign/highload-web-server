# highload-web-server

## How To Run
Python Web Server:
```
sudo docker build -t webserver . && sudo docker run -p 80:3000 webserver
```

Nginx:
```
cp -r http-test-suite/httptest nginx
sudo docker build -t webserver:nginx ./nginx && sudo docker run -p 80:3000 webserver:nginx
```