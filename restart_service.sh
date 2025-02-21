#!/bin/bash

echo "Pulling latest code from Git..."
git pull

if [ $? -ne 0 ]; then
    echo "Git pull failed! Check your repo status."
    exit 1
fi

echo "Restarting Gunicorn..."
sudo systemctl restart gunicorn

echo "Checking Gunicorn Status..."
sudo systemctl status gunicorn --no-pager --lines=5

echo "Restarting Nginx..."
sudo systemctl restart nginx

echo "Checking Nginx Status..."
sudo systemctl status nginx --no-pager --lines=5

echo "Services restarted successfully!"
