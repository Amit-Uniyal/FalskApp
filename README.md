# FalskApp
Flask + MySQL +Swagger - CURD operations

# Install and configure MySQL server
sudo apt-get install mysql-server
sudo apt-get install libmysqlclient-dev 

# login to mysql server
mysql -u root -p

# Create database user
GRANT ALL PRIVILEGES ON *.* TO 'flaskuser'@'localhost' IDENTIFIED BY 'flaskpass';


# login to mysql server by new user
mysql -u flaskuser -p

# create database
CREATE DATABASE flaskapp;

# create table
CREATE TABLE users ( id int PRIMARY KEY AUTO_INCREMENT, username varchar(20) NOT NULL, firstname varchar(20) NOT NULL, lastname varchar(20));

# Configure nginx server
sudo apt-get install  nginx

# remove default and add new nginx configuration
rm /etc/nginx/sites-enabled/default

vim /etc/nginx/sites-avaiable/flask_app

server {
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

sudo ln -s /etc/nginx/sites-avaiable/flask_app /etc/nginx/sites-enabled/flask_app

sudo service nginx restart

# Create new virualenv, install python dependencies inside virtualenv
pip install -r requirements.txt


# start server
gunicorn server:app --bind 0.0.0.0 -D

# navigate to links
elinks://http:(ip addr):8000/apidocs
