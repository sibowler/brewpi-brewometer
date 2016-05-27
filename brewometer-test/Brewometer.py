# Brewometer polling library
# Simon Bowler 21/04/2016
# simon@bowler.id.au

import blescan
import sys

import bluetooth._bluetooth as bluez
import threading
import thread

BREWOMETER_COLOURS = [ 'Red', 'Green', 'Black', 'Purple', 'Orange', 'Blue', 'Yellow', 'Pink' ]
		
class BrewometerValue:
	temperature = 0
	gravity = 0
	
	def __init__(self, temperature, gravity):
		self.temperature = temperature
		self.gravity = gravity
		
	def __str__(self):
		return "T: " + str(round(self.temperature,2)) + " G: " + str(round(self.gravity,3))
		 
class Brewometer:
	colour = ''
	value = None
	lock = None
	
	def __init__(self, colour):
		self.colour = colour
		self.lock = threading.Lock()


	def setValues(self, temperature, gravity):
		with self.lock:
			self.value = BrewometerValue(temperature, gravity)
		
	def getValues(self):
		with self.lock:
			returnValue = self.value
			self.value = None
		return returnValue
		
class BrewometerManager:
	inFarenheight = True
	dev_id = 0
	
	scanning = True
	#Dictionary to hold brewometers - index on colour
	brewometers = {}
	
	brewthread = None
	
	def __init__(self, inFarenheight = True, device_id = 0):
		self.inFarenheight = inFarenheight
		self.dev_id = device_id


	def brewometerName(self, uuid):
		#print 'Lookup name: ' + uuid
		return {
				'a495bb10c5b14b44b5121370f02d74de' : 'Red',
				'a495bb20c5b14b44b5121370f02d74de' : 'Green',
				'a495bb30c5b14b44b5121370f02d74de' : 'Black',
				'a495bb40c5b14b44b5121370f02d74de' : 'Purple',
				'a495bb50c5b14b44b5121370f02d74de' : 'Orange',
				'a495bb60c5b14b44b5121370f02d74de' : 'Blue',
				'a495bb70c5b14b44b5121370f02d74de' : 'Yellow',
				'a495bb80c5b14b44b5121370f02d74de' : 'Pink'
		}.get(uuid)

	def convertFtoC(self, temperatureF):
		return (int(temperatureF) - 32) * 5.0 / 9
	
	def convertSG(self, gravity):
		return float(gravity)/ 1000
    
	#Store function
	def storeValue(self, colour, temperature, gravity):
		#print 'Adding Value: ' + colour + ":" + temperature + ":" + gravity
		brewometer = self.brewometers.get(colour)
		if (brewometer is None):
			brewometer = Brewometer(colour)
			self.brewometers[colour] = brewometer
			
		
		brewometer.setValues(temperature, gravity)
		
	#Retrieve function.
	def getValue(self, colour):
		returnValue = None
		brewometer = self.brewometers.get(colour)
		if (brewometer is not None):
			returnValue = brewometer.getValues()
		return returnValue
		
	#Scanner function
	def scan(self):
		try:
			sock = bluez.hci_open_dev(self.dev_id)

		except:
			print "error accessing bluetooth device..."
			sys.exit(1)

		blescan.hci_le_set_scan_parameters(sock)
		blescan.hci_enable_le_scan(sock)
		
	
		while self.scanning:
			
			returnedList = blescan.parse_events(sock, 10)
			
			for beacon in returnedList:
				beaconParts = beacon.split(",")
				
				name = self.brewometerName(beaconParts[1])
				
				if name is not None:
					temperature = beaconParts[2]
					if not self.inFarenheight:
						temperature = self.convertFtoC(temperature)
					gravity = self.convertSG(beaconParts[3])
					self.storeValue(name, temperature, gravity)

	#Stop Scanning function
	def stop(self):
		self.scanning = False
		
	def start(self):
		self.scanning = True
		self.brewthread = thread.start_new_thread(self.scan, ())

