# Brewometer polling library
# Simon Bowler 06/06/2016
# simon@bowler.id.au
# 
# Version: 1.1 - Added calibration and smoothing functions to reduce noise.

import blescan
import sys
import datetime

import bluetooth._bluetooth as bluez
import threading
import thread

import numpy

from scipy.interpolate import interp1d
from scipy import arange, array, exp
import csv
import functools

BREWOMETER_COLOURS = [ 'Red', 'Green', 'Black', 'Purple', 'Orange', 'Blue', 'Yellow', 'Pink' ]


#extrap1d Sourced from sastanin @ StackOverflow:
#http://stackoverflow.com/questions/2745329/how-to-make-scipy-interpolate-give-an-extrapolated-result-beyond-the-input-range
#This function is required as the interp1d function doesn't support extrapolation in the version of scipy that is currently available on the pi.
def extrap1d(interpolator):
    xs = interpolator.x
    ys = interpolator.y

    def pointwise(x):
        if x < xs[0]:
            return ys[0]+(x-xs[0])*(ys[1]-ys[0])/(xs[1]-xs[0])
        elif x > xs[-1]:
            return ys[-1]+(x-xs[-1])*(ys[-1]-ys[-2])/(xs[-1]-xs[-2])
        else:
            return interpolator(x)

    def ufunclike(xs):
        return array(map(pointwise, array(xs)))

    return ufunclike

#Simple offset calibration if only one point available.
def offsetCalibration(offset, value):
    return value + offset

#More complex interpolation calibration if more than one calibration point available
def extrapolationCalibration(extrapolationFunction, value):
    inputValue = [value]
    returnValue = extrapolationFunction(inputValue)
    return returnValue[0]

def noCalibration(value):
    return value
    
#Load the calibration settings from file and create the calibration functions    
def brewometerCalibrationFunction(type, colour):
    returnFunction = noCalibration
    
    originalValues = []
    actualValues = []
    csvFile = None
    filename = "brewometer/" + type.upper() + "." + colour.lower()
    
    try:
        #print "oppening file"
        csvFile = open(filename, "rb")
        csvFileReader = csv.reader(csvFile, skipinitialspace=True)
        
        for row in csvFileReader:
            #Skip any comment rows
            if (row[0][:1] != "#"): 
                originalValues.append(float(row[0]))
                actualValues.append(float(row[1]))
        
        #Close file
        csvFile.close()
    except IOError:
        print "Brewometer (" + colour + "):  " + type.capitalize() + ": No calibration data (" + filename  + ")"
    except Exception, e:
        print "ERROR: Brewometer (" + colour + "): Unable to initialise " + type.capitalize() + " Calibration data (" + filename  + ") - " + e.message
        #Attempt to close the file
        if (csvFile is not None):
            #Close file
            csvFile.close()
        
    #If more than two values, use interpolation
    if (len(actualValues) >= 2):
        interpolationFunction = interp1d(originalValues, actualValues, bounds_error=False, fill_value=1)
        returnFunction = functools.partial(extrapolationCalibration,extrap1d(interpolationFunction))
        print "Brewometer (" + colour + "): Initialised " + type.capitalize() + " Calibration: Interpolation"
    #Not enough values. Likely just an offset calculation
    elif (len(actualValues) == 1):
        offset = actualValues[0] - originalValues[0]
        returnFunction = functools.partial(offsetCalibration, offset)
        print "Brewometer (" + colour + "): Initialised " + type.capitalize() + " Calibration: Offset (" + str(offset) + ")"
    return returnFunction

#Median utility function        
def median(values):
        return numpy.median(numpy.array(values))

#Class to hold a Brewometer reading
class BrewometerValue:
    temperature = 0
    gravity = 0
    timestamp = 0
    
    def __init__(self, temperature, gravity):
        self.temperature = round(temperature, 2)
        self.gravity = round(gravity, 3)
        self.timestamp = datetime.datetime.now()
        
    def __str__(self):
        return "T: " + str(self.temperature) + " G: " + str(self.gravity)

#Brewometer class, looks after calibration, storing of values and smoothing of read values.        
class Brewometer:
    colour = ''
    values = None
    lock = None
    averagingPeriod = 0
    medianWindow = 0
    tempCalibrationFunction = None
    gravityCalibrationFunction = None
    
    #Averaging period is number of secs to average across. 0 to disable.
    #Median window is the window to use for applying a median filter accross the values. 0 to disable.
    def __init__(self, colour, averagingPeriod = 0, medianWindow = 0):
        self.colour = colour
        self.lock = threading.Lock()
        self.averagingPeriod = averagingPeriod
        self.medianWindow = medianWindow
        self.values = []
        self.tempCalibrationFunction = brewometerCalibrationFunction("temperature", colour)
        self.gravityCalibrationFunction = brewometerCalibrationFunction("gravity", colour)


    def setValues(self, temperature, gravity):
        """Set/add the latest temperature & gravity readings to the store. These values will be calibrated before storing if calibration is enabled"""
        with self.lock:
            self.cleanValues();
            calibratedTemperature = self.tempCalibrationFunction(temperature)
            calibratedGravity = self.gravityCalibrationFunction(gravity)
            self.values.append(BrewometerValue(calibratedTemperature, calibratedGravity))
            
    def getValues(self):
        """Returns the temperature & gravity values of the brewometer. This will be the latest read value unless averaging / median has been enabled"""
        with self.lock:
            returnValue = None
            if (len(self.values) > 0):
                if (self.medianWindow == 0):
                    returnValue = self.averageValues()
                else:
                    returnValue = self.medianValues(self.medianWindow)
                
                self.cleanValues();
        return returnValue
    
    def averageValues(self):
        """Internal function to average all the stored values"""
        returnValue = None
        if (len(self.values) > 0):
            returnValue = BrewometerValue(0,0)
            for value in self.values:
                returnValue.temperature += value.temperature
                returnValue.gravity += value.gravity
            
            #average values
            returnValue.temperature /= len(self.values)
            returnValue.gravity /= len(self.values)
            
            #round values
            returnValue.temperature = round(returnValue.temperature, 2)
            returnValue.gravity = round(returnValue.gravity, 3)
        return returnValue
    
    def medianValues(self, window = 3):
        """Internal function to use a median method across the stored values to reduce noise.
           window - Smoothing window to apply across the data. If the window is less than the dataset size, the window will be moved across the dataset,
                    taking a median value for each window, with the resultant set averaged"""
        returnValue = None
        #Ensure there are enough values to do a median filter, if not shrink window temporarily
        if (len(self.values) < window):
            window = len(self.values)
    
        #print "Median filter!"
        returnValue = BrewometerValue(0,0)
        
        sidebars = (window - 1) / 2
        medianValueCount = 0
        
        for i in range(len(self.values)-(window-1)):
            #Work out range of values to do median. At start and end of assessment, need to pad with start and end values.
            medianValues = self.values[i:i+window]
            medianValuesTemp = []
            medianValuesGravity = []
            
            #Separate out Temp and Gravity values
            for medianValue in medianValues:
                medianValuesTemp.append(medianValue.temperature)
                medianValuesGravity.append(medianValue.gravity)
            
            #Add the median value to the running total.
            returnValue.temperature += median(medianValuesTemp)
            returnValue.gravity += median(medianValuesGravity)
            
            #Increase count
            medianValueCount += 1
            
        #average values
        returnValue.temperature /= medianValueCount
        returnValue.gravity /= medianValueCount
        
        #round values
        returnValue.temperature = round(returnValue.temperature, 2)
        returnValue.gravity = round(returnValue.gravity, 3)

        return returnValue
    
    def cleanValues(self):
        """Function to clean out stale values that are beyond the desired window"""
        nowTime = datetime.datetime.now()

        for value in self.values:
            if ((nowTime - value.timestamp).seconds >= self.averagingPeriod):
                self.values.pop(0)
            else:
                #The list is sorted in chronological order, so once we've hit this condition we can stop searching.
                break

#Class to manage the monitoring of all Brewometers and storing the read values.                
class BrewometerManager:
    inFarenheight = True
    dev_id = 0
    averagingPeriod = 0
    medianWindow = 0
    
    scanning = True
    #Dictionary to hold brewometers - index on colour
    brewometers = {}
    
    brewthread = None
    
    def __init__(self, inFarenheight = True, averagingPeriod = 0, medianWindow = 0, device_id = 0):
        self.inFarenheight = inFarenheight
        self.dev_id = device_id
        self.averagingPeriod = averagingPeriod
        self.medianWindow = medianWindow


    def brewometerName(self, uuid):
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
        brewometer = self.brewometers.get(colour)
        if (brewometer is None):
            brewometer = Brewometer(colour, self.averagingPeriod, self.medianWindow)
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
        
        #Keep scanning until the manager is told to stop.
        while self.scanning:
            
            returnedList = blescan.parse_events(sock, 10)
            
            for beacon in returnedList:
                beaconParts = beacon.split(",")
                
                #Resolve whether the received BLE event is for a brewometer by looking at the UUID.
                name = self.brewometerName(beaconParts[1])
                
                #If the event is for a brewometer, process the data
                if name is not None:
                    #Get the temperature and convert to C if needed.
                    temperature = beaconParts[2]
                    if not self.inFarenheight:
                        temperature = self.convertFtoC(temperature)
                    
                    #Get the gravity.
                    gravity = self.convertSG(beaconParts[3])
                    
                    #Store the retrieved values in the relevant brewometer object.
                    self.storeValue(name, temperature, gravity)

    #Stop Scanning function
    def stop(self):
        self.scanning = False
    
    #Start the scanning thread
    def start(self):
        self.scanning = True
        self.brewthread = thread.start_new_thread(self.scan, ())

