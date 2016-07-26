#Simple utility to test if the Tilt Hydrometer has been connected properly to the raspberry pi.
import TiltHydrometer
import thread
import time

tiltHydrometer = TiltHydrometer.TiltHydrometerManager(False, 60, 40)
tiltHydrometer.loadSettings()
tiltHydrometer.start()

def toString(value):
	returnValue = value
	if value is None:
		returnValue = ''
	return str(returnValue)
    
print "Scanning - 20 Secs (Control+C to exit early)"
for num in range(1,120):
	for colour in TiltHydrometer.TILTHYDROMETER_COLOURS:
		print colour + ": " + str(tiltHydrometer.getValue(colour))
	
	time.sleep(10)

tiltHydrometer.stop()
