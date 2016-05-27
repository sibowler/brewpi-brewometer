#Simple utility to test if the brewometer has been connected properly to the raspberry pi.
import Brewometer
import thread
import time

brewometer = Brewometer.BrewometerManager(False)
brewometer.start()

def toString(value):
	returnValue = value
	if value is None:
		returnValue = ''
	return str(returnValue)
    
print "Scanning - 20 Secs (Control+C to exit early)"
for num in range(1,20):
	for colour in Brewometer.BREWOMETER_COLOURS:
		print colour + ": " + str(brewometer.getValue(colour))
	
	time.sleep(1)

brewometer.stop()
