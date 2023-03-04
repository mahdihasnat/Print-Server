# Collect Static from printserver
- `python manage.py collectstatic`

# Static File server by nginx
- install nginx: `sudo apt install nginx-full`
- go to nginx config dir: `cd /etc/nginx/conf.d`
- create new config file: `sudo touch pstatic.conf`
- add write permission: `sudo chmod +w pstatic.conf`
- edit config file: `sudo gedit pstatic.conf`
- save following template with changing root dir
```
server {
	listen 8001;
	location /collectedstatic/ {
# change next line to your project dir 
		root /home/user/..../printserver/;
	}
	add_header Access-Control-Allow-Origin *;
}
```
- restart nginx: `sudo nginx -s reload`
- test: `curl -X GET http://localhost:8001/collectedstatic/js/all.js`

# Settings in printserver
- In `settings.py` add 
```
STATIC_URL = 'http://127.0.0.1:8001/collectedstatic/'
```
