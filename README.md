# Raspberry Pi Temperature Logger

Started on June 22, 2018 at 2:35 

## Requirements

	Raspberry Pi
	Temparature sensor
	
## Install
	
	git cline
	
	cd pilogger
	
	./install-pilogger.sh
	
## Usage

Browse the log at http://[IP]:5000

Grab the log using a file server

	afp://[IP]
	smb://[IP]

## Login and control the system

	ssh pi@[IP]
	# password is raspberry
	
## At the Raspberry Pi command prompt

	# return to screen session with
	screen -r
	
	# once in a screen session, detatch (d) from it and keep it running in background
	# ctrl+a then d
	
	# kill the screen session
	# ctrl+c
	
	# run a new instance
	screen
	cd ~/fridge_logger
	python fridge_logger.py
	
	# detatch from screen
	# ctrl+a d
	
### Make sure python code is not already running

	ps -aux | grep python

Will give you something like this (different number) if it is already running

	pi         489  0.5  1.3  16444 12672 pts/1    S+   15:39   0:02 python fridge_logger.py


## Install System on Pi

	touch /Volumes/boot/ssh
	
## Grab MAC address from router

Type this

	ifconfig eth0
	
And get something like this

	eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
			inet 192.168.1.82  netmask 255.255.255.0  broadcast 192.168.1.255
			inet6 fe80::809f:6fa0:372d:1a8e  prefixlen 64  scopeid 0x20<link>
			ether b8:27:eb:a0:68:1b  txqueuelen 1000  (Ethernet)
			RX packets 57132  bytes 71670863 (68.3 MiB)
			RX errors 0  dropped 0  overruns 0  frame 0
			TX packets 10845  bytes 1219455 (1.1 MiB)
			TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

Tells you, the mac address is 

	b8:27:eb:a0:68:1b
	
Tell Hopkins to allow it on the network

Go to following address and 'Register For a Fixed IP Address by Subnet' or maybe some other option?

https://jhars.nts.jhu.edu
 
Once form is filled out you will get emailed an IP address

## Login

	ssh pi@10.16.81.172
	# password is raspberry
	
## Update system

	sudo apt-get update  
	sudo apt-get upgrade 

## Networking

### AFP

	sudo apt-get install netatalk

	# stop netatalk
	sudo /etc/init.d/netatalk stop

	# edit config file
	sudo pico /etc/netatalk/AppleVolumes.default

	# change this one line

	# By default all users have access to their home directories.
	#~/                     "Home Directory"
	~/                      "the_name_you_want"

	# restart netatalk
	sudo /etc/init.d/netatalk start

### SMB

	sudo apt-get install samba samba-common-bin

Edit /etc/samba/smb.conf

	sudo pico /etc/samba/smb.conf

Add the following

	[share]
	Comment = Pi shared folder
	Path = /home/pi
	Browseable = yes
	Writeable = yes
	only guest = no
	create mask = 0777
	directory mask = 0777
	Public = yes
	Guest ok = no

Add a password

	sudo smbpasswd -a pi

Restart samba

	sudo /etc/init.d/samba restart

## Install some junk on system (for AdaFruit DHT driver?)

	sudo apt-get install python-pip


## Install ADAFruit DHT python library

See [DHT Humidity Sensing on Raspberry Pi](https://learn.adafruit.com/dht-humidity-sensing-on-raspberry-pi-with-gdocs-logging?view=all)

And see the [Adafruit_Python_DHT](https://github.com/adafruit/Adafruit_Python_DHT) GitHub repository.

	# install git
	sudo apt-get install git
	
	git clone https://github.com/adafruit/Adafruit_Python_DHT.git

	# not sure if these are neccessary
	cd Adafruit_Python_DHT
	sudo apt-get install build-essential python-dev python-openssl

	sudo python setup.py install
	
## Test it, assuming data pin is on GPIO 18

cd examples
sudo ./AdafruitDHT.py 2302 18

## Write some python code

## Send data to plotly

	# pip install plotly
	pip install plotly --upgrade
	
	
## To keep your program running after you logout of shell

	sudo apt-get install screen
	
	screen
	python testdht.py
	# axit screen with ctrl+a then d
	
