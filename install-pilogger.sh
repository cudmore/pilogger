#!/bin/bash

# Author: Robert H Cudmore
# Date: 20180603
# Purpose: Bash script to install pilogger
#	1) create a python3 virtual environment
#	2) install pilogger/requirements.txt
#	3) install a systemctl service pilogger.service
#
# Usage:
#	./install-pilogger.sh
#
# Once this is all done, pilogger server can be used as follows
#	cd homecage/pilogger
#	./pilogger start
#	./pilogger stop
#	./pilogger restart
#	./pilogger status
#	./pilogger enable		# start homecage server at boot
#	./pilogger disable		# do not start homecage server at boot

if [ $(id -u) = 0 ]; then
   echo "Do not run with sudo. Try again without sudo"
   exit 1
fi

ip=`hostname -I | xargs`

#if systemctl is-active --quiet pilogger.service; then
#	echo 'service is active'
#fi

sudo systemctl stop pilogger.service

#################
# pip and virtualenv (system wide) 
#################
if ! type "pip" > /dev/null; then
	echo '==='
	echo "=== Installing pip"
	echo '==='
	sudo apt-get -y install python-pip
fi

if ! type "virtualenv" > /dev/null; then
	echo '==='
	echo "=== Installing virtualenv"
	echo '==='
	sudo /usr/bin/easy_install virtualenv
fi

if [ ! -d "env/" ]; then
	echo '==='
	echo "=== Making Python 3 virtual environment in $PWD/env"
	echo '==='
	mkdir env
	virtualenv -p python3 --no-site-packages env
fi

source env/bin/activate

echo ' '
echo '==='
echo '=== Installing pilogger Python requirements with pip'
echo '==='
pip install -r requirements.txt

deactivate


#################
# service 
#################
echo ' '
echo '==='
echo '=== Configuring systemctl in /etc/systemd/system/pilogger.service'
echo '==='
sudo cp bin/pilogger.service /etc/systemd/system/pilogger.service
sudo chmod 664 /etc/systemd/system/pilogger.service
sudo systemctl daemon-reload
#sudo systemctl start pilogger.service
sudo systemctl enable pilogger.service
#sudo systemctl status pilogger.service



#################
# DHT
#################
echo ' '
echo '==='
echo '=== Installing Adafruit Python DHT'
echo '==='

sudo apt-get install python3-dev

source env/bin/activate

cd

if [ -d "Adafruit_Python_DHT" ]; then
  rm -Rf Adafruit_Python_DHT
fi

git clone https://github.com/adafruit/Adafruit_Python_DHT.git

cd Adafruit_Python_DHT

python setup.py install

deactivate

echo ' '
echo 'Done installing pilogger server. The pilogger server will run at boot.'
echo 'To use the server, point your browser to:'
echo "    http://$ip:5000"

