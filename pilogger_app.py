# Robert Cudmore
# 20180628

import sys, threading

from flask import Flask, render_template, send_file, Response

#from pilogger import runpilogger
import pilogger

app = Flask(__name__)

piloggerThread = threading.Thread(target = pilogger.runpilogger)
piloggerThread.daemon = True
piloggerThread.start()
print(1)

@app.route('/')
def hello_world():
	return render_template('index.html')

@app.route('/log')
def log():
	with open('./log/pilogger.log', 'r') as f:
		return Response(f.read(), mimetype='text/plain')

if __name__ == '__main__':	

	debug = False
	if len(sys.argv) == 2:
		if sys.argv[1] == 'debug':
			debug = True

	# 0.0.0.0 will run on external ip	
	app.run(host='0.0.0.0', debug=debug, threaded=True)