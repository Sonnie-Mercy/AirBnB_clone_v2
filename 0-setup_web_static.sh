#!/usr/bin/env bash
# Script to configure and start a web server for deploying web_static.

apt-get update
apt-get install -y nginx

# Create necessary directories and a basic index.html file
mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/
echo "Holberton School" > /data/web_static/releases/test/index.html
ln -sf /data/web_static/releases/test/ /data/web_static/current

# Set ownership and group for web server directories
chown -R ubuntu /data/
chgrp -R ubuntu /data/

# Configure Nginx with a custom server block
printf %s "server {
listen 80 default_server;
listen [::]:80 default_server;
add_header X-Served-By $HOSTNAME;
root   /var/www/html;
index  index.html index.htm;
location /hbnb_static {
alias /data/web_static/current;
index index.html index.htm;}
location /redirect_me {
return 301 http://cuberule.com/;}
error_page 404 /404.html;
location /404 {
root /var/www/html;
internal;}
}" > /etc/nginx/sites-available/default
# Restart Nginx to apply the configuration changes
service nginx restart
