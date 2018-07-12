# Raspberry Pi Temperature Logger

## Requirements

 - A functioning Raspberry Pi. See our [install instructions][install-stretch]
 - Either a Teensy microcontroller with an analog temperature sensor
 - And/Or a temperature and humidity sensor like the [AM2302](https://www.adafruit.com/product/393)

## Download and install pilogger server
	
```
# update your system if neccessary
sudo apt-get update
sudo apt-get upgrade

# install git if neccessary
sudo apt-get install git
	
git clone https://github.com/cudmore/pilogger.git
	
cd pilogger
./install-pilogger
```

## Install platformio and upload code to a microcontroller

In order to use a microcontroller, it first has to be programmed. To program a microcontroller connected via USB to a Pi, we use [platformio][platformio]. See our [platformio install instructions](platformio).
	
## Usage

### Start and stop the pilogger server

```
./pilogger start	- Run the pilogger server in the background
./pilogger stop		- Stop the background pilogger server
./pilogger run		- Run the pilogger on the command line (useful for debugging)
```

To see the output of the pilogger server on the command line, use `./pilogger run`.

### Browse real-time plots and tables of temperature and humidity

	http://[IP]:5000
	
### Grab the log file using a file-server

Grab the log file from the Raspberry Pi as a file-server. This requires either Apple-File-Protocol and/or Samba to be installed. For help with this, see below.

	afp://[IP]
	smb://[IP]

## The Raspberry Pi As a File Server

### Apple-File-Protocol (AFP)

Apple-File-Protocol allows a Raspberry Pi to be mounted from a macOS computer.

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

### Samba (SMB)

Samba is a protocol that allows a Raspberry Pi to be mounted from either a Windows or macOS computer.


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

## Troubleshooting

### Obtaining a fixed IP address

On corporate and/or university networks, you need to tell your network administrators the MAC address of your Pi and they can (usually) issue you a fixed IP address. You want a fixed IP address so you can reliably find the Pi with one IP.

```
# Type this
ifconfig eth0

# And get something like this
eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
		inet 192.168.1.82  netmask 255.255.255.0  broadcast 192.168.1.255
		inet6 fe80::809f:6fa0:372d:1a8e  prefixlen 64  scopeid 0x20<link>
		ether b8:27:eb:a0:68:1b  txqueuelen 1000  (Ethernet)
		RX packets 57132  bytes 71670863 (68.3 MiB)
		RX errors 0  dropped 0  overruns 0  frame 0
		TX packets 10845  bytes 1219455 (1.1 MiB)
		TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
```

This tells you, the mac address is  `b8:27:eb:a0:68:1b`.

### OSError: [Errno 98] Address already in use

You can't run the background server and the debug/run server at the same time. Try `./pilogger stop` and then `./pilogger run` again.

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



[install-stretch]: http://blog.cudmore.io/post/2017/11/22/raspian-stretch/
[platformio]: https://platformio.org/
