# Raspberry Pi Temperature Logger

## To do

There is a race condition when starting pilogger.service at boot

see: https://unix.stackexchange.com/questions/436666/run-service-after-ttyusb0-becomes-available

get rid of pilogger.service and make

file

/etc/udev/rules.d/99-serial-logger.rules

with 

SUBSYSTEM=="tty", ACTION=="add", KERNEL=="ttyUSB0", RUN+="/serial_script.sh"


or (did this and it works)

remove `WantedBy=default.target` from pilogger.service

and make file

/etc/udev/rules.d/99-serial-logger.rules

with

SUBSYSTEM=="tty", KERNEL=="ttyUSB0", TAG+="systemd", ENV{SYSTEMD_WANTS}+="your-serial-logger.service"


## Requirements

	Raspberry Pi
	Temperature sensor like an [AM2302](https://www.adafruit.com/product/393)
	
## Install
	
	git clone https://github.com/cudmore/pilogger.git
	
	cd pilogger
	
	./install-pilogger.sh
	
## Usage

Browse an up-to-date plot and table of temperature and humidity readings.

	http://[IP]:5000
	
Grab the log using a file server (make sure you install afp or smb)

	afp://[IP]
	smb://[IP]

## Login and control the system

	ssh pi@[IP]
	
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

