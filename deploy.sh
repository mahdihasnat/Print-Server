PIPCMD="pip"
PYTHONCMD="python3"
# set -x # prints commands as they are executed

# dependencies for printserver
$PIPCMD install -r requirements.txt

# make migrations
$PYTHONCMD printserver/manage.py makemigrations users prints
$PYTHONCMD printserver/manage.py migrate

# Collect static
$PYTHONCMD printserver/manage.py collectstatic

# Add user to database
$PYTHONCMD printserver/manage.py shell < printserver/add_user_script.py

# install nginx
sudo apt install nginx-full

# Write config file for nginx
current_dir=$(pwd)
echo "current_dir: $current_dir"
nginx_config="server {
	listen 8001;
	location /collectedstatic/ {
		root $current_dir/printserver/;
	}
	add_header Access-Control-Allow-Origin *;
}"
nginx_config_file="/etc/nginx/conf.d/pstatic.conf"
touch $nginx_config_file
chmod +w $nginx_config_file
echo $nginx_config > $nginx_config_file

# Restart nginx
nginx -s reload

# test nginx
x=$(curl -X GET http://localhost:8001/collectedstatic/js/all.js)
if [ -z "$x" ]; then
	echo "nginx not working"
	exit 1
fi

echo "Chanage static_url in /printserver/printserver/settings.py to http://IP_FOR_STATICSERVER:8001/collectedstatic/"

# Run server
$PYTHONCMD printserver/manage.py runserver


