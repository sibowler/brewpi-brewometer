These brewpi and other files have been modified to support the brewometer.

#Setup & Testing

Ensure you are updated to the latest version of Brewpi using the update script in the `brewpi-tools` folder.

On the raspberry pi you need to install the bluez bnd python-bluez luetooth modules to enable communication with the Brewometer.

	sudo apt-get install bluez python-bluez python-scipy python-numpy libcap2-bin

Then you need to enable python to query bluetooth without being root.

	sudo setcap cap_net_raw+eip $(eval readlink -f `which python`)

Test that you've now enabled a connection by running the utility in the brewometer-test folder (this should not be run as root to test that we've enabled the appropriate permissions)
	
	python BrewometerTest.py

If you see values against your colour brewometer, then the connection has been successful.

# Modifying Brewpi for Brewometer logging

Ensure you have stopped any active logging.

The files in the `brewpi-web` folder should be copied to the `/var/www` directory. Ensure you fix the ownership once the files are copied over (`sudo chown -R www-data:www-data /var/www`)

The files in the `brewpi-script` folder should be copied to the `/home/brewpi` directory. Ensure you fix the ownership once the files are copied over (`sudo chown -R brewpi:brewpi /home/brewpi`)

Once the files have been copied across, you'll need to refresh the web interface and restart the script (button in top right-hand corner) to start logging. 


# Calibration:

To enable calibration for a brewometer create `GRAVITY.<colour>` or `TEMPERATURE.<colour>` files in the `/home/brewpi/brewometer` folder. Example files have been provided to show the syntax.

i.e. To calibrate a Red Brewometer's temperature, a `TEMPERATURE.red` file should be created with the calibration settings inside.

## Note:
If this is not your first install of the Brewometer modification, you will need to add the `python-scipy` and `python-numpy` libraries via apt-get. These libraries are used in the calibration function.

