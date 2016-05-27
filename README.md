These brewpi and other files have been modified to support the brewometer.

#Setup & Testing

On the raspberry pi you need to install the bluez bnd python-bluez luetooth modules to enable communication with the Brewometer.

	sudo apt-get install bluez python-bluez

Then you need to enable python to query bluetooth without being root.

	sudo setcap cap_net_raw+eip $(eval readlink -f `which python`)

Test that you've now enabled a connection by running the utility in the brewometer-test folder (this should not be run as root to test that we've enabled the appropriate permissions)
	
	python BrewometerTest.py

If you see values against your colour brewometer, then the connection has been successful.

# Modifying Brewpi for Brewometer logging

The files in the `brewpi-web` folder should be copied to the `/var/www` directory.

The files in the `brewpi-script` folder should be copied to the `/home/brewpi` directory.

Once the files have been copied across, you'll need to refresh the web interface and restart the script to start logging.


# Notes

The Brewometer calibration functions are not built in yet. The calibration through the app, is currently local to the app and does not impact the raw values coming out of the device. I've spoken with the Brewometer engineers and will look to incorporate the calibration function shortly.
