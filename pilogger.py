# Robert Cudmore
# 20180628

import sys, os, time, socket
from datetime import datetime

import Adafruit_DHT

"""
import plotly
import plotly.plotly as py
from plotly.graph_objs import *
"""

# (Adafruit_DHT.DHT11, Adafruit_DHT.DHT22, Adafruit_DHT.AM2302)
sensor = Adafruit_DHT.AM2302 
pin = 3
intervalSeconds = 60 # seconds


"""
plotly.tools.set_credentials_file(username='cudmore', api_key='F9pRWozfv0eiHkARvr4S')
"""

def test():

	humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
	
	if humidity is not None and temperature is not None:
		print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
	else:
		print('Failed to get reading. Try again!')
	

def runpilogger(sensor=Adafruit_DHT.AM2302 , pin=3, interval=60):
	savePath = '/home/pi/pilogger/log/pilogger.log'

	# save to this file
	"""
	# make directory if necc.
	if not os.path.exists(savePath):
		os.makedirs(savePath)
	"""

	hostname = socket.gethostname()
	
	# make file with header if necc.
	if not os.path.isfile(savePath):
		with open(savePath, 'a') as f:
			headerLine = 'Hostname,Date,Time,Seconds,Temperature,Humidity' + '\n'
			f.write(headerLine)
			
	# initialize
	lastTimeSeconds = 0

	#
	# set up an empty plot plot called 'room_control'
	"""
	trace0 = Scatter(x=[],y=[])
	trace1 = Scatter(x=[],y=[])
	data = [trace0, trace1]
	py.plot(data, filename = 'room_control')
	"""
	
	while True:
	
		# todo: merge nowSeconds and datetime_now (we are sampling time twice)
		nowSeconds = time.time() # epoch in seconds since January 1 1970

		datetime_now = datetime.now()
		theDate = datetime_now.strftime('%Y-%m-%d')
		theTime = datetime_now.strftime('%H:%M:%S')
		
		if nowSeconds > (lastTimeSeconds + intervalSeconds):
		
			print('reading')
			
			humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
			
			if humidity is not None and temperature is not None:
				humidity = round(humidity,2)
				temperature = round(temperature,2)
				#print(theDate, theTime, temperature, humidity)
				
				#
				# append to plotly
				"""
				new_data = Scatter(x=[datetime_now], y=[temperature] )
				data = Data( [ new_data ] )
				
				trace0 = Scatter(x=[datetime_now],y=[temperature])
				trace1 = Scatter(x=[datetime_now],y=[humidity])
				data = [trace0, trace1]
				plot_url = py.plot(data, filename='room_control', fileopt='extend')
				"""
				
			else:
				humidity = ''
				temperature = ''
				print('Failed to get reading. Try again!')

			# even when we fail
			lastTimeSeconds = nowSeconds
		
			oneLine = hostname + ',' + theDate + ',' + theTime + ',' + str(nowSeconds) + "," + str(temperature) + "," + str(humidity) + "\n"
			print(oneLine)
						
			with open(savePath, 'a') as f:
				f.write(oneLine)
		
		time.sleep(1) # just so this code does not hang the system
		
if __name__ == '__main__':
	runpilogger()
	
