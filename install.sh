#!/bin/bash

sudo apt install python3
sudo apt install python3-pip
sudo apt install default-libmysqlclient-dev
pip3 install flask --user
pip3 install flask-jwt-extended
pip3 install -U Flask-SQLAlchemy
pip3 install -U mysqlclient