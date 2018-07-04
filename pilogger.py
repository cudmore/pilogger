"""
Author: Robert Cudmore
Date: 20180628

Purpose: Read sensor data either from a sensor attached to Pi (e.g. DHT sensor)
	or, read sensor data from a sensor attached to an arduino (via serial)
	
To do: Implement reading from multiple sensors.
	This will require adding column 'sensorID' to output file and
	tweeking the javascript to correctly parse this new data
	
"""

import sys, os, time, socket
import threading, queue, serial
from datetime import datetime

import Adafruit_DHT

# (Adafruit_DHT.DHT11, Adafruit_DHT.DHT22, Adafruit_DHT.AM2302)
sensor = Adafruit_DHT.AM2302 
pin = 3
intervalSeconds = 60 # seconds

# serial port connected to Arduino
port = '/dev/ttyACM0'
baud = 115200

# this is used by pilogger_app web interface, do not change
savePath = '/home/pi/pilogger/log/pilogger.log'

#########################################################################
class SerialThread(threading.Thread):
	"""
	A background thread to continuously monitor incoming serial data
	"""
	def __init__(self, inSerialQueue, outSerialQueue, errorSerialQueue, port='/dev/ttyACM0', baud=115200):
		threading.Thread.__init__(self)
		self.inSerialQueue = inSerialQueue
		self.outSerialQueue = outSerialQueue
		self.errorSerialQueue = errorSerialQueue
		
		try:
			# there is no corresponding self.mySerial.close() ???
			self.mySerial = serial.Serial(port, baud, timeout=0.5)
		except (serial.SerialException) as e:
			print('SERIAL ERROR: ', str(e))
			errorSerialQueue.put(str(e))
		except:
			print('SERIAL ERROR')
			raise

	def run(self):
		while True:
			#
			# as we receive serial input from arduino, put it in the outSerialQueue
			# this serial input is usually (float) temperature readings
			result = self.mySerial.readline()
			if result is not None:
				#print(result.decode())
				self.outSerialQueue.put(result.decode())
			
			#
			# process serial commands issued by parent in self.inSerialQueue
			# and send them out the serial port
			"""
			try:
				serialCommand = self.inSerialQueue.get(block=False, timeout=0)
			except (queue.Empty) as e:
				pass
			else:
				#logger.info('serialThread inSerialQueue: "' + str(serialCommand) + '"')
				try:
					if not serialCommand.endswith('\n'):
						serialCommand += '\n'
					self.mySerial.write(serialCommand.encode())
					time.sleep(0.1)
					
					resp = self.mySerial.readline().decode().strip()
					self.outSerialQueue.put(resp)
					#logger.info('serialThread outSerialQueue: "' + str(resp) + '"')
				except (serial.SerialException) as e:
					#logger.error(str(e))
					print(str(e))
				except:
					#logger.error('other exception in mySerialThread run')
					raise
			"""

			# be sure to keep this here
			time.sleep(0.2) # second

#########################################################################
def testdht():

	humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
	
	if humidity is not None and temperature is not None:
		print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
	else:
		print('Failed to get reading. Try again!')
	

#########################################################################
def runpilogger(sensor=Adafruit_DHT.AM2302 , pin=3, interval=60):

	# save to this file
	"""
	# make directory if necc.
	if not os.path.exists(savePath):
		os.makedirs(savePath)
	"""

	inSerialQueue = queue.Queue() # put commands here to send out serial port
	outSerialQueue = queue.Queue()  # receive data coming in on the serial port
	errorSerialQueue = queue.Queue() 
	mySerialThread = SerialThread(inSerialQueue, outSerialQueue, errorSerialQueue, port, baud)
	mySerialThread.daemon = True
	mySerialThread.start()

	hostname = socket.gethostname()
	
	# make file with header if necc.
	if not os.path.isfile(savePath):
		with open(savePath, 'a') as f:
			headerLine = 'Hostname,Date,Time,Seconds,Temperature,Humidity' + '\n'
			f.write(headerLine)
			
	# initialize
	lastTimeSeconds = 0

	while True:
	
		# todo: merge nowSeconds and datetime_now (we are sampling time twice)
		nowSeconds = time.time() # epoch in seconds since January 1 1970

		datetime_now = datetime.now()
		theDate = datetime_now.strftime('%Y-%m-%d')
		theTime = datetime_now.strftime('%H:%M:%S')
		
		#
		# serial in from arduino
		# if we get data in outSerialQueue then process it
		# this happens when arduino spits out a temperature value
		try:
			serialReceive = outSerialQueue.get(block=False, timeout=0)
		except (queue.Empty) as e:
			pass
		else:
			if serialReceive:
				#print('serialReceive:', serialReceive)
				temperature = float(serialReceive)
				temperature = round(temperature,2)
				humidity = ''
				oneLine = hostname + ',' + theDate + ',' + theTime + ',' + str(nowSeconds) + "," + str(temperature) + "," + str(humidity) + "\n"
				print(oneLine)
				with open(savePath, 'a') as f:
					f.write(oneLine)
			
		#
		# DHT sensor hooked up to Pi, read it at an interval
		if False and nowSeconds > (lastTimeSeconds + intervalSeconds):
		
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
		
#########################################################################
if __name__ == '__main__':
	runpilogger()
	
