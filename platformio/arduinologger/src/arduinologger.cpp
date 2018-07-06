/*
 * Author: Robert Cudmore
 * Date: 20180703
 *
 * arduinologger
 * read an analog temperature at an interval
 * and send the value out the serial port
 */
 
#include "Arduino.h"

int analogPin = 0;
String inString;

long int lastReading = 0; // ms
long int readingInterval = 60 * 1000; // ms

void setup()
{

  Serial.begin(115200);

  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }

} // setup()

void loop()
{

	//
	// Serial out
	long int now = millis();
	if (now > (lastReading + readingInterval)) {
		// generate fake temperature data
		float wholeNumber = analogRead(analogPin); // range is [0, 1023]
		float decimal = analogRead(analogPin) / 1023.0; // range is [0, 1023]
		float temperature = wholeNumber + decimal;
		Serial.println(temperature); //println casts float to str, 2 decimal places
		
		lastReading = now;
	}
	
	//
	// Serial in
	/*
	// serial available is True when there is data coming in
	if (Serial.available() > 0) {
		inString = Serial.readStringUntil('\n');
		//serialHandled = fakeScope.SerialIn(now, inString);
		inString.replace("\n","");
		inString.replace("\r","");
		//SerialIn(now, inString);
	}
	*/
	
}

